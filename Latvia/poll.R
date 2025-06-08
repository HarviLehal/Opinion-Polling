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
py_run_file("Latvia/data.py")
poll <- read_csv("Latvia/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)

election<-as.Date("03 10 2026", "%d %m %Y")
old <-min(d$Date)
# LOESS GRAPH

parties<-d[d$variable!='AP!',]
AP<-d[d$variable=='AP!',]
AP<-AP[!is.na(AP$value),]

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#6ab647","#02723a","#ffac01","#932330",
                                "#f08418","#a8343c","#e64632","#fff200",
                                "#ffdd00","#ee222b","#1aa28e","#3560a9",
                                "#6767ab","#284470","#ffec00"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=AP[AP$Date!=old&AP$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=parties[parties$Date!=old&parties$Date!=election,])+
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
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_text(aes(election,h,label = "5% Party Threshold", vjust = -0.6, hjust=1.05),colour="#000000",fontface="italic")+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Latvian Parliamentary Election')
plot1


poll <- read_csv("Latvia/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
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
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d1<-d1[d1$variable!='AP!',]
d2<-d2[d2$variable!='AP!',]
d1<-droplevels(d1)
d2<-droplevels(d2)
# d3<-rbind(d2,d1)
d2$value<-ifelse(is.nan(d2$value)==TRUE,NA,d2$value)
d2$value<-ifelse(is.na(d2$value)==TRUE,0.0000000001,d2$value)
d4<-rbind(d1,d2,d3)
d4<-rbind(d1,d2)




plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#a1d68d","#6ab647",
                               "#26986c","#02723a",
                               "#ffcd66","#ffac01",
                               "#b95c5d","#932330",
                               "#f5b86c","#f08418",
                               "#c96469","#a8343c",
                               "#f37a66","#e64632",
                               "#fff799","#fff200",
                               "#ffe766","#ffdd00",
                               "#f06870","#ee222b",
                               "#66c4b3","#1aa28e",
                               "#7293d0","#3560a9",
                               "#a1a1d6","#6767ab",
                               "#5f709e","#284470",
                               "#fff799","#ffec00"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               ifelse(is.na(d4$value)==F,
                                      ifelse(d4$Date == max(d4$Date),
                                             paste(formattable::percent(d4$value, digits = 2)),
                                             paste(formattable::percent(d4$value, digits = 1))),""), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                                      ifelse(d4$value==0.0000000001,paste("(Part of AP!:",formattable::percent(0.0496, digits = 2),")"),
                                             paste("(",formattable::percent(d4$value, digits = 2),")")),""),
                y = 0),hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold"),
        plot.caption = element_text(hjust = 0,face="bold.italic"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' Latest Poll <br> *(2022 Election)*')+
  # scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  scale_x_discrete(limits = d4$variable[order(d1$value,na.last = FALSE)])+
  coord_flip()

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Latvia/plot.png",width = 15, height = 7.5, type="cairo-png")

