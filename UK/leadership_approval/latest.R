library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("UK/leadership_approval/latest.py")
poll <- read_csv("UK/leadership_approval/latest2023.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(sub("%","",d$value))
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
old<-as.Date("12 12 2019", "%d %m %Y")

f<-formattable::percent(0.6)
g<-formattable::percent(0.55)

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d) +
  scale_color_manual(values = c("#E4003B","#0087DC","#56595c"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,wilder=TRUE, data=d)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)
plot1


plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d) +
  scale_color_manual(values = c("#E4003B","#0087DC","#56595c"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_smooth(method="loess",fullrange=TRUE,se=TRUE,span=0.25,linewidth=0.75, data=d)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)
plot2  
