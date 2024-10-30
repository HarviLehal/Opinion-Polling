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

py_run_file("Japan/seats/data.py")
poll <- read_csv("Japan/seats/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
# d$value[is.na(d$value)] <- 0
d$value<-formattable::percent(d$value)
start<-as.Date("1 10 2024", "%d %m %Y")
old<-min(d$Date)
election<-as.Date("27 10 2024", "%d %m %Y")
f<-formattable::percent(0.6)

d<-d[d$Date>start|d$Date==old,]

# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d[d$Date!=old,],aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#3ca324","#184589","#b8ce43","#f95580","#db001c",
                                "#ffba00","#ed008c","#ed7301","#1ca9e9","#0b80db","#aaaaaa"
  ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  scale_y_continuous(breaks=seq(0,300,10))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_hline(aes(yintercept=233), alpha=1)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_break(c(old+0.5, start+1))+
  scale_x_date(date_breaks = "2 day", date_labels =  "%d %b %Y",limits = c(old-1,election),guide = guide_axis(angle = -90))+
  ggtitle('Seat Projection for the 2024 Japanese General election (Excluding No Party and Undecided)')
plot1 


poll <- read_csv("Japan/seats/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-1),]
d1 <- round(colMeans(poll[-1],na.rm=TRUE),digits=0)
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
  scale_fill_manual(values = c("#77bf66","#3ca324","#748fb8","#184589",
                               "#d4e28e","#b8ce43","#fb99b3","#f95580",
                               "#e96677","#db001c","#ffd666","#ffba00",
                               "#f466ba","#ed008c","#f4ab67","#ed7301",
                               "#77cbf2","#1ca9e9","#6db3e9","#0b80db","#cccccc","#aaaaaa"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date),
                               ifelse(is.nan(d3$value)==TRUE,"",
                                      (paste(d3$value))),""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),
                               ifelse(is.na(d3$value)==TRUE,"(New)",
                                      (paste("(",d3$value,")"))),""),y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 7 day Average \n (2021 Election)')+
  scale_x_discrete(limits = rev(levels(d3$variable)),labels = label_wrap(8))+
  coord_flip()


plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Japan/seats/plot.png",width = 15, height = 7.5)
