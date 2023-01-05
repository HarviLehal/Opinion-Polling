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
  geom_point(size=2) +
  scale_color_manual(values = c("#1b66e8","#E81B23","#765431","#A2A9B1"))+
  bbc_style()+
  geom_line(size=1)+
  geom_segment(aes(x=4,y=h, xend=-Inf, yend=h), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=max(d$Round),y=h-1, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=4,y=h, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  # geom_hline(aes(yintercept=h), alpha=0.75,colour="#000000")+
  geom_text(aes((min(d$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d$Round), breaks = d$Round)
  
ggsave(plot=plot, file="US_Elections/Speaker/plot.png",width = 15, height = 7.5, type = "cairo-png")



# BREAKDOWN

poll2 <- read_csv("US_Elections/Speaker/speaker2.csv")
d2 <- melt(poll2, id.vars="Round")
h <- 218


plot2<-ggplot(data=d2,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(alpha=0.75,size=2) +
  scale_color_manual(values = c("#1b66e8","#E81B23","#A2A9B1", "#d6787c", "#A2A9B1","#765431","#A2A9B1", '#F01D7F',"#FFD700" ,"#000000"))+
  scale_size_manual(values = c(2,2,2,2,2,2,2,5,2))+
  bbc_style()+
  geom_line(size=1)+
  geom_segment(aes(x=4,y=h, xend=-Inf, yend=h), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=max(d2$Round),y=h-1, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=4,y=h, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  # geom_hline(aes(yintercept=h), alpha=0.75,colour="#000000")+
  geom_text(aes((min(d2$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d$Round), breaks = d$Round)

ggsave(plot=plot2, file="US_Elections/Speaker/plot2.png",width = 15, height = 7.5, type = "cairo-png")





## OMMITTING PRESENT!!!

# MAIN GRAPH

d3<-poll
d3$Present<-NULL
d3 <- melt(d3, id.vars="Round")

plot3<-ggplot(data=d3,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=2) +
  scale_color_manual(values = c("#1b66e8","#E81B23","#765431","#A2A9B1"))+
  bbc_style()+
  geom_line(size=1)+
  geom_segment(aes(x=4,y=h, xend=-Inf, yend=h), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=max(d$Round),y=h-1, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=4,y=h, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  # geom_hline(aes(yintercept=h), alpha=0.75,colour="#000000")+
  geom_text(aes((min(d3$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d3$Round), breaks = d3$Round)

ggsave(plot=plot3, file="US_Elections/Speaker/plot3.png",width = 15, height = 7.5, type = "cairo-png")



# BREAKDOWN

d4<-poll2
d4$Present<-NULL
d4 <- melt(d4, id.vars="Round")

plot4<-ggplot(data=d4,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=3,alpha=0.75) +
  scale_color_manual(values = c("#1b66e8","#E81B23","#542123", "#d6787c", "#f59da0","#765431","#736565","#FFD700", '#F01D7F' ,"#000000"))+
  scale_size_manual(values = c(2,2,2,2,2,2,2,5,2))+
  bbc_style()+
  geom_line(size=1)+
  geom_segment(aes(x=4,y=h, xend=-Inf, yend=h), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=max(d4$Round),y=h-1, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  geom_segment(aes(x=4,y=h, xend=4, yend=h-1), alpha=0.75,colour="#000000")+
  # geom_hline(aes(yintercept=h), alpha=0.75,colour="#000000")+
  geom_text(aes((min(d4$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d4$Round), breaks = d4$Round)

ggsave(plot=plot4, file="US_Elections/Speaker/plot4.png",width = 15, height = 7.5, type = "cairo-png")


