library(reticulate)
py_run_file("data.py")
library(readr)
poll <- read_csv("poll.csv")
library(reshape2)
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(sub("%","",d$value))/100
d$value[is.nan(d$value)] <- 0
library(formattable)
d$value<-formattable::percent(d$value)
print(class(d$value))
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)

# MAIN GRAPH

ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = formattable::percent,breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,wilder=TRUE)

# LOESS GRAPH

ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B"))+
  geom_smooth(method="loess",fullrange=TRUE,se=TRUE,span=0.3,size=0.75)+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = formattable::percent,breaks=seq(0,0.6,0.05))

# EXPERIMENTAL THINGS

ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = formattable::percent,breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1)
