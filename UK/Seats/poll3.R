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

py_run_file("UK/Seats/data2.py")
poll <- read_csv("UK/Seats/poll3.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
h <- 0

election<-as.Date("04 07 2024", "%d %m %Y")
# election<-max(d$Date)+14
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  # geom_point(size=2,data=d) +
  geom_point(size=2,data=d)+
  geom_line()+
  scale_color_manual(values = c("#0884dc"))+
  geom_hline(aes(yintercept=h))+
  scale_x_date(date_breaks = "3 month", date_labels =  "%b %Y",limits = c(old-11,election),guide = guide_axis(angle = -90))+
  ylim(0,100)+
  scale_y_continuous(breaks=seq(0,100,5))+
  geom_text(data=d[d$Date==max(d$Date),], aes(label = value), hjust=0, vjust=0, nudge_x = 7, nudge_y = 0, size=3.5, fontface="bold")+
  geom_text(data=d[d$Date==min(d$Date),], aes(label = value), hjust=0, vjust=0, nudge_x = -4, nudge_y = -3, size=3.5, fontface="bold")+
  bbplot::bbc_style()
plot1

ggsave(plot=plot1, file="UK/Seats/plot3.png",width = 15, height = 7.5, type = "cairo-png")
