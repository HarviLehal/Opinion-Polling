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
  scale_color_manual(values = c("#1b66e8","#E81B23","#740e12","#A2A9B1"))+
  bbc_style()+
  geom_line(size=0.5)+
  geom_segment(aes(x=4,y=h, xend=-Inf, yend=h), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=max(d$Round),y=h-1, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=4,y=h, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  # geom_hline(aes(yintercept=h), alpha=0.75,colour="#000000")+
  geom_text(aes((min(d$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")
  
ggsave(plot=plot, file="US_Elections/Speaker/plot.png",width = 15, height = 7.5, type = "cairo-png")



# BREAKDOWN

poll2 <- read_csv("US_Elections/Speaker/speaker2.csv")
d2 <- melt(poll2, id.vars="Round")
h <- 218


plot2<-ggplot(data=d2,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=1) +
  scale_color_manual(values = c("#1b66e8","#E81B23","#ba161c", "#a21319", "#8b1015","#5d0b0e","#46080a" ,"#A2A9B1"))+
  bbc_style()+
  geom_line(size=0.5)+
  geom_segment(aes(x=4,y=h, xend=-Inf, yend=h), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=max(d2$Round),y=h-1, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=4,y=h, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  # geom_hline(aes(yintercept=h), alpha=0.75,colour="#000000")+
  geom_text(aes((min(d2$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")

ggsave(plot=plot2, file="US_Elections/Speaker/plot2.png",width = 15, height = 7.5, type = "cairo-png")