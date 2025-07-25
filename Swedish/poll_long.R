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

poll1 <- read_csv("Swedish/poll_old.csv")
poll2 <- read_csv("Swedish/poll.csv")
poll <- rbind(poll1,poll2) 
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h<-formattable::percent(0.04)
next_election<-as.Date("13 09 2026", "%d %m %Y")
election<-as.Date("11 09 2022", "%d %m %Y")
old_election <-min(d$Date)

d_old <- reshape2::melt(poll1, id.vars="Date")
d_old$value<-as.numeric(d_old$value)/100
d_old$value<-formattable::percent(d_old$value)
d_new <- reshape2::melt(poll2, id.vars="Date")
d_new$value<-as.numeric(d_new$value)/100
d_new$value<-formattable::percent(d_new$value)

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old_election&d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#A60D0E","#DF253A","#419129","#1E4838",
                                "#2B69B3","#3F9BDB","#255DA1","#e0ca0b"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_old[d_old$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_new[d_new$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((next_election-5),h,label = "4% Threshold",hjust=1 ,vjust = -1),colour="#56595c")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=old_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), next_election)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old_election,next_election),guide = guide_axis(angle = -90))+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot1

poll1 <- read_csv("Swedish/poll_old.csv")
poll2 <- read_csv("Swedish/poll.csv")
poll <- rbind(poll1,poll2) 
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==election,]
poll<-poll[poll$Date>(max(poll$Date)-30),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)
d2<-d2[!duplicated(d2), ]

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)

plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
geom_bar(stat="identity",width=0.9, position=position_dodge())+
scale_fill_manual(values = c("#d17171","#A60D0E","#f08d97","#DF253A",
                             "#93c981","#419129","#74a391","#1E4838",
                             "#86add9","#2B69B3","#9acced","#3F9BDB",
                             "#7ea2cf","#255DA1","#f0e585","#e0ca0b"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), ifelse(is.nan(d3$value)==FALSE,paste(formattable::percent(d3$value, digits = 1)),"")
                               ,""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),
                               ifelse(is.na(d3$value)==TRUE,"(New)",
                                      (paste("(",formattable::percent(d3$value, digits = 1),")"))),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(1), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 30 day average \n (2022 Result)')+
  scale_x_discrete(limits = d3$variable[order(d1$value,d2$value,na.last = FALSE)])+
  coord_flip()


plotA<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA

ggsave(plot=plotA, file="Swedish/plot_long.png",width = 15, height = 7.5, type="cairo-png")
