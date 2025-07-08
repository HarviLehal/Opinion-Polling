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
library(ggbreak)

py_run_file("UK/Seats/data.py")
poll <- read_csv("UK/Seats/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
h <- 325

# election<-as.Date("04 07 2024", "%d %m %Y")
election<-max(d$Date)+1
old <-min(d$Date)
start <-min(d[d$Date!=min(d$Date),]$Date)-1
# MAIN GRAPH
# start <-as.Date("25 05 2024", "%d %m %Y")
# d <- d[d$Date>start|d$Date==old,]

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1.5, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#E4003B","#0087DC","#FAA61A","#FDF38E","#12B6CF","#528D6B","#005b54","#BBBBBB"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.875,linewidth=1, data=d[d$Date!=old,])+
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
  geom_hline(aes(yintercept=h),colour="#000000",linetype="dashed")+
  geom_text(aes((start-0.5),h,label = "Majority (326 Seats)",hjust=0 ,vjust = -1),colour="#000000",fontface="bold")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_break(c(old+4, start))+
  scale_x_date(date_breaks = "2 weeks", date_labels =  "%d %b %Y",limits = c(old-4,election),guide = guide_axis(angle = -90))+
  scale_y_continuous(breaks=seq(0,650,25))
plot1

# Bar Chart

poll <- read_csv("UK/Seats/poll.csv")
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


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#f27999","#E4003B","#77c0ed","#0087DC",
                               "#fcd38b","#FAA61A","#fcf7c5","#FDF38E",
                               "#80dae8","#12B6CF","#9dc7af","#528D6B",
                               "#669d98","#005b54","#DDDDDD","#BBBBBB"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average \n (2024 Result)')+
  scale_x_discrete(limits = d3$variable[order(d1$value,d2$value,na.last = FALSE)])+
  coord_flip()+
  geom_hline(aes(yintercept=h), linetype="dashed",colour="#000000")

plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="UK/Seats/plot.png",width = 15, height = 7.5, type = "cairo-png")
