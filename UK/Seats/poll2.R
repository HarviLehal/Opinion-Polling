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
election<-as.Date("31 12 2024", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  # geom_point(size=2,data=d) +
  geom_point(size=2,data=d)+
  geom_line()+
  scale_color_manual(values = c("#0884dc","#e8043c","#000000",
                                "#ffa41c","#d46a4c","#005b54",
                                "#25a928","#528D6B","#f8cc2c",
                                "#085cbc","#c83c34","#80041c",
                                "#10b4d4","#999999","#386464"))+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old,])+
  # theme(axis.title=element_blank(),legend.title = element_blank(),
  #       legend.key.size = unit(2, 'lines'),
  #       legend.position = "none",
  #       axis.text.x.top = element_blank(),
  #       axis.ticks.x.top = element_blank(),
  #       axis.line.x.top = element_blank())+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((election-35),h,label = "Majority (326 Seats)",hjust=1 ,vjust = -1),colour="#56595c")+
  # geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  # geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "3 month", date_labels =  "%b %Y",limits = c(old-11,election-35),guide = guide_axis(angle = -90))+
  scale_y_continuous(breaks=seq(0,650,10))+
  # add label for the last point of each line and make the text bold, making sure labels don't overlap
  geom_text(data=d[d$Date==max(d$Date),], aes(label = value), hjust=0, vjust=0, nudge_x = 4, nudge_y = 2, size=3.5, fontface="bold")+
  geom_text(data=d[d$Date==min(d$Date),], aes(label = value), hjust=0, vjust=0, nudge_x = -4, nudge_y = 2, size=3.5, fontface="bold")+
  bbplot::bbc_style()
plot1

# Bar Chart

# poll <- read_csv("UK/Seats/poll2.csv")
# Date <- c(max(poll$Date))
# poll[-1]<-data.frame(apply(poll[-1], 2, function(x)
#   as.numeric(x)))
# d2 <- poll[poll$Date==min(poll$Date),]
# poll<-poll[poll$Date==max(poll$Date),]
# d1 <- as.data.frame(poll)
# # d1 <- t(d1)
# d1 <- cbind(Date, d1)
# d1 <- as.data.frame(d1)
# d1$Date <- as.Date(d1$Date)
# d2 <- as.data.frame(d2)
# 
# d1 <- reshape2::melt(d1, id.vars="Date")
# 
# d2 <- reshape2::melt(d2, id.vars="Date")
# 
# d3<-rbind(d2,d1)
# 
# 
# plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
#   geom_bar(stat="identity",width=0.9, position=position_dodge())+
#   # scale_fill_manual(values = c("#77c0ed","#0087DC","#f27999","#E4003B",
#   #                              "#fcf7c5","#FDF38E","#fcd38b","#FAA61A",
#   #                              "#669d98","#005b54","#9dc7af","#528D6B"))+
#   geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
#             hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
#   geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
#                 y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
#   theme_minimal()+
#   theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
#         panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
#         panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
#         plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
#   ggtitle('60 day average \n (2019 Result)')+
#   scale_x_discrete(limits = rev(levels(d3$variable)))+
#   coord_flip()
# 
# plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
# plot

ggsave(plot=plot1, file="UK/Seats/plot2.png",width = 24, height = 12, type = "cairo-png")
