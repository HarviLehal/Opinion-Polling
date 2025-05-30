library(ggplot2)
library(bbplot)
library(Cairo)
library(reshape2)
library(readr)
poll <- read_csv("USA/Speaker/speaker.csv")
d <- reshape2::melt(poll, id.vars="Round")
h <- 218

# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=2,data=d[d$variable!='Threshold',]) +
  geom_point(size=2,data=d[d$variable=='Threshold',],shape=4,alpha=0.5)+
  scale_color_manual(values = c("#1b66e8","#E81B23","#765431","#A2A9B1","#000000"))+
  bbc_style()+
  geom_line(size=1,data=d[d$variable!='Threshold',])+
  geom_line(size=1,data=d[d$variable=='Threshold',],alpha=0.5)+
  geom_text(aes((min(d$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d$Round), breaks = d$Round)
  
ggsave(plot=plot, file="USA/Speaker/plot.png",width = 7.5, height = 10, type = "cairo-png")



# BREAKDOWN

poll2 <- read_csv("USA/Speaker/speaker2.csv")
d2 <- reshape2::melt(poll2, id.vars="Round")
h <- 218


plot2<-ggplot(data=d2,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=2,data=d2[d2$variable!='Threshold',],alpha=0.75) +
  scale_color_manual(values = c("#A2A9B1","#A2A9B1","#765431", "#d6787c", "#1b66e8","#F01D7F","#E81B23", '#000000',"#000000" ,"#FFD700","#A2A9B1"))+
  geom_point(size=2,data=d2[d2$variable=='Threshold',],shape=4,alpha=0)+
  # bbc_style()+
  geom_line(size=1,data=d2[d2$variable!='Threshold',])+
  geom_line(size=1,data=d2[d2$variable=='Threshold',],alpha=0.5)+
  geom_text(aes((min(d2$Round)),h-2,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d2$Round), breaks = d2$Round)

ggsave(plot=plot2, file="USA/Speaker/plot2.png",width = 7.5, height = 10, type = "cairo-png")





## OMMITTING PRESENT!!!

# MAIN GRAPH

d3<-poll
d3$Present<-NULL
d3 <- reshape2::melt(d3, id.vars="Round")

plot3<-ggplot(data=d3,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=2,data=d3[d3$variable!='Threshold',]) +
  geom_point(size=2,data=d3[d3$variable=='Threshold',],shape=4,alpha=0.5)+
  scale_color_manual(values = c("#1b66e8","#E81B23","#765431","#A2A9B1","#000000"))+
  bbc_style()+
  geom_line(size=1)+
  geom_text(aes((min(d3$Round)),h-2.5,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d3$Round), breaks = d3$Round)

ggsave(plot=plot3, file="USA/Speaker/plot3.png",width = 15, height = 7.5, type = "cairo-png")



# BREAKDOWN

d4<-poll2
d4$Present<-NULL
d4 <- reshape2::melt(d4, id.vars="Round")

plot4<-ggplot(data=d4,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=2,data=d4[d4$variable!='Threshold',],alpha=0.75) +
  geom_point(size=2,data=d4[d4$variable=='Threshold',],shape=4,alpha=0)+
  scale_color_manual(values = c("#A2A9B1","#A2A9B1","#765431", "#d6787c", "#1b66e8","#F01D7F","#E81B23","#000000" ,"#FFD700","#A2A9B1"))+
  bbc_style()+
  geom_line(size=1,data=d4[d4$variable!='Threshold',])+
  geom_line(size=1,data=d4[d4$variable=='Threshold',],alpha=0.5)+
  geom_text(aes((min(d4$Round)),h-2,label = "Majority", vjust = -1),colour="#000000")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d4$Round), breaks = d4$Round)

ggsave(plot=plot4, file="USA/Speaker/plot4.png",width = 7.5, height = 10, type = "cairo-png")




# BREAKDOWN
poll3 <- read_csv("USA/Speaker/speaker3.csv")

d5<-poll3
d5$Present<-NULL
d5 <- reshape2::melt(d5, id.vars="Round")

plot5<-ggplot(data=d5,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=2,data=d5[d5$variable!='Threshold',],alpha=0.75) +
  geom_point(size=2,data=d5[d5$variable=='Threshold',],shape=4,alpha=0)+
  scale_color_manual(values = c("#1b66e8","#E81B23","#76b5c5","#765431","#A2A9B1","#000000"))+
  scale_size_manual(values=c(1.5,1.5,3,1.5,1.5,1.5))+
  bbc_style()+
  geom_line(size=1,data=d5[d5$variable!='Threshold',])+
  geom_line(size=1.25,data=d5[d5$variable=='Threshold',],alpha=0.75)+
  geom_text(aes((min(d5$Round)),h-2,label = "Majority", vjust = -1),colour="#56595c")+
  geom_vline(xintercept=max(d5$Round-0.5), linetype="solid", color = "#56595c", alpha=1, size=0.75)+
  geom_text(aes((max(d5$Round)-0.65),h+22,label = "No Confidence Vote", vjust = -1, angle=-90),colour="#56595c")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d5$Round), breaks = d5$Round)+
  ylim(0,250)
plot5
ggsave(plot=plot5, file="USA/Speaker/plot5.png",width = 10, height = 10, type = "cairo-png")

poll4 <- read_csv("USA/Speaker/speaker4.csv")

d6<-poll4
d6$Present<-NULL
d6 <- reshape2::melt(d6, id.vars="Round")

plot6<-ggplot(data=d6,aes(x=Round,y=value, colour=variable, group=variable)) +
  geom_point(size=2,data=d6[d6$variable!='Threshold',],alpha=0.75) +
  geom_point(size=2,data=d6[d6$variable=='Threshold',],shape=4,alpha=0)+
  scale_color_manual(values = c("#A2A9B1","#A2A9B1","#765431", "#d6787c", "#1b66e8","#F01D7F","#E81B23","#76b5c5","#000000","#FFD700","#A2A9B1"))+
  geom_point(size=2,data=d6[d6$variable=='Threshold',],shape=4,alpha=0)+
  bbc_style()+
  geom_line(size=1,data=d6[d6$variable!='Threshold',])+
  geom_line(size=1,data=d6[d6$variable=='Threshold',],alpha=0.5)+
  geom_text(aes((min(d6$Round)),h-2,label = "Majority", vjust = -1),colour="#000000")+
  geom_vline(xintercept=max(d5$Round-0.5), linetype="solid", color = "#56595c", alpha=1, size=0.75)+
  geom_text(aes((max(d5$Round)-0.55),h+22,label = "No Confidence Vote", vjust = -1, angle=-90),colour="#56595c")+
  theme(axis.title = element_text(size = 18))+
  labs(x="Round",y="Votes")+
  scale_x_continuous("Round", labels = as.character(d6$Round), breaks = d6$Round)+
  ylim(0,250)
plot6

ggsave(plot=plot6, file="USA/Speaker/plot6.png",width = 10, height = 10, type = "cairo-png")