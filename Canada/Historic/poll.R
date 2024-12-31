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
library(ggbreak)

poll11 <- read_csv("Canada/Historic/poll_11.csv")
poll15 <- read_csv("Canada/Historic/poll_15.csv")
poll19 <- read_csv("Canada/Historic/poll_19.csv")
poll21 <- read_csv("Canada/Historic/poll_21.csv")
poll25 <- read_csv("Canada/Federal//poll.csv")
'%!in%' <- function(x,y)!('%in%'(x,y))


poll<-dplyr::bind_rows(poll25,poll21,poll19,poll15,poll11)
polls<-c("poll25","poll21","poll19","poll15","poll11")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

next_election<-as.Date("20 10 2025", "%d %m %Y")
start <-min(d$Date)

election08<-as.Date("14 10 2008", "%d %m %Y")
election11<-as.Date("02 05 2011", "%d %m %Y")
election15<-as.Date("19 10 2015", "%d %m %Y")
election19<-as.Date("21 10 2019", "%d %m %Y")
election21<-as.Date("20 10 2021", "%d %m %Y")

elections<-c(election08,election11,election15,election19,election21)

for (i in 1:5){
  assign(paste0("d_",i),reshape2::melt(get(paste0(polls[i])), id.vars="Date"))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=as.numeric(value)/100))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=formattable::percent(value)))
}



plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date%!in%elections,],alpha=0.15)+
scale_color_manual(values = c("#00529F","#D91920",
                              "#EF7B00","#127C73",
                              "#442D7B","#3D9F3B"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_1[d_1$Date%!in%elections,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.05,linewidth=0.75, data=d_2[d_2$Date%!in%elections,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_3[d_3$Date%!in%elections,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_4[d_4$Date%!in%elections,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_5[d_5$Date%!in%elections,])+
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
  geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=elections, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date%in%elections,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date%in%elections,],size=5.25, shape=5, alpha=1)+
  xlim(start,next_election)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(start,next_election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling since the 2008 Canadian Federal Election')
plot1


ggsave(plot=plot1, file="Canada/Historic/plot.png",width = 20, height = 7.5, type="cairo-png")
