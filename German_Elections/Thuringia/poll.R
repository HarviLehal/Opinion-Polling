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
old <-min(d$Date)
# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.75)+
  scale_color_manual(values = c("#BE3075","#009EE0","#000000","#E3000F","#46962b", "#ffed00", "#A2A9B1"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(old, max(d$Date))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  geom_text(aes((max(d$Date)-20),h,label = "5% Electoral Threshold", vjust = -1),colour="#56595c")

ggsave(plot=plot, file="German_Elections/Thuringia/plot.png",width = 15, height = 7.5, type = "cairo-png")
