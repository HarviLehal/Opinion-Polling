library(ggplot2)
library(bbplot)
library(Cairo)
library(reshape2)
library(readr)
poll <- read_csv("US_Elections/Speaker/speaker.csv")
d <- melt(poll, id.vars="Round")
h <- 218

# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=1) +
  scale_color_manual(values = c("#1b66e8","#E81B23","#941015","#A2A9B1"))+
  bbc_style()+
  geom_line(size=0.5)+
  geom_segment(aes(x=3,y=h, xend=-Inf, yend=h), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=5,y=h-1, xend=3, yend=h-1), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=3,y=h, xend=3, yend=h-1), alpha=0.75,colour="#000000")+
  # geom_hline(aes(yintercept=h), alpha=0.75,colour="#000000")+
  geom_text(aes((min(d$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")
  
ggsave(plot=plot, file="US_Elections/Speaker/plot.png",width = 15, height = 7.5, type = "cairo-png")
