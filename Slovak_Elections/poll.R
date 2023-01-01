library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Slovak_Elections/data.py")
poll <- read_csv("Slovak_Elections/poll.csv")
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#BED62F","#D82222","#034B9F","#005222","#00BDFF", "#007FFF", "#A7CF35", "#FDBB12", "#173A70", "#FF0000", "#0000CD"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 3,linetype="solid",linewidth=0.75,wilder=TRUE)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  geom_text(aes((min(d$Date)+15),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")


ggsave(plot=plot1, file="Slovak_Elections/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5,alpha=0.5) +
  scale_color_manual(values = c("#BED62F","#D82222","#034B9F","#005222","#00BDFF", "#007FFF", "#A7CF35", "#FDBB12", "#173A70", "#FF0000", "#0000CD"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75)+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  geom_text(aes((min(d$Date)+15),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")

ggsave(plot=plot2, file="Slovak_Elections/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#BED62F","#D82222","#034B9F","#005222","#00BDFF", "#007FFF", "#A7CF35", "#FDBB12", "#173A70", "#FF0000", "#0000CD"))+
  # bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.35)+
  theme(axis.title=element_blank(),legend.title = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  geom_text(aes((min(d$Date)+15),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")


ggsave(plot=plot3, file="Slovak_Elections/plot3.png",width = 15, height = 7.5, type = "cairo-png")

