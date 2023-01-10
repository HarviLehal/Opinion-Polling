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
old<-c(as.Date("12 12 2019", "%d %m %Y"),
       as.Date("08 06 2017", "%d %m %Y"),
       as.Date("07 05 2015", "%d %m %Y"),
       as.Date("06 05 2010", "%d %m %Y"),
       as.Date("05 05 2005", "%d %m %Y"),
       as.Date("07 06 2001", "%d %m %Y"),
       as.Date("01 05 1997", "%d %m %Y"),
       as.Date("09 04 1992", "%d %m %Y"),
       as.Date("11 06 1987", "%d %m %Y"),
       as.Date("09 06 1983", "%d %m %Y"),
       as.Date("03 05 1979", "%d %m %Y"),
       as.Date("10 10 1974", "%d %m %Y"),
       as.Date("28 02 1974", "%d %m %Y"),
       as.Date("18 06 1970", "%d %m %Y"),
       as.Date("31 03 1966", "%d %m %Y"),
       as.Date("15 10 1964", "%d %m %Y"),
       as.Date("08 10 1959", "%d %m %Y"),
       as.Date("26 05 1955", "%d %m %Y"),
       as.Date("25 10 1951", "%d %m %Y"),
       as.Date("23 02 1950", "%d %m %Y"),
       as.Date("05 07 1945", "%d %m %Y"))

f<-formattable::percent(0.6)
g<-formattable::percent(0.55)

h<-melt(poll[5899,],id.vars="Date")
h$value<-as.numeric(h$value)/100
h$value<-formattable::percent(h$value)

h2<-melt(poll[6551,],id.vars="Date")
h2$value<-as.numeric(h2$value)/100
h2$value<-formattable::percent(h2$value)
  
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
  geom_point(data=d[d$Date==old[9],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[9],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h,size=5, shape=18, alpha=0.5)+
  geom_point(data=h,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h2,size=5, shape=18, alpha=0.5)+
  geom_point(data=h2,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5.25, shape=5, alpha=0.5)+
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
  geom_point(data=d[d$Date==old[9],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[9],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h,size=5, shape=18, alpha=0.5)+
  geom_point(data=h,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h2,size=5, shape=18, alpha=0.5)+
  geom_point(data=h2,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5.25, shape=5, alpha=0.5)+
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
  geom_point(data=d[d$Date==old[9],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[9],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h,size=5, shape=18, alpha=0.5)+
  geom_point(data=h,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h2,size=5, shape=18, alpha=0.5)+
  geom_point(data=h2,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "1 year",date_labels = "%Y")+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)
        ,axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))


ggsave(plot=plot3, file="UK_Elections/general_polling/plot3.png",width = 30, height = 7.5, type = "cairo-png")

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
  geom_point(data=d[d$Date==old[9],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[9],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[10],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[11],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h,size=5, shape=18, alpha=0.5)+
  geom_point(data=h,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[12],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[14],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[15],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[16],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[17],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[18],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[19],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=h2,size=5, shape=18, alpha=0.5)+
  geom_point(data=h2,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old[21],],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "1 year",date_labels = "%Y")+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)
        ,axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))


ggsave(plot=plot4, file="UK_Elections/general_polling/plot4.png",width = 30, height = 7.5, type = "cairo-png")


z<-poll
z$`Change UK`<-NULL

i<-melt(z[5899,],id.vars="Date")
i$value<-as.numeric(i$value)/100
i$value<-formattable::percent(i$value)
i2<-melt(z[6551,],id.vars="Date")
i2$value<-as.numeric(i2$value)/100
i2$value<-formattable::percent(i2$value)

z <- melt(z, id.vars="Date")
z$value<-as.numeric(z$value)/100
z$value<-formattable::percent(z$value)

plot5<-ggplot(data=z,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=z[z$Date!=old,],alpha=0.1) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF","#6D3177"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.05,linewidth=0.75, data=z[z$Date!=old,])+
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
  geom_point(data=z[z$Date==old[9],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[9],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[10],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[10],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[11],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[11],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=i,size=5, shape=18, alpha=0.5)+
  geom_point(data=i,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[12],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[12],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[14],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[14],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[15],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[15],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[16],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[16],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[17],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[17],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[18],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[18],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[19],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[19],],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=i2,size=5, shape=18, alpha=0.5)+
  geom_point(data=i2,size=5.25, shape=5, alpha=0.5)+
  geom_point(data=z[z$Date==old[21],],size=5, shape=18, alpha=0.5)+
  geom_point(data=z[z$Date==old[21],],size=5.25, shape=5, alpha=0.5)+
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
ggsave(plot=plot5, file="UK_Elections/general_polling/plot5.png",width = 30, height = 7.5, type = "cairo-png")

