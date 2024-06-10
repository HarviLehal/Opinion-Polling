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

poll <- read_csv("Italy/European/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.04)

election<-as.Date("09 06 2024", "%d %m %Y")
start<-as.Date("01 01 2024", "%d %m %Y")
old <-min(d$Date)
# LOESS GRAPH


# TRUE M5S COLOURS
plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,]) +
  scale_color_manual(values = c("#048404","#ef1c27","#f4c01a","#0484dc",
                                "#03386a","#bc3454","#b41317","#0039aa",
                                "#075271","#f6d025","#fcd404","#d4448c"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "4% Party Threshold", vjust = -1, hjust=0.5),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, linewidth=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.75)+
  scale_x_break(c(old+2, start+3))+
  scale_x_date(date_breaks = "1 week", date_labels =  "%d %b %Y",limits = c(old-2,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2024 European Election in Italy')

plot1



poll <- read_csv("Italy/European/poll2.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
Date <- c(max(poll$Date)-1)
poll<-poll[poll$Date>(max(poll$Date)-7),]
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
d2$value<-formattable::percent(d2$value, digits = 2)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 2)

d4<-rbind(d1,d2,d3)

d4<-d4[d4$variable!='IV',]
d4<-d4[d4$variable!='+E',]
d4<-droplevels(d4)


plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#048404","#68b568","#048404","#ef1c27","#f5777d","#ef1c27","#f4c01a","#f8d976","#f4c01a","#0484dc","#68b5ea","#0484dc",
                               "#03386a","#6888a6","#03386a","#bc3454","#d78598","#bc3454","#b41317","#d27174","#b41317","#0039aa","#6688cc","#0039aa",
                               "#075271","#6a97aa","#075271","#f6d025","#fae37c","#f6d025","#fcd404","#fde568","#fcd404","#d4448c","#e58fba","#d4448c"))+
  # geom_text(aes(label = ifelse(d4$Date == max(d4$Date),
  #                              ifelse(is.na(d4$value)==FALSE,paste(formattable::percent(d4$value)),""),
  #                              ifelse(is.na(d4$value)==FALSE,paste("(",formattable::percent(d4$value),")"),
                                      # ifelse(d4$variable=='SUE','(3.1% from E+)',"(New)"))),y = 0),
            # hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = formattable::percent(ifelse(d4$Date != min(d4$Date), d4$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),ifelse(is.na(d4$value)==TRUE,ifelse(d4$variable=='SUE','(3.1% from E+)',"(New)")
                                                              ,(paste("(",formattable::percent(d4$value,digits=1),")"))),""),y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 2024 Result \n 7 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d4$variable)))+
  coord_flip()

plot2

plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))

ggsave(plot=plot, file="Italy/European/plot2.png",width = 20, height = 7.5, type="cairo-png")
