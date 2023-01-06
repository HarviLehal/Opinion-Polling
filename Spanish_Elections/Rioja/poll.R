library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Spanish_Elections/Rioja/data.py")
poll <- read_csv("Spanish_Elections/Rioja/poll.csv")
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
d$value[d$value == 0] <- NA
election<-as.Date("28 05 2023", "%d %m %Y")
old<-as.Date("26 05 2019", "%d %m %Y")

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c('#EF1C27',"#1D84CE","#EB6109",'#7B4977','#00AA42',"#63BE21"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 3,linetype="solid",linewidth=0.75,wilder=TRUE)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_text(aes(election,0.02,label = "Election Date", vjust = -1, alpha=0.5),colour="#56595c", angle = 90)+
  xlim(min(d$Date), election)


ggsave(plot=plot1, file="Spanish_Elections/Rioja/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.75)+
  scale_color_manual(values = c('#EF1C27',"#1D84CE","#EB6109",'#7B4977','#00AA42',"#63BE21"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.65,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'), legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_text(aes(election,0.02,label = "Election Date", vjust = -1, alpha=0.5),colour="#56595c", angle = 90)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot2, file="Spanish_Elections/Rioja/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c('#EF1C27',"#1D84CE","#EB6109",'#7B4977','#00AA42',"#63BE21"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1)+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'), legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_text(aes(election,0.02,label = "Election Date", vjust = -1, alpha=0.5),colour="#56595c", angle = 90)+
  xlim(min(d$Date), election)


ggsave(plot=plot3, file="Spanish_Elections/Rioja/plot3.png",width = 15, height = 7.5, type = "cairo-png")

