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
library(dplyr)

poll <- read_csv("UK/Subnational/Scotland/poll3.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
old<-as.Date("06 05 2021", "%d %m %Y")

Alex<-as.Date("20 08 2021", "%d %m %Y")
Yousaf<-as.Date("29 03 2023", "%d %m %Y")
Swinney<-as.Date("06 05 2024", "%d %m %Y")
f<-formattable::percent(0.6)


# MAIN GRAPH (SCOTTISH HOLYROOD)

d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=14, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="right"))

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old,]) +
  scale_color_manual(values = c("#decb10","#0087DC","#E4003B","#FAA61A","#528D6B"))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  geom_vline(xintercept=Alex, linetype="dashed", color = "#FAA61A", alpha=0.5, size=1)+
  geom_vline(xintercept=Yousaf, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_vline(xintercept=Swinney, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_text(aes(Alex,f,label = "Cole-Hamilton", vjust = -1, hjust=0, angle=-90),colour="#FAA61A")+
  geom_text(aes(Yousaf,f,label = "Yousaf", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_text(aes(Swinney,f,label = "Swinney", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(yintercept = 0, size = 1, colour="#333333")+
  ggtitle("Scottish Parliamentary Polling - Constituency Vote")


# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5) +
  scale_color_manual(values = c("#decb10","#0087DC","#E4003B","#FAA61A","#528D6B"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  bbplot::bbc_style()+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=Alex, linetype="dashed", color = "#FAA61A", alpha=0.5, size=1)+
  geom_vline(xintercept=Yousaf, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_vline(xintercept=Swinney, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_text(aes(Alex,f,label = "Cole-Hamilton", vjust = -1, hjust=0, angle=-90),colour="#FAA61A")+
  geom_text(aes(Yousaf,f,label = "Yousaf", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_text(aes(Swinney,f,label = "Swinney", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(yintercept = 0, size = 1, colour="#333333")+
  ggtitle("Scottish Parliamentary Polling - Constituency Vote")



# BAR CHART!!
poll <- read_csv("UK/Subnational/Scotland/poll3.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
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
  scale_fill_manual(values = c("#ede480","#decb10","#77c0ed","#0087DC",
                               "#f27999","#E4003B","#fcd38b","#FAA61A","#9dc7af","#528D6B"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average \n (2021 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()


plot1a<-ggarrange(plot1, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
plot2a<-ggarrange(plot2, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
ggsave(plot=plot1a, file="UK/Subnational/Scotland/plot1_Holyrood_Constituency .png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot2a, file="UK/Subnational/Scotland/plot2_Holyrood_Constituency .png",width = 15, height = 7.5, type = "cairo-png")
