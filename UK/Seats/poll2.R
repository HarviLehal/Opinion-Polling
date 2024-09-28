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
library(ggbreak)

py_run_file("UK/Seats/data2.py")
poll <- read_csv("UK/Seats/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
h <- 325

# election<-as.Date("15 10 2024", "%d %m %Y")
election<-as.Date("04 07 2024", "%d %m %Y")
election<-max(d$Date)+14
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  # geom_point(size=2,data=d) +
  geom_point(size=2,data=d)+
  geom_line()+
  scale_color_manual(values = c("#e8043c","#0884dc","#ffa41c","#fff48c",
                                "#d46a4c","#666666","#10b4d4","#528D6B","#005b54",
                                "#25a928","#f8cc2c","#201464",
                                "#a09cfc","#999999","#386464"))+
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
  geom_hline(aes(yintercept=h))+
  geom_text(aes((election),h,label = "Majority (326 Seats)",hjust=1 ,vjust = -1),colour="#000000",fontface="bold.italic")+
  # geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  # geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "1 week", date_labels =  "%d %b %Y",limits = c(old-4,election),guide = guide_axis(angle = -90))+
  scale_y_continuous(breaks=seq(0,650,20))+
  # add label for the last point of each line and make the text bold, making sure labels don't overlap
  ggtitle('Make-up of the House of Commons Since the 2024 General Election')
plot1

# Bar Chart

poll <- read_csv("UK/Seats/poll2.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x)
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date==max(poll$Date),]
d1 <- as.data.frame(poll)
# d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")

d2 <- reshape2::melt(d2, id.vars="Date")

d3<-rbind(d2,d1)


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#f27999","#E4003B","#77c0ed","#0087DC","#fcd38b","#FAA61A",
                               "#fcf7c5","#FDF38E","#e5a694","#d46a4c","#a3a3a3","#666666",
                               "#70d2e5","#10b4d4","#9dc7af","#528D6B","#669d98","#005b54",
                               "#7ccb7e","#25a928","#fbe080","#f8cc2c","#7972a2","#201464",
                               "#c6c4fd","#a09cfc","#c2c2c2","#999999","#88a2a2","#386464"
                               ))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=ifelse(d3$value>100,-1,ifelse(d3$value>10,-1.4,-2.5)), color="#000000",position = position_dodge(0.9), size=3.5,fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=-0.3, color="#404040", position = position_dodge(0.8), size=3.5,fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' Current \n (2024 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()

plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="UK/Seats/plot2.png",width = 24, height = 12, type = "cairo-png")

