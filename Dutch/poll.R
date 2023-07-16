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

py_run_file("Dutch/data.py")
poll <- read_csv("Dutch/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
election<-as.Date("01 03 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# SEATS

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#222ACA","#3DAD3E","#0E2758",
                                "#53C74A","#E81718","#D21D24",
                                "#8ABD00","#7C1B1C","#226B26",
                                "#43A6EB","#552C83","#262B57",
                                "#DD601C","#45B6B1","#8C2591",
                                "#99C11A","#FBFD00","#162141"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)


# PVDA-GL FUSIE

poll <- read_csv("Dutch/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
election<-as.Date("01 03 2025", "%d %m %Y")
old <-min(d$Date)

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#222ACA","#3DAD3E","#0E2758",
                                "#cc1d1d","#53C74A","#E81718",
                                "#7C1B1C","#226B26","#43A6EB",
                                "#552C83","#262B57","#DD601C",
                                "#45B6B1","#8C2591","#99C11A",
                                "#FBFD00","#162141"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.2,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

# BAR CHART

poll <- read_csv("Dutch/poll2.csv")
Date <- c(max(poll$Date))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d1 <- round(colMeans(poll[-1]), digits=0)
d1 <- as.data.frame(d1)
d1[d1 == 0] <- 1   # ADDS 1 TO PARTY WITH 0 SEATS BUT REMOVE IF SUM OF PARTIES >150
sum(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2[-1]<-lapply(d2[-1],as.numeric)

d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d2 <- reshape2::melt(d2, id.vars="Date")
d2$value[is.na(d2$value)] <- 0 # FIXES 0 SEATS OLD ELECTION PARTIES

d3<-rbind(d2,d1)

plot3<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#858be6","#222ACA","#92d692","#3DAD3E","#657dad","#0E2758",
                                "#e68383","#cc1d1d","#a1e39d","#53C74A","#f58787","#E81718",
                                "#bd7375","#7C1B1C","#77b57b","#226B26","#9fd3f5","#43A6EB",
                                "#a080bf","#552C83","#7b80ab","#262B57","#f0ad89","#DD601C",
                                "#97dbd5","#45B6B1","#c37fc9","#8C2591","#cae080","#99C11A",
                                "#fafc7e","#FBFD00","#6c7aa1","#162141"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('30 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()



plot<-ggarrange(plot2, plot3,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Dutch/plot.png",width = 15, height = 7.5, type="cairo-png")

