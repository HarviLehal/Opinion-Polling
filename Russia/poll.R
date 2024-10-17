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

py_run_file("Russia/data.py")
poll <- read_csv("Russia/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
# d$value[is.na(d$value)] <- 0
d$value<-formattable::percent(d$value)
old<-as.Date("19 09 2021", "%d %m %Y")
election<-as.Date("20 09 2026", "%d %m %Y")
president<-as.Date("17 03 2024", "%d %m %Y")
war<-as.Date("24 02 2022", "%d %m %Y")

f<-formattable::percent(1)
g<-formattable::percent(0.55)
h <- formattable::percent(0.05)

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#2056ae","#cc1111","#4488cc","#ffc003","#0ad1c9"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d)+
  # geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=president, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=war, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_text(aes(president,f,label = "Presidential Election", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  geom_text(aes(war,f,label = "Invasion of Ukraine", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  geom_hline(aes(yintercept=h), alpha=0.75,linetype="dashed",colour="#000000")+
  geom_text(aes(election-14,h,label = "5% Party Threshold", vjust = -1, hjust=1),colour="#000000", alpha=0.75, fontface="italic")+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 months", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  geom_hline(yintercept = 0, size = 1, colour="#333333",alpha=0)+
  ggtitle('Opinion Polling for the Next Russian Legislative "Election"')+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])


plot1

# BAR CHART!!

poll <- read_csv("Russia/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
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
  scale_fill_manual(values = c("#799ace","#2056ae","#e07070","#cc1111","#8fb8e0","#4488cc",
                               "#ffd968","#ffc003","#6ce3df","#0ad1c9"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=-0.4, vjust = 0, color="#000000",position = position_dodge(0.7), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),y = 0),
            hjust=-0.15, vjust = 0, color="#000000", position = position_dodge(1.1), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average \n (2021 "Result")')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
ggsave(plot=plot, file="Russia/plot.png",width = 20, height = 7.5, type = "cairo-png")
