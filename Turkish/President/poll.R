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

py_run_file("Turkish/President/data.py")
poll <- read_csv("Turkish/President/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h<-0.5

election<-as.Date("07 05 2028", "%d %m %Y")
start <- as.Date("17 08 2024", "%d %m %Y")

old <-min(d$Date)


# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#FFCC00","#ed1c24","#951b88","#007d60","#404040"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.6,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  scale_x_break(c(old+20, start))+
  scale_x_date(date_breaks = "2 months", date_labels =  "%b %Y",limits = c(old-20,election),guide = guide_axis(angle = -90))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.8,0.05))+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  ggtitle('Opinion Polling for the 2028 Turkish Presidential Election')
plot1


poll <- read_csv("Turkish/President/poll.csv")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-8),]
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
  scale_fill_manual(values = c("#ffe066","#FFCC00",
                               "#f4777c","#ed1c24",
                               "#bf76b8","#951b88",
                               "#66b1a0","#007d60",
                               "#8c8c8c","#404040"
  ))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               ifelse(d4$Date == max(d4$Date),
                                      paste(formattable::percent(d4$value, digits = 2)),
                                      paste(formattable::percent(d4$value, digits = 1))), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),ifelse(is.na(d4$value)==FALSE,
                                                              paste("(",formattable::percent(d4$value, digits = 2),")"),ifelse(d4$variable=='Erbakan YRP',paste("( Endorsed ",names(poll)[2],")"),"( Endorsed Kılıçdaroğlu CHP )")),""),
                y = 0),hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",
        axis.title=element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold",lineheight = 1.5),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 Day Average <br> *(2023 Results)*')+
  # scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  scale_x_discrete(limits = d4$variable[order(d1$value,na.last=FALSE)],labels = label_wrap(8))+
  coord_flip()
plot2



plot<-aplot::plot_list(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot


ggsave(plot=plot, file="Turkish/President/plot.png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot, file="Turkish/President/plot.svg",width = 15, height = 7.5)
aaa=readLines("Turkish/President/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Turkish/President/plot.svg")
