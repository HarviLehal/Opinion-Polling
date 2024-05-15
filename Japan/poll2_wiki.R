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
poll <- read_csv("Japan/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("29 10 2025", "%d %m %Y")
abe<-as.Date("08 07 2022", "%d %m %Y")
slush<-as.Date("08 12 2023", "%d %m %Y")
old <-min(d$Date)
now <-max(d$Date)
f<-formattable::percent(0.8)

# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d[d$Date!=old,],aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#3ca324","#184589","#b8ce43","#f95580","#db001c",
                                "#ffba00","#ed008c","#ed7301","#1ca9e9","#60bcaf"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.6,linewidth=0.75, data=d[d$Date!=old,])+
  geom_vline(xintercept=abe, linetype="dashed", color = "#3ca324", alpha=0.5, size=1)+
  geom_vline(xintercept=slush, linetype="dashed", color = "#3ca324", alpha=0.5, size=1)+
  geom_text(aes(abe,f,label = "Abe Assassinated", vjust = -1, hjust=0, angle=-90),colour="#3ca324")+
  geom_text(aes(slush,f,label = "Slush Fund Scandal", vjust = -1, hjust=0, angle=-90),colour="#3ca324")+
  # bbplot::bbc_style()+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.8,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  scale_x_date(date_breaks = "3 month", date_labels =  "%b %Y",limits = c(old,now+14),guide = guide_axis(angle = -45))+
  ggtitle('Japanese Party Identification Polling Since 2022 (Excluding None)')

poll <- read_csv("Japan/poll2.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

plot2<-ggplot(data=d1, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#3ca324","#184589","#b8ce43","#f95580",
                               "#db001c","#ffba00","#ed008c","#ed7301",
                               "#1ca9e9","#60bcaf"))+
  geom_text(aes(label = formattable::percent(d1$value, digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 day average')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Japan/plot2_wiki.png",width = 21, height = 7, type="cairo-png")
