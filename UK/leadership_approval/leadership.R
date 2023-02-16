library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("UK/leadership_approval/data.py")
boris1 <- read_csv("UK/leadership_approval/boris.csv")
sunak1 <- read_csv("UK/leadership_approval/sunak.csv")
truss1 <- read_csv("UK/leadership_approval/truss.csv")

d1 <- melt(boris1, id.vars="Date")
d2 <- melt(sunak1, id.vars="Date")
d3 <- melt(truss1, id.vars="Date")
d <- rbind(d1,d2,d3)
d.list<-lapply(1:3,function(x) eval(parse(text=paste0("d",x))))
names(d.list)<-lapply(1:3, function(x) paste0("d", x))


for (i in 1:length(d.list)){ 
  d.list[[i]]$Date<-as.Date(d.list[[i]]$Date, "%d %b %Y")
  d.list[[i]]$value<-as.numeric(sub("%","",d.list[[i]]$value))/100
  d.list[[i]]$value[is.nan(d.list[[i]]$value)] <- 0
  d.list[[i]]$value<-formattable::percent(d.list[[i]]$value)
}
list2env(d.list,.GlobalEnv)

d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(sub("%","",d$value))/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)

starm<-as.Date("04 04 2020", "%d %m %Y")
truss<-as.Date("06 09 2022", "%d %m %Y")
sunak<-as.Date("25 10 2022", "%d %m %Y")

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c", "#015387", "#4ba3db"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",linewidth=0.75,wilder=TRUE)+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1.5)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1.5)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#015387", alpha=0.5, size=1.5)


ggsave(plot=plot1, file="UK/leadership_approval/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5,alpha=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c", "#015387", "#4ba3db"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75)+
  bbplot::bbc_style()+
  scale_y_continuous(name="Percentage",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1.5)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1.5)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#015387", alpha=0.5, size=1.5)

ggsave(plot=plot2, file="UK/leadership_approval/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c", "#015387", "#4ba3db"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",size=0.75,ratio=0.1)+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1.5)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1.5)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#015387", alpha=0.5, size=1.5)

ggsave(plot=plot3, file="UK/leadership_approval/plot3.png",width = 15, height = 7.5, type = "cairo-png")



# BORIS!!!!

# MA GRAPH

plot1b<-ggplot(data=d1,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",linewidth=0.75,wilder=TRUE)+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1.5)


ggsave(plot=plot1b, file="UK/leadership_approval/plot1b.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2b<-ggplot(data=d1,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5,alpha=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75)+
  bbplot::bbc_style()+
  scale_y_continuous(name="Percentage",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1.5)

ggsave(plot=plot2b, file="UK/leadership_approval/plot2b.png",width = 15, height = 7.5, type = "cairo-png")



# SUNAK

plot1s<-ggplot(data=d2,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",linewidth=0.75,wilder=TRUE)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.5, size=1.5)


ggsave(plot=plot1s, file="UK/leadership_approval/plot1s.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2s<-ggplot(data=d2,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5,alpha=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75)+
  bbplot::bbc_style()+
  scale_y_continuous(name="Percentage",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.5, size=1.5)

ggsave(plot=plot2s, file="UK/leadership_approval/plot2s.png",width = 15, height = 7.5, type = "cairo-png")


# TRUSS

plot1t<-ggplot(data=d3,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",linewidth=0.75,wilder=TRUE)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1.5)


ggsave(plot=plot1t, file="UK/leadership_approval/plot1t.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2t<-ggplot(data=d3,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5,alpha=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#8c8c8c"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75)+
  bbplot::bbc_style()+
  scale_y_continuous(name="Percentage",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1.5)

ggsave(plot=plot2t, file="UK/leadership_approval/plot2t.png",width = 15, height = 7.5, type = "cairo-png")
