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

poll <- read_csv("UK/leadership_approval/starmer_approval_long.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
old<-min(d$Date)
elect<-as.Date("04 07 2024", "%d %m %Y")
elect2<-elect+(Sys.Date()-as.Date("04 07 2024", "%d %m %Y"))
election<-max(d$Date)+14
f<-formattable::percent(0.6)



plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#33a22b","#c70000"
  ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.15,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.8,0.05))+
  geom_hline(aes(yintercept=0.5), alpha=0.5, linewidth=1, linetype="dashed", colour="#000000")+
  geom_vline(xintercept=elect, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=elect2, linetype="solid", color = "#000000", alpha=0.75, size=0.75)+
  geom_text(aes(elect2,f,label = "Current Point", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  geom_text(aes(elect,f,label = "Election", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  scale_x_date(date_breaks = "2 months", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  geom_hline(yintercept = 0, size = 1, colour="#333333",alpha=0)+
  geom_hline(yintercept = 0.9, size = 1, colour="#333333",alpha=0)+
  ggtitle('Keir Starmer Approval Rating')

ggsave(plot=plot1, file="UK/leadership_approval/plot_starmer_long_v1.png",width = 20, height = 7.5, type = "cairo-png")

plot1

# BAR CHART!!

poll <- read_csv("UK/leadership_approval/starmer_approval_long.csv")
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
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)


plot2<-ggplot(data=d1, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#33a22b","#c70000"
  ))+
  # geom_text(aes(label = formattable::percent(d1$value, digits = 1),y = 0),
  #           hjust=0.5, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = formattable::percent(d1$value, digits = 1),y = 0),
            hjust=ifelse(d1$value<0,1.1,-0.1), color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  geom_hline(aes(yintercept=0), alpha=1, linewidth=1, linetype="solid", colour="#000000")+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold", hjust = 0),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average')+
  scale_x_discrete(limits = rev(levels(d1$variable)))+
  coord_flip()
plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="UK/leadership_approval/plot_starmer_long.png",width = 20, height = 7.5, type = "cairo-png")
