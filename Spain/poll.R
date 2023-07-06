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
py_run_file("Spain/data.py")
poll <- read_csv("Spain/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("23 07 2023", "%d %m %Y")
old <-min(d$Date)

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old|d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#ef1c27","#1d84ce","#63be21",
                                "#ffb232","#00c7ae","#4aae4a",
                                "#b5cf18","#ec640c","#ef4b91"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.15,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot1
# Moving Average


d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=14, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="right"))

plot1a<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,]) +
  scale_color_manual(values = c("#ef1c27","#1d84ce","#63be21",
                                "#ffb232","#00c7ae","#4aae4a",
                                "#b5cf18","#ec640c","#ef4b91"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)



poll <- read_csv("Spain/poll.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
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
  scale_fill_manual(values = c("#f46068","#ef1c27","#61a9dd","#1d84ce","#92d264","#63be21",
                               "#ffc970","#ffb232","#4dd8c6","#00c7ae","#80c680","#4aae4a",
                               "#cbdd5d","#b5cf18","#f29355","#ec640c","#f481b2","#ef4b91"))+
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
  ggtitle('7 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()



plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="Spain/plot.png",width = 15, height = 7.5, type="cairo-png")

plot1a<-plot1a+theme(legend.position = "none")
plot<-ggarrange(plot1a, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))

ggsave(plot=plot, file="Spain/plot2.png",width = 15, height = 7.5, type="cairo-png")
