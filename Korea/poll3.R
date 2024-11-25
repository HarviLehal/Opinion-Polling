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
library(zoo)
library(tidyverse)
library(data.table)
library(hrbrthemes)
py_run_file("Korea/data3.py")
poll <- read_csv("Korea/approval.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
f<-formattable::percent(0.9)
election<-as.Date("03 03 2027", "%d %m %Y")
# election<-max(d$Date)+2


# LOESS GRAPH
d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 7, Date), mean,na.rm=TRUE))

plotwiki<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#3ca324","#db001c","#666666"))+
  # geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        # legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Approval",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.9,0.05))+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(min(d$Date)-2,election),guide = guide_axis(angle = -90))+
  ggtitle('Yoon Suk Yeol Presidency Approval')
plotwiki
ggsave(plot=plotwiki, file="Korea/approval.png",width = 15, height = 7.5, type = "cairo-png")






# NET APPROVAL
poll <- read_csv("Korea/approval2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 7, Date), mean,na.rm=TRUE))

plotwiki<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#5f3976"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d)+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme_minimal()+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        # legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Approval",labels = scales::percent_format(accuracy = 5L),breaks=seq(-0.9,0.9,0.05))+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(min(d$Date)-2,election),guide = guide_axis(angle = -90))+
  ggtitle('Yoon Suk Yeol Presidency Net Approval')
plotwiki
ggsave(plot=plotwiki, file="Korea/approval2.png",width = 15, height = 7.5, type = "cairo-png")