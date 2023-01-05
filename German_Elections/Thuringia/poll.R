library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("German_Elections/Thuringia/data.py")
poll <- read_csv("German_Elections/Thuringia/poll.csv")
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#BE3075","#009EE0","#000000","#E3000F","#46962b", "#ffed00", "#A2A9B1"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 3,linetype="solid",linewidth=0.75,wilder=TRUE)+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_text(aes((min(d$Date)+20),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")

ggsave(plot=plot1, file="German_Elections/Thuringia/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1,alpha=0.5) +
  scale_color_manual(values = c("#BE3075","#009EE0","#000000","#E3000F","#46962b", "#ffed00", "#A2A9B1"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75)+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'), legend.text = element_text(size=16))+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_text(aes((old+20),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")+
  geom_point(aes(x=old,y=formattable::percent(0.310)),colour="#BE3075", shape=18, size=2.5)+
  geom_point(aes(x=old,y=formattable::percent(0.234)),colour="#009EE0", shape=18, size=2.5)+
  geom_point(aes(x=old,y=formattable::percent(0.217)),colour="#000000", shape=18, size=2.5)+
  geom_point(aes(x=old,y=formattable::percent(0.082)),colour="#E3000F", shape=18, size=2.5)+
  geom_point(aes(x=old,y=formattable::percent(0.052)),colour="#46962b", shape=18, size=2.5)+
  geom_point(aes(x=old,y=formattable::percent(0.050)),colour="#ffed00", shape=18, size=2.5)+
  geom_point(aes(x=old,y=formattable::percent(0.049)),colour="#A2A9B1", shape=18, size=2.5)

ggsave(plot=plot2, file="German_Elections/Thuringia/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#BE3075","#009EE0","#000000","#E3000F","#46962b", "#ffed00", "#A2A9B1"))+
  bbplot::bbc_style()+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1)+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'), legend.text = element_text(size=16))+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_text(aes((min(d$Date)+20),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")

ggsave(plot=plot3, file="German_Elections/Thuringia/plot3.png",width = 15, height = 7.5, type = "cairo-png")

