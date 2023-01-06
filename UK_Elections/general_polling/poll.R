library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
py_run_file("UK_Elections/general_polling/data.py")
poll <- read_csv("UK_Elections/general_polling/poll.csv")
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(sub("%","",d$value))/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
old<-as.Date("12 12 2019", "%d %m %Y")

starm<-as.Date("04 04 2020", "%d %m %Y")
davey<-as.Date("27 08 2020", "%d %m %Y")
green<-as.Date("01 10 2021", "%d %m %Y")
truss<-as.Date("06 09 2022", "%d %m %Y")
sunak<-as.Date("25 10 2022", "%d %m %Y")
f<-formattable::percent(0.6)
g<-formattable::percent(0.55)

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,]) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",linewidth=0.75,wilder=TRUE, data=d[d$Date!=old,])+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1)+
  geom_vline(xintercept=davey, linetype="dashed", color = "#FAA61A", alpha=0.5, size=1)+
  geom_vline(xintercept=green, linetype="dashed", color = "#528D6B", alpha=0.5, size=1)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_text(aes(starm,f,label = "Starmer", vjust = -1, angle=-90),colour="#E4003B")+
  geom_text(aes(davey,f,label = "Davey", vjust = -1, angle=-90),colour="#FAA61A")+
  geom_text(aes(green,g,label = "Denyer & Ramsay", vjust = -1, angle=-90),colour="#528D6B")+
  geom_text(aes(truss,f,label = "Truss", vjust = -1, angle=-90),colour="#0087DC")+
  geom_text(aes(sunak,f,label = "Sunak", vjust = -1, angle=-90),colour="#0087DC")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)


ggsave(plot=plot1, file="UK_Elections/general_polling/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,],alpha=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF"))+
  geom_smooth(method="loess",fullrange=TRUE,se=TRUE,span=0.075,linewidth=0.75, data=d[d$Date!=old,])+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1)+
  geom_vline(xintercept=davey, linetype="dashed", color = "#FAA61A", alpha=0.5, size=1)+
  geom_vline(xintercept=green, linetype="dashed", color = "#528D6B", alpha=0.5, size=1)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_text(aes(starm,f,label = "Starmer", vjust = -1, angle=-90),colour="#E4003B")+
  geom_text(aes(davey,f,label = "Davey", vjust = -1, angle=-90),colour="#FAA61A")+
  geom_text(aes(green,g,label = "Denyer & Ramsay", vjust = -1, angle=-90),colour="#528D6B")+
  geom_text(aes(truss,f,label = "Truss", vjust = -1, angle=-90),colour="#0087DC")+
  geom_text(aes(sunak,f,label = "Sunak", vjust = -1, angle=-90),colour="#0087DC")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot2, file="UK_Elections/general_polling/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,]) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1, data=d[d$Date!=old,])+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1)+
  geom_vline(xintercept=davey, linetype="dashed", color = "#FAA61A", alpha=0.5, size=1)+
  geom_vline(xintercept=green, linetype="dashed", color = "#528D6B", alpha=0.5, size=1)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_text(aes(starm,f,label = "Starmer", vjust = -1, angle=-90),colour="#E4003B")+
  geom_text(aes(davey,f,label = "Davey", vjust = -1, angle=-90),colour="#FAA61A")+
  geom_text(aes(green,g,label = "Denyer & Ramsay", vjust = -1, angle=-90),colour="#528D6B")+
  geom_text(aes(truss,f,label = "Truss", vjust = -1, angle=-90),colour="#0087DC")+
  geom_text(aes(sunak,f,label = "Sunak", vjust = -1, angle=-90),colour="#0087DC")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot3, file="UK_Elections/general_polling/plot3.png",width = 15, height = 7.5, type = "cairo-png")
