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
library(zoo)
library(tidyverse)
library(data.table)
library(hrbrthemes)
py_run_file("Japan/data.py")
poll <- read_csv("Japan/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("05 10 2027", "%d %m %Y")
election<-min(d$Date)+14
old <-as.Date("28 10 2024", "%d %m %Y")
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#3ca324","#00469c","#ffba00",
                                "#f95580","#b8ce43","#ed008c",
                                "#db001c","#ee7300","#0b80db",
                                "#1ca9e9","#777777"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d)+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  scale_x_date(date_breaks = "2 day", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  # ggtitle('Opinion Polling for the 2024 New Brunswick general election')
  ggtitle('Party Identification for the Next Japanese General Election')



plot1


poll <- read_csv("Japan/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)
d4<-d1
plot2<-ggplot(data=d1, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#3ca324","#00469c","#ffba00",
                               "#f95580","#b8ce43","#ed008c",
                               "#db001c","#ee7300","#0b80db",
                               "#1ca9e9","#777777"))+
  geom_text(aes(label = paste(formattable::percent(d4$value, digits = 2)),
                y = 0),hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",
        axis.title=element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold.italic",size=8.5, color="#000000"),
        plot.title = ggtext::element_markdown(face="bold",lineheight = 1.5),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('*7 Day Average*')+
  scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Japan/plot.png",width = 15, height = 7.5, type="cairo-png")
ggsave(plot=plot, file="Japan/plot.svg",width = 15, height = 7.5)
aaa=readLines("Japan/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Japan/plot.svg")
