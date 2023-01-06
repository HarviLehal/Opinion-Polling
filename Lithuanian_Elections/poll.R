library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Lithuanian_Elections/data.py")
poll <- read_csv("Lithuanian_Elections/poll.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("06 10 2024", "%d %m %Y")
old<-min(d$Date)
g<-formattable::percent(0.05)
h<-formattable::percent(0.07)

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.75)+
  scale_color_manual(values = c("#3DA49A","#319032","#2D568C","#D41720",
                                "#D6136E","#E98313","#711625","#C2312F",
                                "#369C3A","#F3BB0C","#121072"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(aes(yintercept=g), alpha=0.75, linetype="dashed", colour="#000000")+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="dotted", colour="#000000")+
  geom_text(aes(election,g,label = "5% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_text(aes(election,h,label = "7% Coalition Threshold", vjust = -1, hjust=1),colour="#56595c")
  
ggsave(plot=plot, file="Lithuanian_Elections/plot.png",width = 15, height = 7.5, type = "cairo-png")
 