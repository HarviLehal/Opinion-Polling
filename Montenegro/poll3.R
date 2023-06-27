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

py_run_file("Montenegro/data2.py")
poll <- read_csv("Montenegro/poll3.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.03)

election<-as.Date("11 06 2023", "%d %m %Y")
old <-min(d$Date)

# LOESS GRAPH

plot<-ggplot(data=d[d$Date!=old&d$Date!=election,],aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.75)+
  scale_color_manual(values = c("#6866B2","#F08080","#00008B","#6CB4EE",
                                "#32CD32","#FF0000","#2B2C2D","#FFCC00","#800080"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "3% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)

plot
ggsave(plot=plot, file="Montenegro/plot.svg",width = 15, height = 7.5)
aaa=readLines("Montenegro/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Montenegro/plot.svg")
