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

py_run_file("Irish/data.py")
poll <- read_csv("Irish/poll.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("20 02 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#39675F","#74BC64","#729AFF","#45AD6E", "#C11112", "#712C8D","#87221E","#445225"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot, file="Irish/plot.png",width = 15, height = 7.5,type="cairo-png")
