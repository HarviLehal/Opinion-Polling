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
poll <- read_csv("Spain/Catalunya/seats3.csv")
d <- reshape2::melt(poll, id.vars="Date")

election<-as.Date("12 05 2024", "%d %m %Y")
old <-min(d$Date)
# LOESS GRAPH
start<-as.Date("13 03 2024", "%d %m %Y")
d<-d[d$Date>start,]

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#d74930","#ffdb00","#054a81",
                                "#c31530","#7f2a52","#1d84ce"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot1

d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 5, Date), mean,na.rm=TRUE))

plot1a<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#d74930","#ffdb00","#054a81",
                                "#c31530","#7f2a52","#1d84ce"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot1a

poll <- read_csv("Spain/Catalunya/seats3.csv")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-4),]
d1 <- round(colMeans(poll[-1],na.rm=TRUE), digits=0)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)
d3 <- as.data.frame(d3)

d1 <- reshape2::melt(d1, id.vars="Date")

d2 <- reshape2::melt(d2, id.vars="Date")

d3 <- reshape2::melt(d3, id.vars="Date")
d4<-rbind(d1,d2,d3)

hx<-67

plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#ac3a26","#e79283","#d74930",
                               "#ccaf00","#ffe966","#ffdb00",
                               "#043b67","#6992b3","#054a81",
                               "#9c1126","#db7383","#c31530",
                               "#662242","#b27f97","#7f2a52",
                               "#176aa5","#61a9dd","#1d84ce"))+
  geom_text(aes(label = d4$value,y = 0),hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(is.na(d4$value), "Not Contested", ""),y = 0),hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' Results \n Average (After Legal Ban) \n (2021 Result)')+
  geom_hline(aes(yintercept=hx), alpha=0.75, linetype="longdash", colour="#000000")+
  scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(16))+
  coord_flip()
plot2

  
plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="Spain/Catalunya/seats_coalitions.png",width = 15, height = 7.5, type="cairo-png")

plot<-ggarrange(plot1a, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="Spain/Catalunya/seats_coalitions_ma.png",width = 15, height = 7.5, type="cairo-png")