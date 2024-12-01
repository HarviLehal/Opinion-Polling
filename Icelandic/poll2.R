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
library(ggbreak)

poll <- read_csv("Icelandic/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("30 Nov 2024", "%d %b %Y")
start <- as.Date("02 Oct 2024", "%d %b %Y")

old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#41A4DB","#A2D150","#6D9B3F",
                                "#EC3E48","#F8CB3C","#790581",
                                "#EDA823","#3B8F93","#F13A52"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.225,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_break(c(old+1, start))+
  scale_x_date(date_breaks = "2 days", date_labels =  "%d %b %Y",limits = c(old-1,election),guide = guide_axis(angle = -90))+
  ggtitle('Campaign Period Polling for the 2024 Icelandic general election')

plot1

poll <- read_csv("Icelandic/poll.csv")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-5),]
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


plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#b3dbf1","#8dc8e9","#41A4DB",
                               "#daedb9","#c7e396","#A2D150",
                               "#c5d7b2","#a7c38c","#6D9B3F",
                               "#f7b2b6","#f48b91","#EC3E48",
                               "#fceab1","#fbe08a","#F8CB3C",
                               "#c99bcd","#af69b3","#790581",
                               "#f8dca7","#f4cb7b","#EDA823",
                               "#b1d2d4","#89bcbe","#3B8F93",
                               "#f9b0ba","#f78997","#F13A52"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),ifelse(d4$Date == max(d4$Date),ifelse(d4$variable=='BCU',paste(''),paste(formattable::percent(d4$value, digits = 2))),ifelse(d4$variable=='BCU',paste('Campaign Suspended'),paste(formattable::percent(d4$value, digits = 1)))), ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               ifelse(is.na(d4$value)==TRUE,"(New)",
                                      (paste("(",formattable::percent(d4$value, digits = 1),")"))),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('2024 Results <br> 7 Day Average <br> *(2021 Results)*')+
  scale_x_discrete(limits = d4$variable[order(d1$value,na.last = FALSE)])+

  coord_flip()


plot<-aplot::plot_list(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Icelandic/plot_short.png",width = 15, height = 7.5, type="cairo-png")