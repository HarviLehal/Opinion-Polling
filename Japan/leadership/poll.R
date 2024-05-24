library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(svglite)
library(Rcpp)
library(ggpubr)
library(zoo)
library(tidyverse)
library(data.table)
library(hrbrthemes)
py_run_file("Japan/leadership/data.py")
poll <- read_csv("Japan/leadership/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("29 10 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d[d$Date!=old,],aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#224192","#b61b28","#43b3ae","#1e90ff","#ff7538",
                                "#ff69b4","#228b22","#9370db","#f2ba42","#444444",
                                "#999999"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.8,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  ggtitle('Preferred Prime Minister of Japan')
  # bbplot::bbc_style()
plot1

poll <- read_csv("Japan/leadership/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x)
  as.numeric(sub("%","",as.character(x)))))
poll<-poll[poll$Date==max(poll$Date),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

plot2<-ggplot(data=d1, aes(x=forcats::fct_rev(variable), y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#224192","#b61b28","#43b3ae","#1e90ff","#ff7538",
                               "#ff69b4","#228b22","#9370db","#f2ba42","#444444",
                               "#999999"))+
  geom_text(aes(label = ifelse(d1$Date == min(d1$Date),paste(d1$value),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Japan/leadership/plot.png",width = 15, height = 7.5, type = "cairo-png")

