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

py_run_file("Slovak/Seats/data.py")
poll <- read_csv("Slovak/Seats/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
election<-as.Date("31 12 2028", "%d %m %Y")
old <-min(d$Date)


d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 30, Date), mean,na.rm=TRUE))

d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=2, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=FALSE, fill=NA, align="right"))
# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#D82222","#00BDFF","#81163B",
                                "#BED62F","#FFE17C","#78fc04",
                                "#173A70","#e4010a","#f48c1f","#4D0E90"))+
  # geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d[d$Date!=old,])+
  stat_smooth(fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d[d$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Seats",breaks=seq(0,50,5))+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Seat Projection for the Next Slovak Parliamentary Election')
plot


poll <- read_csv("Slovak/Seats/poll.csv")
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


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#e87a7a","#D82222",
                               "#66d7ff","#00BDFF",
                               "#b37389","#81163B",
                               "#d8e682","#BED62F",
                               "#ffedb0","#FFE17C",
                               "#aefd68","#78fc04",
                               "#7489a9","#173A70",
                               "#ef676c","#e4010a",
                               "#f8ba79","#f48c1f",
                               "#946ebc","#4D0E90"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        plot.caption = element_text(hjust = 0,face="italic"))+
  ggtitle(' 14 day average \n (2023 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()+
  labs(caption = "* Government Parties (Smer-Hlas-SNS)")
plot2


plotA<-ggarrange(plot, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA

ggsave(plot=plotA, file="Slovak/Seats/plot.png",width = 15, height = 7.5, type="cairo-png")
