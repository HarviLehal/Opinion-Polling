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

py_run_file("Irish/data.py")
poll <- read_csv("Irish/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("20 02 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#39675F","#74BC64","#729AFF","#45AD6E", "#C11112", "#712C8D","#87221E","#445225"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d[d$Date!=old,])+
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
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Irish General Election')
plot1

# d <- d %>%
#   group_by(variable) %>%
#   arrange(Date) %>%
#   mutate(Moving_Average = zoo::rollmean(value, k = 7, fill = NA, align = "right"))
d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 30, Date), mean,na.rm=TRUE))

plot1a<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#39675F","#74BC64","#729AFF","#45AD6E", "#C11112", "#712C8D","#87221E","#445225"))+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Irish General Election')
plot1a


poll <- read_csv("Irish/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
d1 <- colMeans(poll[-1],na.rm = TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)

plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#88a49f","#39675F","#acd7a2","#74BC64",
                               "#aac2ff","#729AFF","#8fcea8","#45AD6E",
                               "#da7071","#C11112","#aa80bb","#712C8D",
                               "#b77a78","#87221E","#8f977c","#445225"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),
                y = 0),hjust=ifelse(d3$value<0.1,-0.35,-0.25), color="#000000",position = position_dodge(0.8), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(0.8), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold"),
        plot.caption = element_text(hjust = 0,face="bold.italic"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average <br> *(2020 Result)*')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Irish/plot.png",width = 15, height = 7.5,type="cairo-png")
plot<-ggarrange(plot1a, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Irish/plot2.png",width = 15, height = 7.5,type="cairo-png")
