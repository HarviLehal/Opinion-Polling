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
library(dplyr)
library(ggbreak)

poll <- read_csv("Norwegian/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
# election<-as.Date("22 11 2023", "%d %m %Y")
old <-min(d$Date)
election<-as.Date("01 09 2025", "%d %m %Y")

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#c82518","#01438e"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d[d$Date!=old,])+
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
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_hline(yintercept=0,alpha=0)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "1 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Red-Blue Bloc Polling for the Next Norwegian General Election')

plot1

# BAR CHART

poll <- read_csv("Norwegian/poll2.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)



plot3<-ggplot(d3, aes(fill=interaction(Date,variable), y=value, x=Date)) + 
  scale_fill_manual(values = c("#de7c74","#c82518",
                               "#678ebb","#01438e"
  ))+
  geom_bar(position="fill", stat="identity")+
  geom_text(aes(label = ifelse(d3$Date==max(d3$Date),ifelse(d3$variable=="Red",paste("Red:",d3$value),ifelse(d3$variable=="Blue",paste("Blue:",d3$value),paste("M:",d3$value))),
                               ifelse(d3$variable=="Red",paste("Current Red:",d3$value),ifelse(d3$variable=="Blue",paste("Current Blue:",d3$value),paste("M:",d3$value)))),
                hjust=0.5, vjust = 0.5,y = ifelse(d3$variable=="Red",0.89,ifelse(d3$variable=="Blue",0.11,0.47))),
            color="#000000",position =, size=5, fontface="bold")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_blank(),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=1,alpha=0.75) +
  coord_flip()

plot3


plotA<-ggarrange(plot1, plot3,ncol = 1, nrow = 2,heights=c(2,0.3))
plotA

ggsave(plot=plotA, file="Norwegian/plot2.png",width = 20, height = 10, type="cairo-png")
