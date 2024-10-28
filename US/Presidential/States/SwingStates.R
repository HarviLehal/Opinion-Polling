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

py_run_file("US/Presidential/States/data.py")
election<-as.Date("05 11 2024", "%d %m %Y")
old<-as.Date("21 07 2024", "%d %m %Y")

# Georgia
poll <- read_csv("US/Presidential/States/GA.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank(),
        axis.text.x.bottom=element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Georgia')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))

plot1


# Michigan
poll <- read_csv("US/Presidential/States/MI.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_blank(),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank(),
        axis.text.x.bottom=element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Michigan')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))
plot2


# North Carolina
poll <- read_csv("US/Presidential/States/NC.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#e81b23","#0042ca","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank(),
        axis.text.x.bottom=element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('North Carolina')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))
plot3


# Nevada
poll <- read_csv("US/Presidential/States/NV.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot4<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_blank(),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank(),
        axis.text.x.bottom=element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Nevada')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))
plot4


# Pennsylvania
poll <- read_csv("US/Presidential/States/PA.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot5<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank(),
        axis.text.x.bottom=element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Pennsylvania')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))
plot5


# Wisconsin
poll <- read_csv("US/Presidential/States/WI.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot6<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_blank(),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank(),
        axis.text.x.bottom=element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Wisconsin')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))
plot6


# Arizona
poll <- read_csv("US/Presidential/States/AZ.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot7<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#0042ca","#e81b23","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Arizona')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))
plot7


# Florida
poll <- read_csv("US/Presidential/States/FL.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

plot8<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#e81b23","#0042ca","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_blank(),
        plot.title = element_text(face="bold",hjust = 0.5,size=20),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 1L),breaks=seq(0.42,0.58,0.02))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0.42), alpha=0)+
  geom_hline(aes(yintercept=0.58), alpha=0)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Florida')+
  # if the 7 day average for Harris is higher than Trump, then change background to blue
  theme(panel.background = element_rect(fill = ifelse(colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Harris"] > colMeans(poll[poll$Date > max(poll$Date) - 6,][-1])["Trump"], "#b0ceff", "#ffb6b6")))
plot8


plot<-ggarrange(plot1,plot2,plot3,plot4,plot5,plot6,plot7,plot8,ncol = 2, nrow = 4)
plot


ggsave(plot=plot, file="US/Presidential/States/States.png",width = 20, height = 15, type="cairo-png")

