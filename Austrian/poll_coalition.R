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
poll <- read_csv("Austrian/poll3.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.47)

election<-as.Date("23 10 2024", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#509a3a","#dd1529","#10305b",
                                "#8ee53f","#ee8d23","#e84188","#aa692f"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.15,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election-4,h,label = "Mehrheit", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

plot1


d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=14, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="center"))

plot1a<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#509a3a","#dd1529","#10305b",
                                "#8ee53f","#ee8d23","#e84188","#aa692f"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election-4,h,label = "Mehrheit", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

plot1a


poll <- read_csv("Austrian/poll3.csv")

# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
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
  scale_fill_manual(values = c("#96c289","#509a3a","#eb737f","#dd1529","#70839d","#10305b",
                               "#bbef8c","#8ee53f","#f5bb7b","#ee8d23","#f18db8","#e84188",
                               "#cca582","#aa692f"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),
                y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Austrian/plot2.png",width = 15, height = 7.5, type="cairo-png")

plota<-ggarrange(plot1a, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plota

ggsave(plot=plota, file="Austrian/plot2_ma.png",width = 15, height = 7.5, type="cairo-png")
