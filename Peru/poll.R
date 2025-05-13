library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(ggpubr)
library(zoo)
library(dplyr)

py_run_file("Peru/data.py")
poll <- read_csv("Peru/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
old<-min(d$Date)
election<-max(d$Date)+14



plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#33a22b","#c70000","#CDCDCD"
  ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.05))+
  # geom_hline(aes(yintercept=0), alpha=0.5, linewidth=1, linetype="dashed", colour="#000000")+
  # geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  # geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  scale_x_date(date_breaks = "1 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  # geom_hline(yintercept = 0, size = 1, colour="#333333",alpha=0)+
  ggtitle('Dina Boluarte Approval Rating')

ggsave(plot=plot1, file="Peru/plot.png",width = 15, height = 7.5, type="cairo-png")




poll <- read_csv("Peru/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-formattable::percent(d$value)
old<-min(d$Date)
election<-max(d$Date)+14
plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#c70000"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(-1,1,0.05))+
  # geom_hline(aes(yintercept=0), alpha=0.5, linewidth=1, linetype="dashed", colour="#000000")+
  # geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  # geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  scale_x_date(date_breaks = "1 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  geom_hline(yintercept = -1, size = 1, colour="#333333",alpha=0)+
  ggtitle('Dina Boluarte Net Approval Rating (Excluding Neithers)')


ggsave(plot=plot2, file="Peru/plot2.png",width = 15, height = 7.5, type="cairo-png")
