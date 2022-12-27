library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Turkish_Elections/data.py")
poll <- read_csv("Turkish_Elections/poll.csv")
z = length(poll$Date)
for (i in 1:z){
  print( i)
  if (nchar(poll$Date[i]) < 10) {
    print(nchar(poll$Date[i]))
    poll$Date[i] <- paste("15 ", poll$Date[i])
  }
}


d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(sub("%","",d$value))/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)


# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#FFCC00","#3db5e6","#ff5f5f","#870000","#006aa7", "#2db34a","#0d5ca6","#ed1c24","#951b88"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 3,linetype="solid",linewidth=0.75,wilder=TRUE)

ggsave(plot=plot1, file="Turkish_Elections/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#FFCC00","#3db5e6","#ff5f5f","#870000","#006aa7", "#2db34a","#0d5ca6","#ed1c24","#951b88"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.45,linewidth=0.75)+
  # bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))

ggsave(plot=plot2, file="Turkish_Elections/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#FFCC00","#3db5e6","#ff5f5f","#870000","#006aa7", "#2db34a","#0d5ca6","#ed1c24","#951b88"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1)

ggsave(plot=plot3, file="Turkish_Elections/plot3.png",width = 15, height = 7.5, type = "cairo-png")

