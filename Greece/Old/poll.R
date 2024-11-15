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
py_run_file("Greece/data.py")
poll <- read_csv("Greece/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.03)

election<-as.Date("21 05 2023", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old|d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#325BC7","#E48291",
                                "#389043","#D61616",
                                "#6192CE","#B83824"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.15,linewidth=0.75, data=d[d$Date!=old|d$Date!=election,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "3% Threshold", vjust = -1, hjust=1),colour="#56595c")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)

plot1

poll <- read_csv("Greece/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)
d3 <- as.data.frame(d3)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d4<-rbind(d1,d2,d3)


plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
geom_bar(stat="identity",width=0.9, position=position_dodge())+
scale_fill_manual(values = c("#325BC7","#8fa5e3","#0f3fbd",
                             "#E48291","#f2bdc7","#de4b62",
                             "#389043","#89c793","#187824",
                             "#D61616","#eb8181","#800808",
                             "#6192CE","#acc8e8","#20497a",
                             "#B83824","#db8f84","#801b0b"))+
geom_text(aes(label = formattable::percent(ifelse(d4$Date != min(d4$Date), d4$value, ""), digits = 2),
              y = 0),
          hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
geom_text(aes(label = ifelse(d4$Date == min(d4$Date),paste("(",d2$value,")"),""),
              y = 0),
          hjust=0, color="#000000", position = position_dodge(1), size=3.5)+
theme_minimal()+
theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
      panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
      panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
      plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
ggtitle(' Results (90.76% Reporting) \n 7 day Average \n (2019 Election)')+
scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="Greece/plot.png",width = 15, height = 7.5, type="cairo-png")
