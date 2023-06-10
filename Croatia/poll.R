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

py_run_file("Croatia/data.py")
poll <- read_csv("Croatia/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("22 07 2024", "%d %m %Y")
old<-min(d$Date)

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#255AAA","#DF262D","#082464","#DC5A2D",
                                "#CBE264","#cc0404","#cc1c74","#05accc",
                                "#e4bc42","#ff931e","#043c7c","#841116",
                                "#bbbdbe","#56595c"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
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
plot
ggsave(plot=plot, file="Croatia/plot.png",width = 15, height = 7.5, type = "cairo-png")



# NEW VERSION

poll2 <- read_csv("Croatia/poll2.csv")
poll2<-poll2[,!names(poll2) %in% c("NS-R", "BM365")]
d <- reshape2::melt(poll2, id.vars="Date")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("22 07 2024", "%d %m %Y")
old<-min(d$Date)

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#255AAA","#DF262D","#082464","#DC5A2D",
                                "#CBE264","#cc0404","#cc1c74","#05accc",
                                "#e4bc42","#ff931e",
                                # "#3cb371","#4a217b",
                                "#043c7c","#841116","#bbbdbe"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
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
plot2
ggsave(plot=plot2, file="Croatia/plot2.png",width = 15, height = 7.5, type = "cairo-png")



# BAR CHART!!
poll <- read_csv("Croatia/poll2.csv")
poll<-poll[,!names(poll) %in% c("NS-R", "BM365")]

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

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)



plot4<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#92add5","#255AAA","#ef9396","#DF262D","#8492b2","#082464","#eead96","#DC5A2D",
                               "#e5f1b2","#CBE264","#e68282","#cc0404","#e68eba","#cc1c74","#82d6e6","#05accc",
                               "#f2dea1","#e4bc42","#ffc98f","#ff931e",
                               # "#9ed9b8","#3cb371","#a590bd","#4a217b",
                               "#829ebe","#043c7c","#c2888b","#841116","#dddedf","#bbbdbe"))+
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
plot2

plot2a<-ggarrange(plot2, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
plot2a
ggsave(plot=plot2a, file="Croatia/plot2a.png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot2a, file="Croatia/plot.svg",width = 15, height = 7.5)
aaa=readLines("Croatia/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Croatia/plot.svg")
