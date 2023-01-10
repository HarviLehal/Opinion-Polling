library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(dplyr)
py_run_file("UK_Elections/general_polling/data.py")
poll <- read_csv("UK_Elections/general_polling/poll.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
old<-c(as.Date("12 12 2019", "%d %m %Y"),as.Date("08 07 2017", "%d %m %Y"),as.Date("07 05 2015", "%d %m %Y"),as.Date("06 05 2010", "%d %m %Y"),as.Date("05 05 2005", "%d %m %Y"),as.Date("07 06 2001", "%d %m %Y"),as.Date("01 05 1997", "%d %m %Y"),as.Date("09 04 1992", "%d %m %Y"))

starm<-as.Date("04 04 2020", "%d %m %Y")
davey<-as.Date("27 08 2020", "%d %m %Y")
green<-as.Date("01 10 2021", "%d %m %Y")
truss<-as.Date("06 09 2022", "%d %m %Y")
sunak<-as.Date("25 10 2022", "%d %m %Y")
f<-formattable::percent(0.6)
g<-formattable::percent(0.55)

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,],alpha=0.1) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF","#6D3177", "#222221"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 14,linetype="solid",linewidth=0.75,wilder=TRUE, data=d[d$Date!=old,])+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old[1],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[1],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5.25, shape=5, alpha=0.5)+ 
  scale_x_date(date_breaks = "1 year",date_labels = "%Y")+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)
        ,axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))


ggsave(plot=plot1, file="UK_Elections/general_polling/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,],alpha=0.1) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF","#6D3177", "#222221"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.1,linewidth=0.75, data=d[d$Date!=old,])+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old[1],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[1],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5.25, shape=5, alpha=0.5)+ 
  scale_x_date(date_breaks = "1 year",date_labels = "%Y")+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)
        ,axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))
  
# for(i in 1:8) {
#     geom_point(data=d[d$Date==old[i],],size=5, shape=18, alpha=0.5)+
#     geom_point(data=d[d$Date==old[i],],size=5.25, shape=5, alpha=0.5)
# }
ggsave(plot=plot2, file="UK_Elections/general_polling/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,],alpha=0.1) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF","#6D3177", "#222221"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 7,linetype="solid",linewidth=0.75,wilder=TRUE, data=d[d$Date!=old,])+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old[1],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[1],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5.25, shape=5, alpha=0.5)+ 
  scale_x_date(date_breaks = "1 year",date_labels = "%Y")+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)
        ,axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))


ggsave(plot=plot4, file="UK_Elections/general_polling/plot3.png",width = 30, height = 7.5, type = "cairo-png")

plot4<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,],alpha=0.1) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF","#6D3177", "#222221"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 3,linetype="solid",linewidth=0.75,wilder=TRUE, data=d[d$Date!=old,])+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old[1],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[1],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[2],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[3],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[4],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[5],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[6],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[7],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[8],],size=5.25, shape=5, alpha=0.5)+ 
  scale_x_date(date_breaks = "1 year",date_labels = "%Y")+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)
        ,axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))


ggsave(plot=plot4, file="UK_Elections/general_polling/plot4.png",width = 30, height = 7.5, type = "cairo-png")


z<-poll
z$`Change UK`<-NULL
z <- melt(z, id.vars="Date")
z$value<-as.numeric(z$value)/100
z$value<-formattable::percent(z$value)

plot5<-ggplot(data=z,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=z[z$Date!=old,],alpha=0.1) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF","#6D3177"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.01,linewidth=0.75, data=z[z$Date!=old,])+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=z[z$Date==old[1],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[1],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[2],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[2],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[3],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[3],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[4],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[4],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[5],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[5],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[6],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[6],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[7],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[7],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[8],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[8],],size=5.25, shape=5, alpha=0.5)+ 
  scale_x_date(date_breaks = "1 year",date_labels = "%Y")+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)
        ,axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))

# for(i in 1:8) {
#     geom_point(data=d[d$Date==old[i],],size=5, shape=18, alpha=0.5)+
#     geom_point(data=d[d$Date==old[i],],size=5.25, shape=5, alpha=0.5)
# }
ggsave(plot=plot5, file="UK_Elections/general_polling/plot5.png",width = 15, height = 7.5, type = "cairo-png")
