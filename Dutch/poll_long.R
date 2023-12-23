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

poll1 <- read_csv("Dutch/poll.csv")
poll2 <- read_csv("Dutch/poll_new.csv")
poll<-dplyr::bind_rows(poll1,poll2)
# poll <- rbind(poll1,poll2) 
d <- reshape2::melt(poll, id.vars="Date")
election<-as.Date("22 11 2023", "%d %m %Y")
next_election<-max(d$Date)
old_election <-min(d$Date)

d_old <- reshape2::melt(poll1, id.vars="Date")
d_new <- reshape2::melt(poll2, id.vars="Date")

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old_election|d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#222ACA","#3DAD3E","#0E2758",
                                "#cc1d1d","#53C74A","#E81718",
                                "#7C1B1C","#226B26","#43A6EB",
                                "#552C83","#262B57","#DD601C",
                                "#45B6B1","#8C2591","#99C11A",
                                "#FBFD00","#162141","#f0c400"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=d_old[d_old$Date!=election,])+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=1,linewidth=0.75, data=d_new)+
  # geom_line(linewidth=0.75,data=d_new)+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_vline(xintercept=old_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), next_election)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5.25, shape=5, alpha=1)
plot1

# poll1 <- read_csv("Dutch/poll.csv")
poll <- read_csv("Dutch/poll_new.csv")
# poll<-dplyr::bind_rows(poll1,poll2)
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))

d2 <- poll[poll$Date==election,]
poll<-poll[poll$Date>(max(poll$Date)-7),]
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
  
  scale_fill_manual(values = c("#6e7d9b","#0E2758",
                               "#e07777","#cc1d1d",
                               "#7a7fdf","#222ACA",
                               "#f6dc66","#f0c400",
                               "#8bce8b","#3DAD3E",
                               "#c2da76","#99C11A",
                               "#98dd92","#53C74A",
                               "#f17474","#E81718",
                               "#8fd3d0","#45B6B1",
                               "#7aa67d","#226B26",
                               "#b07677","#7C1B1C",
                               "#eba077","#DD601C",
                               "#8ecaf3","#43A6EB",
                               "#9980b5","#552C83",
                               "#7d809a","#262B57"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 day average \n (2023 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()


plotA<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA

ggsave(plot=plotA, file="Dutch/plot_long.png",width = 15, height = 7.5, type="cairo-png")
