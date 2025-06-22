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

py_run_file("Spain/Seats/data.py")
poll <- read_csv("Spain/Seats/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
# d$value[d$value=='-'] <- NULL
election<-as.Date("22 08 2027", "%d %m %Y")
old<-min(d$Date)
# MAIN GRAPH


plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#1d84ce","#ef1c27","#63be21","#ef4b91","#ffb232","#00c7ae","#b5cf18","#4aae4a","#adcfef","#ffd700","#00599b","#9369f5","#795a44"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  scale_y_continuous(breaks=seq(0,180,20))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 months", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Seat Projection for the Next Spanish General Election')
plot1


# BAR CHART

poll <- read_csv("Spain/Seats/poll2.csv")
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

plot3<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#61a9dd","#1d84ce",
                               "#f46068","#ef1c27",
                               "#92d264","#63be21",
                               "#f481b2","#ef4b91",
                               "#ffc970","#ffb232",
                               "#4dd8c6","#00c7ae",
                               "#cbdd5d","#b5cf18",
                               "#80c680","#4aae4a",
                               "#cee2f5","#adcfef",
                               "#ffe766","#ffd700",
                               "#669bc3","#00599b",
                               "#bea5f9","#9369f5",
                               "#af9c8f","#795a44"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date),
                               ifelse(d3$Date == max(d3$Date),
                                      paste(d3$value),
                                      paste(d3$value)), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),ifelse(is.na(d3$value)==FALSE,
                                                              paste("(",d3$value,")"),ifelse(d3$variable=='Podemos',paste("(Left Sumar)"),paste("(New)"))),""),
                y = 0),hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day average \n (2023 Result)')+
  scale_x_discrete(limits = d3$variable[order(d1$value,na.last = FALSE)])+
  coord_flip()
plot3


plotA<-ggarrange(plot1, plot3,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA



ggsave(plot=plotA, file="Spain/Seats/plot2.png",width = 20, height = 10, type="cairo-png")

# EXTRA GRAPHIEK


d1$value<-ifelse(is.na(d1$value)==TRUE,0,d1$value)
d2$value<-ifelse(is.na(d2$value)==TRUE,0,d2$value)
d1$value<-d1$value/sum(d1$value,na.rm=TRUE)
d2$value<-d2$value/sum(d2$value,na.rm=TRUE)
d1$Date<-'14 Day Average'
d2$Date<-'2023 Result'

ordered<-c('PP','UPN','VOX','SALF','CCa','JxCat','Podemos','PNV','EHB','ERC','BNG','Sumar','PSOE')

d1<-d1 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d2<-d2 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d3<-rbind(d1,d2)


plot3a<-ggplot(d3, aes(fill=interaction(rev(Date),variable), y=value, x=Date,label=round(value*350))) + 
  scale_fill_manual(values = c("#61a9dd","#1d84ce",
                               "#669bc3","#00599b",
                               "#92d264","#63be21",
                               "#af9c8f","#795a44",
                               "#ffe766","#ffd700",
                               "#4dd8c6","#00c7ae",
                               "#bea5f9","#9369f5",
                               "#80c680","#4aae4a",
                               "#cbdd5d","#b5cf18",
                               "#ffc970","#ffb232",
                               "#cee2f5","#adcfef",
                               "#f481b2","#ef4b91",
                               "#f46068","#ef1c27"))+
  geom_bar(position="fill", stat="identity")+
  geom_text(data=subset(d3,value != 0),size = 5.5, position = position_stack(vjust = 0.5),fontface=ifelse(subset(d3,value != 0)$Date=='2023 Result',"bold.italic","bold"),color="#FFFFFF")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold",color="#000000",size=10),
        axis.text.y = element_text(face="bold.italic",size=15,color="#000000",hjust=1),
        # axis.text.y = element_blank(),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=0.5,alpha=0.25) +
  scale_x_discrete(limits=rev)+
  coord_flip()
plot3a

plot<-ggarrange(plot1, plot3a,ncol = 1, nrow = 2,heights=c(2,0.3))
plot



ggsave(plot=plot, file="Spain/Seats/plot2_bloc.png",width = 15, height = 7.5, type = "cairo-png")

