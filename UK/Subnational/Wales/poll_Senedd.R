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
library(ggbreak)

py_run_file("UK/Subnational/Wales/data2.py")
poll <- read_csv("UK/Subnational/Wales/poll_Senedd.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
old<-as.Date("06 05 2021", "%d %m %Y")
election<-as.Date("07 05 2026", "%d %m %Y")
reform<-as.Date("08 05 2024", "%d %m %Y")

f<-formattable::percent(0.6)


# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,],alpha=0.5) +
  scale_color_manual(values = c("#E4003B","#0087DC","#1e5b53",
                                "#528D6B","#FAA61A","#800001","#12B6CF"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=d[d$Date!=old,])+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old-0.5,election),guide = guide_axis(angle = -90))+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=reform, linetype="dashed", color = "#000000", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(yintercept = 0, size = 1, colour="#333333",alpha=0)+
  ggtitle('Opinion Polling for the Next Senedd Election')
plot1

# BAR CHART

poll <- read_csv("UK/Subnational/Wales/poll_Senedd.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
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
  scale_fill_manual(values = c("#f27999","#E4003B","#77c0ed","#0087DC","#74b0a9","#1e5b53",
                               "#9dc7af","#528D6B","#fcd38b","#FAA61A","#bf6069","#800001",
                               "#80dae8","#12B6CF"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=-0.35, vjust = 0, color="#000000",position = position_dodge(0.7), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),y = 0),
            hjust=-0.1, vjust = 0, color="#404040", position = position_dodge(1.1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 30 day average \n (2021 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="UK/Subnational/Wales/plot_Senedd.png",width = 15, height = 7.5, type="cairo-png")