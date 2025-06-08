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
library(dplyr)
library(ggbreak)

py_run_file("Dutch/data_new.py")
poll <- read_csv("Dutch/poll_new.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
election<-as.Date("29 10 2025", "%d %m %Y")
old <-min(d$Date)

z <- d[d$Date!=old,]

z<- z %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 14, Date), mean,na.rm=TRUE))
# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#0E2758","#cc1d1d","#222ACA",
                                "#f0c400","#3DAD3E","#99C11A",
                                "#53C74A","#E81718","#45B6B1",
                                "#226B26","#7C1B1C","#DD601C",
                                "#43A6EB","#552C83","#262B57"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d[d$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold",color="#000000"),
        axis.text.y = element_text(face="bold",color="#000000"),
        plot.title = element_text(face="bold",color="#000000"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  xlim(min(d$Date), max)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "1 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Dutch Parliamentary Election')
  plot1

# MA GRAPH

plot2<-ggplot(data=z,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#0E2758","#cc1d1d","#222ACA",
                                "#f0c400","#3DAD3E","#99C11A",
                                "#53C74A","#E81718","#45B6B1",
                                "#226B26","#7C1B1C","#DD601C",
                                "#43A6EB","#552C83","#262B57"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold",color="#000000"),
        axis.text.y = element_text(face="bold",color="#000000"),
        plot.title = element_text(face="bold",color="#000000"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  xlim(min(d$Date), max)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "1 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Dutch Parliamentary Election')
plot2
# BAR CHART

poll <- read_csv("Dutch/poll_new.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
d1 <- round(colMeans(poll[-1],na.rm=TRUE), digits=0)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")

d2 <- reshape2::melt(d2, id.vars="Date")

d3<-rbind(d2,d1)


plot3<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#6e7d9b","#0E2758","#e07777","#cc1d1d","#7a7fdf","#222ACA",
                               "#f6dc66","#f0c400","#8bce8b","#3DAD3E","#c2da76","#99C11A",
                               "#98dd92","#53C74A","#f17474","#E81718","#8fd3d0","#45B6B1",
                               "#7aa67d","#226B26","#b07677","#7C1B1C","#eba077","#DD601C",
                               "#8ecaf3","#43A6EB","#9980b5","#552C83","#7d809a","#262B57"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=ifelse(d3$value<10,-1.45,-0.45), color="#000000",position = position_dodge(0.8), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=-0.1, color="#000000", position = position_dodge(0.8), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day average \n (2023 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot3


plotA<-ggarrange(plot1, plot3,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA

plotB<-ggarrange(plot2, plot3,ncol = 2, nrow = 1,widths=c(2,0.5))
plotB



ggsave(plot=plotA, file="Dutch/plot.png",width = 20, height = 10, type="cairo-png")

ggsave(plot=plotB, file="Dutch/plot_ma.png",width = 20, height = 10, type="cairo-png")

# EXTRA GRAPHIEK


d1$value<-ifelse(is.na(d1$value)==TRUE,0,d1$value)
d2$value<-ifelse(is.na(d2$value)==TRUE,0,d2$value)
d1$value<-d1$value/sum(d1$value,na.rm=TRUE)
d2$value<-d2$value/sum(d2$value,na.rm=TRUE)
d1$Date<-'14 Day Average'
d2$Date<-'2023 Result'

ordered<-c('SP','PvdD','PvdA-GL','DENK','D66','Volt','CU','CDA','NSC','VVD','BBB','PVV','SGP','FvD','JA21')

d1<-d1 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d2<-d2 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d3<-rbind(d1,d2)


plot3a<-ggplot(d3, aes(fill=interaction(rev(Date),variable), y=value, x=Date,label=round(value*150))) + 
  scale_fill_manual(values = c("#f17474","#E81718","#7aa67d","#226B26","#e07777","#cc1d1d",
                               "#8fd3d0","#45B6B1","#8bce8b","#3DAD3E","#9980b5","#552C83",
                               "#8ecaf3","#43A6EB","#98dd92","#53C74A","#f6dc66","#f0c400",
                               "#7a7fdf","#222ACA","#c2da76","#99C11A","#6e7d9b","#0E2758",
                               "#eba077","#DD601C","#b07677","#7C1B1C","#7d809a","#262B57"))+
  geom_bar(position="fill", stat="identity")+
  geom_text(data=subset(d3,value != 0),size = 5.5, position = position_stack(vjust = 0.5),fontface=ifelse(d3$Date=='2023 Result',"bold.italic","bold"),color="#FFFFFF")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold",color="#000000",size=10),
        axis.text.y = element_text(face="bold.italic",size=15,color="#000000",hjust=1),
        # axis.text.y = element_blank(),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=0.5,alpha=0.25) +
  scale_x_discrete(limits=rev)+
  coord_flip()
plot3a

plot<-ggarrange(plot1, plot3a,ncol = 1, nrow = 2,heights=c(2,0.3))
plot

ggsave(plot=plot, file="Dutch/plot_bar.png",width = 20, height = 10, type="cairo-png")

