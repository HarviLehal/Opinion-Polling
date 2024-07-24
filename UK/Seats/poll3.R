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
poll <- read_csv("UK/Seats/poll3.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
h <- 0

election<-as.Date("04 07 2024", "%d %m %Y")
election<-max(d$Date)+14
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  # geom_point(size=2,data=d) +
  geom_point(size=2,data=d)+
  geom_line()+
  theme(axis.title=element_blank(),
        legend.title=element_blank(),
        axis.text.x = element_text(color = "grey20", size = 19, angle = 0, hjust = .5, vjust = .5, face = "plain"),
        axis.text.y = element_text(color = "grey20", size = 19, angle = 0, hjust = 0, vjust = 0.4, face = "plain"),
        legend.key.size = unit(2.5, 'lines'), legend.text = element_text(size=20))+
  scale_color_manual(values = c("#c70000"))+
  geom_hline(aes(yintercept=h))+
  scale_x_date(date_breaks = "1 week", date_labels =  "%d %b %Y",limits = c(old-3,election),guide = guide_axis(angle = -90))+
  ylim(0,100)+
  scale_y_continuous(breaks=seq(0,200,10))+
  geom_text(data=d[d$Date==max(d$Date),], aes(label = value), hjust=0, vjust=0, nudge_x = 0.1, nudge_y = 0, size=3.5, fontface="bold")+
  geom_text(data=d[d$Date==min(d$Date),], aes(label = value), hjust=0, vjust=0, nudge_x = -0.85, nudge_y = 0, size=3.5, fontface="bold")+
  guides(color = guide_legend(override.aes = list(label = "")))+
  ggtitle('Government Working Majority Since the 2024 General Election')+
  bbplot::bbc_style()
  
plot1

ggsave(plot=plot1, file="UK/Seats/plot3.png",width = 15, height = 7.5, type = "cairo-png")
