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
poll <- read_csv("US/old/poll2.csv")
poll<-poll[poll$Date!=max(poll$Date),]
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("03 11 2020", "%d %m %Y")
old <-min(d$Date)
# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d[d$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.75)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.75)+
  scale_x_date(date_breaks = "1 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -45))+
  ggtitle('2020 US Presidential Polling (Excluding Undecided/Other)')
plot1

ggsave(plot=plot1, file="US/old/plot.png",width = 15, height = 7.5, type="cairo-png")

