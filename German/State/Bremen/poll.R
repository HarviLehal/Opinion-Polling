library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(ggbreak)

py_run_file("German/State/Bremen/data.py")
poll <- read_csv("German/State/Bremen/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("14 05 2023", "%d %m %Y")
old<-min(d$Date)

# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1,alpha=0.5) +
  scale_color_manual(values = c("#000000","#E3000F","#46962b","#BE3075","#009EE0", "#ffed00", "#0000AA", "#A2A9B1"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(old,election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_break(c(old+90, as.Date("01 01 2022", "%d %m %Y")))+
  scale_x_date(date_breaks = "3 month", date_labels =  "%m %Y",limits = c(old-10,election+10))

ggsave(plot=plot, file="German/State/Bremen/plot.png",width = 15, height = 7.5, type = "cairo-png")

