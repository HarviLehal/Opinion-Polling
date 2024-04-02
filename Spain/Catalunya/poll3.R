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
poll <- read_csv("Spain/Catalunya/seats2.csv")
d <- reshape2::melt(poll, id.vars="Date")

election<-as.Date("18 05 2024", "%d %m %Y")
old <-min(d$Date)
# start<-as.Date("01 01 2024", "%d %m %Y")
# d<-d[d$Date>start,]

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#ffb232","#ef1c27"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.5,linewidth=0.75, data=new[new$Date!=old,])+
  # geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  # scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date)-0.725, election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot1

poll <- read_csv("Spain/Catalunya/seats2.csv")
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


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#ffc970","#ffb232",
                               "#f46068","#ef1c27"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day Average \n (2021 Election)')+
  scale_x_discrete(limits = rev(levels(d3$variable)),labels = label_wrap(8))+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plot

ggsave(plot=plot, file="Spain/Catalunya/seats2.png",width = 15, height = 7.5, type="cairo-png")
