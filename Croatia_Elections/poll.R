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

py_run_file("Croatia_Elections/data.py")
poll <- read_csv("Croatia_Elections/poll.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("22 07 2024", "%d %m %Y")
old<-min(d$Date)

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#255AAA","#DF262D","#000000",
                                "#DC5A2D","#CBE264","#326BA4","#CC272C"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot, file="Croatia_Elections/plot.png",width = 15, height = 7.5, type = "cairo-png")



# NEW VERSION

poll2 <- read_csv("Croatia_Elections/poll2.csv")
poll2<-subset(poll2,select=-c(Other))
d <- melt(poll2, id.vars="Date")
d$value<-as.numeric(d$value)
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("22 07 2024", "%d %m %Y")
old<-min(d$Date)

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#255AAA","#DF262D","#a2aab3",
                                "#DC5A2D","#CBE264","#a2aab3"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

ggsave(plot=plot2, file="Croatia_Elections/plot2.png",width = 15, height = 7.5, type = "cairo-png")



# BAR CHART!!
poll <- read_csv("Croatia_Elections/poll2.csv")
poll<-subset(poll,select=-c(Other))
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
d1 <- colMeans(poll[-1])
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- melt(d1, id.vars="Date")
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- melt(d2, id.vars="Date")
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)

plot4<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#83a3d6","#255AAA","#f08d90","#DF262D",
                               "#d0d4d9","#a2aab3","#eda78e","#DC5A2D",
                               "#e6f2ae","#CBE264"))+
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
  ggtitle('30 day average \n (2020 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2<-plot2+theme(legend.position = "none")

plot2a<-ggarrange(plot2, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
ggsave(plot=plot2a, file="Croatia_Elections/plot2a.png",width = 15, height = 7.5, type = "cairo-png")
