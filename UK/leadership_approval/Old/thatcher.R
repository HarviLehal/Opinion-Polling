library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(ggpubr)
library(zoo)
library(dplyr)

poll <- read_csv("UK/leadership_approval/Old/thatcher_adjusted.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
old<-min(d$Date)
elect<-as.Date("03 04 1979", "%d %m %Y")
elect2<-elect+(Sys.Date()-as.Date("04 07 2024", "%d %m %Y"))
election<-max(d$Date)+14
f<-0.75



plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#33a22b","#c70000"
  ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.8,0.05))+
  geom_hline(aes(yintercept=0.5), alpha=0.5, linewidth=1, linetype="dashed", colour="#000000")+
  geom_vline(xintercept=elect, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=elect2, linetype="solid", color = "#000000", alpha=0.75, size=0.75)+
  geom_text(aes(elect2,f,label = "Current Point", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  geom_text(aes(elect,f,label = "Election", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  scale_x_date(date_breaks = "2 months", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  geom_hline(yintercept = 0, size = 1, colour="#333333",alpha=0)+
  geom_hline(yintercept = 0.8, size = 1, colour="#333333",alpha=0)+
  ggtitle('Margret Thatcher Approval Rating')


plot1


ggsave(plot=plot1, file="UK/leadership_approval/Old/Thatcher.png",width = 20, height = 7.5, type = "cairo-png")
