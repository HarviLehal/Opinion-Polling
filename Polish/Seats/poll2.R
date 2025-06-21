library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

poll <- read_csv("Polish/Seats/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
# d$value[d$value=='-'] <- NULL
h <- 231
election<-as.Date("11 11 2027", "%d %m %Y")
old<-min(d$Date)
# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#4f2d8f","#20B2AA","#263778"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  geom_hline(aes(yintercept=h), colour="#000000")+
  geom_text(aes((election-5),h,label = "Majority (231 Seats)",hjust=1 ,vjust = -1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 months", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Seat Projection for the Next Polish Parliamentary Election by Coalition')
plot


ggsave(plot=plot, file="Polish/Seats/plot2.png",width = 15, height = 7.5, type = "cairo-png")

