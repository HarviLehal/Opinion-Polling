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
py_run_file("Spain/Seats/data.py")
poll <- read_csv("Spain/Seats/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")

election<-as.Date("22 08 2027", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH
# parties<-d[d$variable!='Podemos'&d$variable!='SALF',]
# podemos<-d[d$variable=='Podemos'|d$variable=='SALF',]
# podemos<-podemos[!is.na(podemos$value),]

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#ef1c27","#1d84ce"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  scale_y_continuous(breaks=seq(0,200,10))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Seat Projection For Next Spanish General Election')

plot1


poll <- read_csv("Spain/Seats/poll.csv")
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

plot2<-ggplot(d3, aes(fill=interaction(Date,variable), y=value, x=Date)) + 
  scale_fill_manual(values = c("#f46068","#ef1c27",
                               "#61a9dd","#1d84ce"))+
  geom_bar(position="fill", stat="identity")+
  geom_text(aes(label = ifelse(d3$Date==max(d3$Date),ifelse(d3$variable=="Government",paste("Government:",d3$value),paste("Opposition:",d3$value)),
                               ifelse(d3$variable=="Government",paste("Current Government:",d3$value),paste("Current Opposition:",d3$value))),
                hjust=0.5, vjust = 0.5,y = ifelse(d3$variable=="Government",0.89,0.11)),
            color="#000000",position =, size=5, fontface="bold")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_blank(),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=1,alpha=0.75) +
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 1, nrow = 2,heights=c(2,0.3))
plot

ggsave(plot=plot, file="Spain/Seats/plot.png",width = 15, height = 7.5, type="cairo-png")

