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

py_run_file("Israel/data.py")
poll <- read_csv("Israel/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")

election<-as.Date("27 10 2026", "%d %m %Y")
old <-min(d$Date)
# d$value[is.na(d$value)]<-0
new<-d[d$variable!='Democrats'&d$variable!='New Hope',]
new2<-d[d$variable=='Democrats'|d$variable=='New Hope',]
new2<-new2[!is.na(new2$value),]
h<-3.25
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#1c5a9f","#1a3581","#ff4300",
                                "#00bce0","#0082b3","#032470",
                                "#003066","#9bc1e3","#0d7a3a",
                                "#d51f33","#ef1520","#1be263",
                                "#2d38cf","#f66004"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=new[new$Date!=old&new$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=new2[new2$Date!=old&new2$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        plot.caption = element_text(hjust = 0,face="italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  # scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_hline(aes(yintercept=h), alpha=0.75,linetype="dashed",colour="#000000")+
  geom_text(aes(election-2,h,label = "Party Threshold*", vjust = -1, hjust=1),colour="#000000", alpha=0.75,fontface="italic")+
  ylim(0,45)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Israeli General Election Seat Projection Since 2022') + 
  # labs(caption = "Labor-Meretz seats combined since 28 May 2024 for simplicity")
  labs(caption = "* Below 3.25% is represented as N%, above 3.25% is N Seats")
  
plot1

d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 14, Date), mean,na.rm=TRUE))

plot1a<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#1c5a9f","#1a3581","#ff4300",
                                "#00bce0","#0082b3","#032470",
                                "#003066","#9bc1e3","#0d7a3a",
                                "#d51f33","#ef1520","#1be263",
                                "#2d38cf","#f66004"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        plot.caption = element_text(hjust = 0,face="italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  # scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_hline(aes(yintercept=h), alpha=0.75,linetype="dashed",colour="#000000")+
  geom_text(aes(election-2,h,label = "Party Threshold*", vjust = -1, hjust=1),colour="#000000", alpha=0.75,fontface="italic")+
  ylim(0,45)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Israeli General Election Seat Projection Since 2022') + 
  # labs(caption = "Labor-Meretz seats combined since 28 May 2024 for simplicity")
  labs(caption = "* Below 3.25% is represented as N%, above 3.25% is N Seats")

plot1a

poll <- read_csv("Israel/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>=(max(poll$Date)-15),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value <-ifelse(d1$value<4,d1$value,round(d1$value, digits=0))

d2 <- reshape2::melt(d2, id.vars="Date")

d3<-rbind(d2,d1)

d3$value[is.na(d3$value)]<- 0

plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#779cc5","#1c5a9f","#7686b3","#1a3581","#ff8e66","#ff4300","#66d7ec","#00bce0",
                               "#66b4d1","#0082b3","#687ca9","#032470","#6683a3","#003066","#c3daee","#9bc1e3",
                               "#6eaf89","#0d7a3a","#e67985","#d51f33","#f57379","#ef1520","#76eea1","#1be263",
                               "#8188e2","#2d38cf","#faa068","#f66004"))+
  geom_text(aes(label = ifelse(d3$Date == max(d3$Date),
                               ifelse(d3$value>=4,paste(d3$value),
                                      ifelse(d3$variable=='Meretz'|d3$variable=='Labor','Merged into The Democrats',paste(round(d3$value,digits=2),"%"))),
                               ifelse(d3$value>=4,paste("(",d3$value,")"),
                                      ifelse(d3$variable=='New Hope','(Part of National Unity)',
                                             ifelse(d3$variable=='Democrats',"(Labor-Meretz Merger)",paste("(",round(d3$value,digits=2),"%",")"))))),
                y = 0),hjust=ifelse(is.na(d3$value)==TRUE,ifelse(d3$Date==max(d3$Date),ifelse(d3$value<10,ifelse(d3$value<4,-0.15,-1.1),-0.45),0),0), color="#000000",position = position_dodge(1), size=3.5, fontface=ifelse(d3$value<4,"bold.italic","bold"))+
  # geom_text(aes(label = ifelse(is.na(d3$value), "New", ""),y = 0),
  #           hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average \n (2022 Result)')+
  scale_x_discrete(limits = d3$variable[order(d1$value,na.last=FALSE)])+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot


ggsave(plot=plot, file="Israel/plot.png",width = 15, height = 7.5, type="cairo-png")

plot<-ggarrange(plot1a, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="Israel/plot2.png",width = 15, height = 7.5, type="cairo-png")
