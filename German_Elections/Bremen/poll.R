library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("German_Elections/Bremen/data.py")
poll <- read_csv("German_Elections/Bremen/poll.csv")
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)
election<-as.Date("14 05 2023", "%d %m %Y")

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#000000","#E3000F","#46962b","#BE3075","#009EE0", "#ffed00", "#0000AA", "#A2A9B1"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 3,linetype="solid",linewidth=0.75,wilder=TRUE)+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_text(aes((min(d$Date)+15),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_text(aes(election,0.02,label = "Election Date", vjust = -1, alpha=0.5),colour="#56595c", angle = 90)+
  xlim(min(d$Date), election)


ggsave(plot=plot1, file="German_Elections/Bremen/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1,alpha=0.5) +
  scale_color_manual(values = c("#000000","#E3000F","#46962b","#BE3075","#009EE0", "#ffed00", "#0000AA", "#A2A9B1"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75)+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'), legend.text = element_text(size=16))+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_text(aes((min(d$Date)+15),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_text(aes(election,0.02,label = "Election Date", vjust = -1, alpha=0.5),colour="#56595c", angle = 90)+
  xlim(min(d$Date), election)

ggsave(plot=plot2, file="German_Elections/Bremen/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#000000","#E3000F","#46962b","#BE3075","#009EE0", "#ffed00", "#0000AA", "#A2A9B1"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1)+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'), legend.text = element_text(size=16))+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_text(aes((min(d$Date)+15),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_text(aes(election,0.02,label = "Election Date", vjust = -1, alpha=0.5),colour="#56595c", angle = 90)+
  xlim(min(d$Date), election)


ggsave(plot=plot3, file="German_Elections/Bremen/plot3.png",width = 15, height = 7.5, type = "cairo-png")

