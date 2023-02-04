library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(svglite)
library(Rcpp)
library(ggpubr)

py_run_file("Dutch_Elections/data.py")
poll <- read_csv("Dutch_Elections/poll.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
election<-as.Date("01 03 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# SEATS

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#222ACA","#3DAD3E","#0E2758",
                                "#53C74A","#E81718","#D21D24",
                                "#8ABD00","#7C1B1C","#226B26",
                                "#43A6EB","#552C83","#262B57",
                                "#DD601C","#45B6B1","#8C2591",
                                "#99C11A","#FBFD00","#162141"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)


# VOTES

poll <- read_csv("Dutch_Elections/poll2.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(sub("%","",d$value))/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(1/150)
election<-as.Date("01 03 2025", "%d %m %Y")
old <-min(d$Date)

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#222ACA","#3DAD3E","#0E2758",
                                "#53C74A","#E81718","#D21D24",
                                "#8ABD00","#7C1B1C","#226B26",
                                "#43A6EB","#552C83","#262B57",
                                "#DD601C","#45B6B1","#8C2591",
                                "#99C11A","#FBFD00","#162141"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "0.67% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,heights=c(4,4),widths=c(8,8))
plot

ggsave(plot=plot, file="Dutch_Elections/plot.png",width = 15, height = 7.5, type="cairo-png")

