library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Polish_Elections/data.py")
poll <- read_csv("Polish_Elections/poll.csv")
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value[is.nan(d$value)] <- 0
d<-na.omit(d)
h <- 231

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#263778","#F68F2D","#851A64","#1BB100","#122746", "#F9C013", "#A2A9B1"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 3,linetype="solid",linewidth=0.75,wilder=TRUE)+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((min(d$Date)+10),h,label = "Majority (231 Seats)", vjust = -1),colour="#56595c")


ggsave(plot=plot1, file="Polish_Elections/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5,alpha=0.5) +
  scale_color_manual(values = c("#263778","#F68F2D","#851A64","#1BB100","#122746", "#F9C013", "#A2A9B1"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75)+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank())+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((min(d$Date)+10),h,label = "Majority (231 Seats)", vjust = -1),colour="#56595c")

ggsave(plot=plot2, file="Polish_Elections/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#263778","#F68F2D","#851A64","#1BB100","#122746", "#F9C013", "#A2A9B1"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1)+
  theme(axis.title=element_blank(),legend.title = element_blank())+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((min(d$Date)+10),h,label = "Majority (231 Seats)", vjust = -1),colour="#56595c")


ggsave(plot=plot3, file="Polish_Elections/plot3.png",width = 15, height = 7.5, type = "cairo-png")

