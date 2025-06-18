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
library(ggbreak)
poll <- read_csv("Norwegian/poll_seats2.csv")
Sys.setlocale("LC_ALL", "Norwegian")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)

election<-as.Date("08 09 2025", "%d %m %Y")
start <- as.Date("10 Jan 2025", "%d %b %Y")
old <-min(d$Date)

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#c82518","#01438e"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold",color="#000000"),
        axis.text.y = element_text(face="bold",color="#000000"),
        plot.title = element_text(face="bold",color="#000000"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_y_continuous(name="Vote",breaks=seq(0,120,5))+
  scale_x_break(c(old+2, start))+
  scale_x_date(date_breaks = "1 week", date_labels =  "%d %b %Y",limits = c(old-2,election),guide = guide_axis(angle = -90))+
  ggtitle('Meningsmåling til Stortingsvalget 2025')
plot1

# MA GRAPH


# BAR CHART

poll <- read_csv("Norwegian/poll_seats2.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
d1 <- round(colMeans(poll[-1],na.rm=TRUE), digits=0)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")

d2 <- reshape2::melt(d2, id.vars="Date")

d3<-rbind(d2,d1)


# EXTRA GRAPHIEK


d1$value<-ifelse(is.na(d1$value)==TRUE,0,d1$value)
d2$value<-ifelse(is.na(d2$value)==TRUE,0,d2$value)
d1$value<-d1$value/169
d2$value<-d2$value/169
d1$Date<-'Gjennomsnitt'
d2$Date<-'Resultat'

d3<-rbind(d2,d1)


plot2<-ggplot(d3, aes(fill=interaction(Date,variable), y=value, x=Date,label=round(value*150))) + 
  scale_fill_manual(values = c("#de7c74","#c82518",
                               "#678ebb","#01438e"))+
  geom_bar(position="fill", stat="identity")+
  geom_text(data=subset(d3,value != 0),size = 5.5, position = position_stack(vjust = 0.5),fontface="bold",color="#000000")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold",color="#000000",size=10),
        axis.text.y = element_text(face="bold.italic",size=15,color="#000000",hjust=1),
        # axis.text.y = element_blank(),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=0.5,alpha=0.25) +
  coord_flip()
plot2


plot<-aplot::plot_list(plot1, plot2,ncol = 1, nrow = 2,heights=c(2,0.3))
plot

ggsave(plot=plot, file="Norwegian/plot_seats2.png",width = 20, height = 10, type="cairo-png")
Sys.setlocale("LC_ALL", "English")