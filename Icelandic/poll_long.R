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

poll1 <- read_csv("Icelandic/old/poll.csv")
poll2 <- read_csv("Icelandic/poll.csv")
poll<-dplyr::bind_rows(poll1,poll2)
# poll <- rbind(poll1,poll2) 
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("30 11 2024", "%d %m %Y")
next_election<-as.Date("30 11 2028", "%d %m %Y")
old_election <-min(d$Date)
h <- formattable::percent(0.05)

d_old <- reshape2::melt(poll1, id.vars="Date")
d_new <- reshape2::melt(poll2, id.vars="Date")
d_old$value<-as.numeric(d_old$value)/100
d_old$value<-formattable::percent(d_old$value)
d_new$value<-as.numeric(d_new$value)/100
d_new$value<-formattable::percent(d_new$value)
colss <-c("S"="#EC3E48",
          "D"="#41A4DB",
          "C"="#EDA823",
          "F"="#F8CB3C",
          "M"="#3B8F93",
          "B"="#A2D150",
          "J"="#F13A52",
          "P"="#790581",
          "V"="#6D9B3F"
)
# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old_election|d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = colss)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d_old[d_old$Date!=election&d_old$Date!=old_election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d_new[d_new$Date!=election&d_new$Date!=old_election,])+
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
  geom_vline(xintercept=old_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), next_election)+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_text(aes(election-50,h,label = "5% Party Threshold", vjust = -0.5, hjust=1),colour="#000000", fontface="italic", alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(min(d$Date),next_election),guide = guide_axis(angle = -90))+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5.25, shape=5, alpha=1)
plot1

poll <- read_csv("Icelandic/poll.csv")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-31),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)
d3 <- as.data.frame(d3)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 2)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d4<-rbind(d1,d2,d3)
d4<-rbind(d1,d2)


plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  # scale_fill_manual(values = c("#b3dbf1","#8dc8e9","#41A4DB",
  #                              "#daedb9","#c7e396","#A2D150",
  #                              "#c5d7b2","#a7c38c","#6D9B3F",
  #                              "#f7b2b6","#f48b91","#EC3E48",
  #                              "#fceab1","#fbe08a","#F8CB3C",
  #                              "#c99bcd","#af69b3","#790581",
  #                              "#f8dca7","#f4cb7b","#EDA823",
  #                              "#b1d2d4","#89bcbe","#3B8F93",
  #                              "#f9b0ba","#f78997","#F13A52"))+
  scale_fill_manual(values = c("#f48b91","#EC3E48",
                               "#8dc8e9","#41A4DB",
                               "#f4cb7b","#EDA823",
                               "#fbe08a","#F8CB3C",
                               "#89bcbe","#3B8F93",
                               "#c7e396","#A2D150",
                               "#f78997","#F13A52",
                               "#af69b3","#790581",
                               "#a7c38c","#6D9B3F"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               ifelse(d4$Date == max(d4$Date),
                                      paste(formattable::percent(d4$value, digits = 2)),
                                      paste(formattable::percent(d4$value, digits = 1))), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               paste("(",formattable::percent(d4$value, digits = 2),")"),""),
                y = 0),hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",
        axis.title=element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold",lineheight = 1.5),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 30 Day Average <br> *(2024 Results)*')+
  # scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  scale_x_discrete(limits = d4$variable[order(d3$value,na.last=FALSE)],labels = label_wrap(8))+
  coord_flip()
plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot


ggsave(plot=plot, file="Icelandic/plot_long.png",width = 15, height = 7.5, type="cairo-png")
