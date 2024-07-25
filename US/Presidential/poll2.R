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

poll <- read_csv("US/Presidential/poll2.csv")
# poll<-poll[poll$Date!=max(poll$Date),]
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("05 11 2024", "%d %m %Y")
old <-min(d$Date)
f<-formattable::percent(0.6)
begin<-as.Date("21 07 2024", "%d %m %Y")
# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.275,linewidth=0.75, data=d[d$Date!=old,])+
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
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=begin, linetype="dashed", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_text(aes(begin,f,label = "Biden Drops Out", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.75)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.75)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election-50),guide = guide_axis(angle = -45))+
  ggtitle('2024 US Presidential Polling (Excluding Undecided/Other)')
plot1

old2<-as.Date("28 06 2024", "%d %m %Y")
d2<-d[d$Date>old2|d$Date==old,]

d2<- d2 %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 7, Date), mean))

begin<-as.Date("21 07 2024", "%d %m %Y")
plot1a<-ggplot(data=d2,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d2[d2$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.8,linewidth=1, data=d2[d2$Date!=old,])+
  
  geom_line(aes(y = Moving_Average), linetype = "dashed",linewidth=1.5,alpha=0.35)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        plot.caption = element_text(hjust = 0,face="italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=begin, linetype="dashed", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_text(aes(begin,f,label = "Biden Drops Out", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  geom_point(data=d2[d2$Date==old,],size=5, shape=18, alpha=0.75)+
  geom_point(data=d2[d2$Date==old,],size=5.25, shape=5, alpha=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  scale_x_break(c(old+1.5, old2))+
  scale_x_date(date_breaks = "4 day", date_labels =  "%d %b %Y",limits = c(old-1.5,election),guide = guide_axis(angle = -90))+
  ggtitle('2024 US Presidential Polling (Excluding Undecided/Other)*')+
  labs(caption = "*LOESS regression solid line, 7-day Moving average dashed line")
plot1a

# MA GRAPH

# d <- d %>%
#   group_by(variable) %>%
#   arrange(Date) %>%
#   mutate(Moving_Average = zoo::rollmean(value, k = 7, fill = NA, align = "left"))

d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 7, Date), mean))



plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
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
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.75)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.75)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election-50),guide = guide_axis(angle = -45))+
  ggtitle('2024 US Presidential Polling (Excluding Undecided/Other)')
plot3


# BAR CHART

poll <- read_csv("US/Presidential/poll2.csv")
# poll<-poll[poll$Date!=max(poll$Date),]
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 2)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 2)

d3<-rbind(d2,d1)



plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#b0ceff","#0042ca",
                               "#ffb6b6","#e81b23"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, vjust = 0, color="#000000",position = position_dodge(0.7), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),ifelse(d3$variable=='Harris',paste("(",d3$value,")*"),paste("(",d3$value,")")),""),y = 0),
            hjust=0, vjust = 0, color="#404040", position = position_dodge(1.1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        plot.caption = element_text(hjust = 0,face="italic"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 7 day Average \n (2020 Election)')+
  scale_x_discrete(limits = rev(levels(d3$variable)),labels = label_wrap(8))+
  coord_flip()+
  labs(caption = "*Result for Biden in 2020")


plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="US/Presidential/plot_decided.png",width = 15, height = 7.5, type="cairo-png")


ggsave(plot=plot1a, file="US/Presidential/plot_decided_comparison.png",width = 15, height = 7.5, type="cairo-png")

plot<-ggarrange(plot3, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="US/Presidential/plot_decided_ma.png",width = 15, height = 7.5, type="cairo-png")
