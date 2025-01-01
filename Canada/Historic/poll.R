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

poll62 <- read_csv("Canada/Historic/poll_62.csv")
poll63 <- read_csv("Canada/Historic/poll_63.csv")
poll65 <- read_csv("Canada/Historic/poll_65.csv")
poll68 <- read_csv("Canada/Historic/poll_68.csv")
poll72 <- read_csv("Canada/Historic/poll_72.csv")
poll74 <- read_csv("Canada/Historic/poll_74.csv")
poll79 <- read_csv("Canada/Historic/poll_79.csv")
poll80 <- read_csv("Canada/Historic/poll_80.csv")
poll84 <- read_csv("Canada/Historic/poll_84.csv")
poll88 <- read_csv("Canada/Historic/poll_88.csv")
poll93 <- read_csv("Canada/Historic/poll_93.csv")
poll97 <- read_csv("Canada/Historic/poll_97.csv")
poll00 <- read_csv("Canada/Historic/poll_00.csv")
poll04 <- read_csv("Canada/Historic/poll_04.csv")
poll06 <- read_csv("Canada/Historic/poll_06.csv")
poll08 <- read_csv("Canada/Historic/poll_08.csv")
poll11 <- read_csv("Canada/Historic/poll_11.csv")
poll15 <- read_csv("Canada/Historic/poll_15.csv")
poll19 <- read_csv("Canada/Historic/poll_19.csv")
poll21 <- read_csv("Canada/Historic/poll_21.csv")
poll25 <- read_csv("Canada/Federal//poll.csv")
'%!in%' <- function(x,y)!('%in%'(x,y))


poll<-dplyr::bind_rows(poll25,poll21,poll19,poll15,poll11,poll08,poll06,poll04,poll00,poll97,poll93,poll88,poll84,poll80,poll79,poll74,poll72,poll68,poll65,poll63,poll62)
polls<-c("poll25","poll21","poll19","poll15","poll11","poll08","poll06","poll04","poll00","poll97","poll93","poll88","poll84","poll80","poll79","poll74","poll72","poll68","poll65","poll63","poll62")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

next_election<-as.Date("20 10 2025", "%d %m %Y")
start <-min(d$Date)

election58<-as.Date("31 03 1958", "%d %m %Y")
election62<-as.Date("18 06 1962", "%d %m %Y")
election63<-as.Date("08 04 1963", "%d %m %Y")
election65<-as.Date("08 11 1965", "%d %m %Y")
election68<-as.Date("25 06 1968", "%d %m %Y")
election72<-as.Date("30 10 1972", "%d %m %Y")
election74<-as.Date("08 07 1974", "%d %m %Y")
election79<-as.Date("22 05 1979", "%d %m %Y")
election80<-as.Date("18 02 1980", "%d %m %Y")
election84<-as.Date("04 09 1984", "%d %m %Y")
election88<-as.Date("21 11 1988", "%d %m %Y")
election93<-as.Date("25 10 1993", "%d %m %Y")
election97<-as.Date("02 06 1997", "%d %m %Y")
election00<-as.Date("27 11 2000", "%d %m %Y")
election04<-as.Date("28 06 2004", "%d %m %Y")
election06<-as.Date("23 01 2006", "%d %m %Y")
election08<-as.Date("14 10 2008", "%d %m %Y")
election11<-as.Date("02 05 2011", "%d %m %Y")
election15<-as.Date("19 10 2015", "%d %m %Y")
election19<-as.Date("21 10 2019", "%d %m %Y")
election21<-as.Date("20 10 2021", "%d %m %Y")

elections<-c(election58,election62,election63,election65,election68,election72,election74,election79,election80,election84,election88, election93,election97,election00,election04,election06,election08,election11,election15,election19,election21)

for (i in 1:21){
  assign(paste0("d_",i),reshape2::melt(get(paste0(polls[i])), id.vars="Date"))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=as.numeric(value)/100))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=formattable::percent(value)))
}



plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date%!in%elections,],alpha=0.15)+
scale_color_manual(values = c("#00529F","#D91920",
                              "#EF7B00","#127C73",
                              "#442D7B","#3D9F3B",
                              "#5f9ea0","#9999ff"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_1[d_1$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_2[d_2$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_3[d_3$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_4[d_4$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_5[d_5$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d_6[d_6$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d_7[d_7$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=d_8[d_8$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_9[d_9$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_10[d_10$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_11[d_11$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_12[d_12$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_13[d_13$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1.0,linewidth=0.75, data=d_14[d_14$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_15[d_15$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.6,linewidth=0.75, data=d_16[d_16$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=d_17[d_17$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.6,linewidth=0.75, data=d_18[d_18$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.6,linewidth=0.75, data=d_19[d_19$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1.0,linewidth=0.75, data=d_20[d_20$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1.0,linewidth=0.75, data=d_21[d_21$Date%!in%elections,],alpha=0.5)+
  
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=elections, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date%in%elections,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date%in%elections,],size=5.25, shape=5, alpha=1)+
  xlim(start,next_election)+
  scale_x_date(date_breaks = "1 year", date_labels =  "%Y",limits = c(start,next_election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling since the 1958 Canadian Federal Election')
# plot1


ggsave(plot=plot1, file="Canada/Historic/plot.png",width = 15, height = 7.5, type="cairo-png")

