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
py_run_file("Polish/President/data.py")
poll <- read_csv("Polish/President/poll_new.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

old<-min(d$Date)
election<-as.Date("18 05 2025", "%d %m %Y")
# election<-max(d$Date)+14

# MAIN GRAPH

colss <-c(
          "Nawrocki"   ="#263778",
          "Trzaskowski"="#F68F2D",
          "Hołownia"   ="#F9C013",
          "Biejat"     ="#eb2a48",
          "Zandberg"   ="#ac145a",
          "Mentzen"    ="#717d90",
          "Braun"      ="#d4aa00",
          "Jakubiak"   ="#1b2d7f",
          # "Woch"       ="#e6001a",
          # "Szumlewicz" ="#c99999",
          "Stanowski"  ="#99c9c9")

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1.5, data=d[d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = colss)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold.italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(aes(yintercept=0), alpha=0, linetype="longdash", colour="#000000")+
  scale_x_date(date_breaks = "1 week", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2025 Polish Presidential Election')
plot1



poll <- read_csv("Polish/President/poll_new.csv")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==max(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-5),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d2 <- colMeans(d2[-1],na.rm=TRUE)
d2 <- as.data.frame(d2)
d2 <- t(d2)
Date <- c(election)
d2 <- cbind(Date, d2)
d2 <- as.data.frame(d2)
d1$Date <- as.Date(d1$Date)
d2$Date <- as.Date(d2$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)
d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 2)
d4<-rbind(d1,d2)


plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#7d87ae","#263778",
                               "#fabc81","#F68F2D",
                               "#fbd971","#F9C013",
                               "#f37f91","#eb2a48",
                               "#cd729c","#ac145a",
                               "#aab1bc","#717d90",
                               "#e5cc66","#d4aa00",
                               "#7681b2","#1b2d7f",
                               "#c2dfdf","#99c9c9"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               ifelse(d4$Date == max(d4$Date),
                                      paste(formattable::percent(d4$value, digits = 2)),
                                      paste(formattable::percent(d4$value, digits = 1))), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               paste("(",formattable::percent(d4$value, digits = 1),")"),""),
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
  ggtitle(' Result <br> 5 Day Average')+
  scale_x_discrete(limits = d4$variable[order(d1$value,d2$value,na.last = FALSE)])+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Polish/President/plot_new.png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot, file="Polish/President/plot2.svg",width = 15, height = 7.5)
aaa=readLines("Polish/President/plot2.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Polish/President/plot2.svg")