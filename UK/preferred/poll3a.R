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
library(zoo)
library(dplyr)

poll <- read_csv("UK/preferred/poll3a.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")

d$value<-formattable::percent(d$value)
# old<-as.Date("04 07 2024", "%d %m %Y")
old<-min(d$Date)-14
LE25<-as.Date("01 05 2025", "%d %m %Y")
election<-max(d$Date)+14
f<-formattable::percent(0.6)

colss <-c("Starmer" ="#c70000",
          "Badenoch"="#0066b7",
          "Farage"  ="#13bece",
          "Davey"   ="#e05e00",
          "Sunak"   ="#0066b7",
          "Denyer"  ="#33a22b",
          "Adams"   ="#528D6B",
          "None"    ="#999999")

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d)+
  geom_point(size=1.75, data=d,alpha=0.5) +
  scale_color_manual(values=colss)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold.italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=LE25, color = "#000000",linetype="dashed",alpha=0.5, size=0.75)+
  geom_text(aes(LE25,f,label = "Local Elections", vjust = -1, hjust=0, angle=-90),colour="#000000",size=3)+
  scale_x_date(date_breaks = "2 week", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Preferred PM')


plot1

# BAR CHART!!

poll <- read_csv("UK/preferred/poll3a.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
poll<-poll[poll$Date>(max(poll$Date)-14),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
# d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d1<-d1[d1$variable!='Sunak',]
# d1<-d1[d1$variable!='Badenoch',]

d1<-droplevels(d1)

plot2<-ggplot(data=d1, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#c70000","#0077b6","#13bece","#999999"))+
  # geom_text(aes(label = formattable::percent(d1$value, digits = 1),y = 0),
  #           hjust=0.5, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = formattable::percent(d1$value, digits = 1),y = 0),
            hjust=ifelse(d1$value<0,1.8,-0.1), color="#000000",position = position_dodge(1), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  geom_hline(aes(yintercept=0), alpha=1, linewidth=1, linetype="solid", colour="#000000")+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold.italic", hjust = 0, colour="#000000"),
        plot.title = element_text(face="bold.italic", colour="#000000"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 Day Average')+
  scale_x_discrete(limits = d1$variable[order(d1$value,na.last = TRUE)])+
  coord_flip()
plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="UK/preferred/plot3a.png",width = 20, height = 7.5, type = "cairo-png")
