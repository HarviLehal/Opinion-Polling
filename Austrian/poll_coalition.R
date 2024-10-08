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
poll <- read_csv("Austrian/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
# h <- formattable::percent(0.47)
h <- read.csv("Austrian/poll3.csv")  # this is the majority line, plot it for each poll and join them
h <- reshape2::melt(h, id.vars="Date")
h$value<-as.numeric(h$value)/100
hy<-formattable::percent(h$value[h$Date==min(h$Date)]-0.01)
h$value<-formattable::percent(h$value)
h$Date <- as.Date(h$Date, "%Y-%m-%d")

election<-as.Date("29 09 2024", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#509a3a","#ce000c","#e84188","#4D0E90",
                                "#aa692f","#8ee53f","#ee8d23","#000000"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.15,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.15,linewidth=1.2, data=h, alpha=0.5, linetype="dashed")+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  # geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(old,hy,label = "Mehrheit", vjust = -1, hjust=1),colour="#000000")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date)-12, election)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2024 Austrian Legislative Election')

plot1



d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=14, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="center"))

plot1a<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#88b626","#ce000c","#4D0E90","#8ee53f",
                                "#ee8d23","#e84188","#aa692f","#000000"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_hline(aes(yintercept=max(h$value[h$Date==max(h$Date)])), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,max(h$value[h$Date==max(h$Date)]),label = "Mehrheit", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2024 Austrian Legislative Election')

plot1a


poll <- read_csv("Austrian/poll2.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=max(poll$Date),]
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
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d4<-rbind(d1,d2,d3)

hx <- read.csv("Austrian/poll3.csv")
hx$Date <- as.Date(hx$Date, "%Y-%m-%d")
hx<-hx[hx$Date==(max(h$Date)),]
hx <- colMeans(hx[-1],na.rm=TRUE)
hx <- reshape2::melt(hx, id.vars="Date")
hx$value<-as.numeric(hx$value)/100
hx$value<-formattable::percent(hx$value, digits = 3)



plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#cfe2a8","#b8d37d","#88b626",
                               "#eb999e","#e2666d","#ce000c",
                               "#a687c8","#713ea6","#4D0E90",
                               "#d2f5b2","#bbef8c","#8ee53f",
                               "#f8d1a7","#f5bb7b","#ee8d23",
                               "#f6b3cf","#f18db8","#e84188",
                               "#ddc3ac","#cca582","#aa692f"))+
  geom_hline(aes(yintercept=hx$value), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               paste(formattable::percent(d4$value, digits = 1)), ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface=ifelse(d4$Date==max(d4$Date),"bold","bold.italic"))+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               ifelse(is.na(d4$value)==TRUE,"(New)",
                                      (paste("(",formattable::percent(d4$value, digits = 1),")"))),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('Results <br> *7 day Average* <br> *(2019 Election)*')+
  scale_x_discrete(limits = rev(levels(d4$variable)))+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Austrian/plot2.png",width = 15, height = 7.5, type="cairo-png")

plota<-ggarrange(plot1a, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plota

ggsave(plot=plota, file="Austrian/plot2_ma.png",width = 15, height = 7.5, type="cairo-png")
