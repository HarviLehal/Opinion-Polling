library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Turkish/Campaign/data.py")
poll <- read_csv("Turkish/Campaign/poll.csv")


d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("14 05 2023", "%d %m %Y")
d$Date<-as.Date(d$Date)
old<-as.Date("10 03 2023", "%d %m %Y")
ban<-as.Date("04 05 2023", "%d %m %Y")
h <- formattable::percent(0.5)
g <- formattable::percent(0.54)

# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.75)+
  scale_color_manual(values = c("#FFCC00","#ed1c24",
                                "#3e4042","#0d5ca6"))+
  geom_smooth(method='loess',fullrange=TRUE,span=0.5,se=FALSE,linewidth=0.75, data=d)+
  # stat_smooth(method='lm', formula = y~poly(x,2),se=FALSE)+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((election),h,label = "50%",hjust=1 ,vjust = -1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_vline(xintercept=ban, linetype="dashed", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_text(aes(ban,g,label = "Polling Ban", vjust = -1, angle=-90))+
  xlim(old, election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)
plot
ggsave(plot=plot, file="Turkish/Campaign/plot.svg",width = 15, height = 7.5)
aaa=readLines("Turkish/Campaign/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Turkish/Campaign/plot.svg")
