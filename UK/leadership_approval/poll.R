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

py_run_file("UK/leadership_approval/data.py")

poll1 <- read_csv("UK/leadership_approval/sunak.csv")
poll2 <- read_csv("UK/leadership_approval/truss.csv")
poll3 <- read_csv("UK/leadership_approval/boris.csv")
poll4 <- read_csv("UK/leadership_approval/corbyn.csv")
poll<-dplyr::bind_rows(poll1,poll2,poll3,poll4)
f<-formattable::percent(0.575)

# poll <- rbind(poll1,poll2) 
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
sunak<-as.Date("25 10 2022", "%d %m %Y")
truss<-as.Date("06 09 2022", "%d %m %Y")
boris<-as.Date("12 12 2019", "%d %m %Y")
starm<-as.Date("04 04 2020", "%d %m %Y")

d_sunak <- reshape2::melt(poll1, id.vars="Date")
d_truss <- reshape2::melt(poll2, id.vars="Date")
d_boris <- reshape2::melt(poll3, id.vars="Date")
d_corbyn<- reshape2::melt(poll4, id.vars="Date")

d_sunak$value<-as.numeric(d_sunak$value)/100
d_sunak$value<-formattable::percent(d_sunak$value)

d_truss$value<-as.numeric(d_truss$value)/100
d_truss$value<-formattable::percent(d_truss$value)

d_boris$value<-as.numeric(d_boris$value)/100
d_boris$value<-formattable::percent(d_boris$value)

d_corbyn$value<-as.numeric(d_corbyn$value)/100
d_corbyn$value<-formattable::percent(d_corbyn$value)
# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=sunak|d$Date!=truss|d$Date!=boris,],alpha=0.25)+
  scale_color_manual(values = c("#e4003b","#005184","#999999",
                                "#66b7ea","#0087dc","#890023"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.9,linewidth=0.75, data=d_sunak[d_sunak$Date!=sunak,])+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=1,linewidth=0.75, data=d_truss[d_truss$Date!=truss,])+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.25,linewidth=0.75, data=d_boris[d_boris$Date!=boris,])+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.75,linewidth=0.75, data=d_corbyn[d_corbyn$Date!=boris,])+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  # geom_line(linewidth=0.75,data=d_new)+
  # theme(axis.title=element_blank(),legend.title = element_blank(),
  #       legend.key.size = unit(2, 'lines'),
  #       legend.position = "none")+
  geom_vline(xintercept=boris, linetype="dashed", color = "#0087DC", alpha=0.75, size=1)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.75, size=1)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.75, size=1)+
  geom_vline(xintercept=starm, linetype="dashed", color = "#e4003b", alpha=0.75, size=1)+
  geom_text(aes(boris,f,label = "Election", vjust = -0.5, angle=-90),colour="#0087DC")+
  geom_text(aes(sunak,f,label = "Sunak", vjust = -0.5, angle=-90),colour="#0087DC")+
  geom_text(aes(truss,f,label = "Truss", vjust = -0.5, angle=-90),colour="#0087DC")+
  geom_text(aes(starm,f,label = "Starmer", vjust = -0.5, angle=-90),colour="#e4003b")+
  xlim(min(d$Date), max(d$Date))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==sunak|d$Date==truss|d$Date==boris,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==sunak|d$Date==truss|d$Date==boris,],size=5.25, shape=5, alpha=1)
plot1


ggsave(plot=plot1, file="UK/leadership_approval/plot.png",width = 15, height = 7.5, type="cairo-png")
