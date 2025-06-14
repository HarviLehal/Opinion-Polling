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
py_run_file("Canada/Provincial/British Columbia/data.py")
poll <- read_csv("Canada/Provincial/British Columbia/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("21 10 2028", "%d %m %Y")
old <-min(d$Date)

parties<-d[d$variable!='OneBC'&d$variable!='CentreBC',]
kass<-d[d$variable=='OneBC'|d$variable=='CentreBC',]
kass<-kass[!is.na(kass$value),]
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1.5, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#EF7B00","#00529F","#3D9F3B","#c49b50","#ee2d30","#aaaaaa"
                                ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=2,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=kass[kass$Date!=old&kass$Date!=election,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=parties[parties$Date!=old&parties$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold.italic",lineheight = 1.5),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 44<sup>th</sup> British Columbia general election')

plot1
poll <- read_csv("Canada/Provincial/British Columbia/poll.csv")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-30),]
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
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d4<-rbind(d1,d2,d3)
d4<-rbind(d1,d2)


plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#f9ca99","#f5b066","#EF7B00",
                               "#9ab4f2","#6F94ED","#00529F",
                               "#b1d9b1","#8bc589","#3D9F3B",
                               "#dddddd","#cccccc","#aaaaaa"))+
  scale_fill_manual(values = c("#f5b066","#EF7B00",
                               "#6F94ED","#00529F",
                               "#8bc589","#3D9F3B",
                               "#dcc396","#c49b50",
                               "#f58183","#ee2d30",
                               "#cccccc","#aaaaaa"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               paste(formattable::percent(d4$value, digits = 1)), ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               ifelse(is.na(d4$value)==TRUE,"(New)",
                                      (paste("(",formattable::percent(d4$value, digits = 1),")"))),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",
        axis.title=element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold",lineheight = 1.5),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('30 day Average <br> *(2024 Election)*')+
  scale_x_discrete(limits = d4$variable[order(d3$value,na.last = FALSE)])+
  coord_flip()

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Canada/Provincial/British Columbia/plot.png",width = 15, height = 7.5, type="cairo-png")
ggsave(plot=plot, file="Canada/Provincial/British Columbia/plot.svg",width = 15, height = 7.5)
aaa=readLines("Canada/Provincial/British Columbia/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Canada/Provincial/British Columbia/plot.svg")