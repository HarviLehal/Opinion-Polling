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
library(dplyr)
library(ggbreak)

py_run_file("Europe/data.py")
poll <- read_csv("Europe/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
election<-as.Date("06 06 2024", "%d %m %Y")
old <-min(d$Date)
d<-d[d$Date<election+5,]
# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#b71c1c","#f0001c","#57b45f",
                                "#fed700","#3399ff","#196ca8",
                                "#0e408a","#000000","#999999"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election-38),guide = guide_axis(angle = -45))+
  scale_y_continuous(breaks=seq(0,200,20))
plot1


poll <- read_csv("Europe/poll.csv")
max <-max(d$Date)
poll<-poll[poll$Date<election+5,]
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
d1 <- round(colMeans(poll[-1],na.rm=TRUE), digits=0)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")

d2 <- reshape2::melt(d2, id.vars="Date")

d3<-rbind(d2,d1)


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#d47777","#b71c1c","#f66677","#f0001c","#9ad29f","#57b45f",
                               "#ffe766","#fed700","#85c2ff","#3399ff","#75a7cb","#196ca8",
                               "#6e8cb9","#0e408a","#666666","#000000","#c2c2c2","#999999"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=0, color="#FFFFFF",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2

plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Europe/plot.png",width = 15, height = 7.5, type = "cairo-png")
