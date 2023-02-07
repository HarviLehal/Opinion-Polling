library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(ggpubr)

py_run_file("UK_Elections/general_polling/data.py")
poll <- read_csv("UK_Elections/general_polling/poll.csv")
d <- melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(sub("%","",d$value))/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
old<-as.Date("12 12 2019", "%d %m %Y")

starm<-as.Date("04 04 2020", "%d %m %Y")
davey<-as.Date("27 08 2020", "%d %m %Y")
green<-as.Date("01 10 2021", "%d %m %Y")
truss<-as.Date("06 09 2022", "%d %m %Y")
sunak<-as.Date("25 10 2022", "%d %m %Y")
f<-formattable::percent(0.6)
g<-formattable::percent(0.55)

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,]) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_ma(ma_fun=EMA, n = 5,linetype="solid",linewidth=0.75,wilder=TRUE, data=d[d$Date!=old,])+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1)+
  geom_vline(xintercept=davey, linetype="dashed", color = "#FAA61A", alpha=0.5, size=1)+
  geom_vline(xintercept=green, linetype="dashed", color = "#528D6B", alpha=0.5, size=1)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_text(aes(starm,f,label = "Starmer", vjust = -1, angle=-90),colour="#E4003B")+
  geom_text(aes(davey,f,label = "Davey", vjust = -1, angle=-90),colour="#FAA61A")+
  geom_text(aes(green,g,label = "Denyer & Ramsay", vjust = -1, angle=-90),colour="#528D6B")+
  geom_text(aes(truss,f,label = "Truss", vjust = -1, angle=-90),colour="#0087DC")+
  geom_text(aes(sunak,f,label = "Sunak", vjust = -1, angle=-90),colour="#0087DC")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)


ggsave(plot=plot1, file="UK_Elections/general_polling/plot1.png",width = 15, height = 7.5, type = "cairo-png")

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,],alpha=0.5) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF"))+
  geom_smooth(method="loess",fullrange=TRUE,se=TRUE,span=0.075,linewidth=0.75, data=d[d$Date!=old,])+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", alpha=0.5, size=1)+
  geom_vline(xintercept=davey, linetype="dashed", color = "#FAA61A", alpha=0.5, size=1)+
  geom_vline(xintercept=green, linetype="dashed", color = "#528D6B", alpha=0.5, size=1)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", alpha=0.5, size=1)+
  geom_text(aes(starm,f,label = "Starmer", vjust = -1, angle=-90),colour="#E4003B")+
  geom_text(aes(davey,f,label = "Davey", vjust = -1, angle=-90),colour="#FAA61A")+
  geom_text(aes(green,g,label = "Denyer & Ramsay", vjust = -1, angle=-90),colour="#528D6B")+
  geom_text(aes(truss,f,label = "Truss", vjust = -1, angle=-90),colour="#0087DC")+
  geom_text(aes(sunak,f,label = "Sunak", vjust = -1, angle=-90),colour="#0087DC")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot2, file="UK_Elections/general_polling/plot2.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,]) +
  scale_color_manual(values = c("#0087DC","#E4003B","#FAA61A","#FDF38E","#528D6B", "#12B6CF"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.075,linewidth=0.75, data=d[d$Date!=old,])+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=starm, linetype="dashed", color = "#E4003B", size=1)+
  geom_vline(xintercept=davey, linetype="dashed", color = "#FAA61A", size=1)+
  geom_vline(xintercept=green, linetype="dashed", color = "#528D6B", size=1)+
  geom_vline(xintercept=truss, linetype="dashed", color = "#0087DC", size=1)+
  geom_vline(xintercept=sunak, linetype="dashed", color = "#0087DC", size=1)+
  geom_text(aes(starm,f,label = "Starmer", vjust = -1, angle=-90),colour="#E4003B")+
  geom_text(aes(davey,f,label = "Davey", vjust = -1, angle=-90),colour="#FAA61A")+
  geom_text(aes(green,g,label = "Denyer & Ramsay", vjust = -1, angle=-90),colour="#528D6B")+
  geom_text(aes(truss,f,label = "Truss", vjust = -1, angle=-90),colour="#0087DC")+
  geom_text(aes(sunak,f,label = "Sunak", vjust = -1, angle=-90),colour="#0087DC")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5)


ggsave(plot=plot3, file="UK_Elections/general_polling/plot3.png",width =12 , height = 6)



# BAR CHART!!
poll <- read_csv("UK_Elections/general_polling/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
d1 <- colMeans(poll[-1],na.rm = TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)

plot4<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#77c0ed","#0087DC","#f27999","#E4003B",
                               "#fcd38b","#FAA61A","#fcf7c5","#FDF38E",
                               "#9dc7af","#528D6B","#80dae8","#12B6CF"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('30 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()


plot1a<-ggarrange(plot1, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
plot2a<-ggarrange(plot2, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
ggsave(plot=plot1a, file="UK_Elections/general_polling/plot1a.png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot2a, file="UK_Elections/general_polling/plot2a.png",width = 15, height = 7.5, type = "cairo-png")
