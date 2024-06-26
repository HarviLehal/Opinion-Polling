library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Turkish/data2.py")
poll2 <- read_csv("Turkish/poll2.csv")

d2 <- reshape2::melt(poll2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value)
election<-as.Date("14 05 2023", "%d %m %Y")
old<-min(d2$Date)
d2$Date<-as.Date(d2$Date)
h <- formattable::percent(0.5)

# MAIN GRAPH

plot2<-ggplot(data=d2,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d2[d2$Date!=old,],alpha=0.75)+
  scale_color_manual(values = c("#FFCC00","#3db5e6","#870000","#006aa7", "#2db34a" ,"#ff5f5f","#0d5ca6","#ed1c24","#951b88"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.4,linewidth=0.75, data=d2[d2$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((election),h,label = "50%",hjust=1 ,vjust = -1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d2$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d2[d2$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d2[d2$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot2, file="Turkish/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

