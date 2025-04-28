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

poll9 <- read_csv("UK/leadership_approval/Approval/thatcher_net.csv")
poll8 <- read_csv("UK/leadership_approval/Approval/major_net.csv")
poll7 <- read_csv("UK/leadership_approval/Approval/blair_net.csv")
poll6 <- read_csv("UK/leadership_approval/Approval/brown_net.csv")
poll5 <- read_csv("UK/leadership_approval/Approval/cameron.csv")
poll4 <- read_csv("UK/leadership_approval/Approval/may.csv")
poll3 <- read_csv("UK/leadership_approval/Approval/boris.csv")
poll2 <- read_csv("UK/leadership_approval/Approval/truss.csv")
poll1 <- read_csv("UK/leadership_approval/Approval/sunak.csv")
poll <- read_csv("UK/leadership_approval/starmer_approval.csv")

poll9$`Net Approval`<-poll9$`Net Approval`/100
poll8$`Net Approval`<-poll8$`Net Approval`/100
poll7$`Net Approval`<-poll7$`Net Approval`/100
poll6$`Net Approval`<-poll6$`Net Approval`/100
poll5$`Net Approval`<-poll5$`Net Approval`/100
poll4$`Net Approval`<-poll4$`Net Approval`/100

poll3$total <- poll3$Approve+poll3$Disapprove
poll3$Approve <- poll3$Approve/poll3$total
poll3$Disapprove <- poll3$Disapprove/poll3$total
poll3$`Net Approval` <- poll3$Approve-poll3$Disapprove
poll3 <- subset( poll3, select = c(Date,`Net Approval`))

poll2$total <- poll2$Approve+poll2$Disapprove
poll2$Approve <- poll2$Approve/poll2$total
poll2$Disapprove <- poll2$Disapprove/poll2$total
poll2$`Net Approval` <- poll2$Approve-poll2$Disapprove
poll2 <- subset( poll2, select = c(Date,`Net Approval`))

poll1$total <- poll1$Approve+poll1$Disapprove
poll1$Approve <- poll1$Approve/poll1$total
poll1$Disapprove <- poll1$Disapprove/poll1$total
poll1$`Net Approval` <- poll1$Approve-poll1$Disapprove
poll1 <- subset( poll1, select = c(Date,`Net Approval`))

poll$total <- poll$Approval+poll$Disapproval
poll$Approval <- poll$Approval/poll$total
poll$Disapproval <- poll$Disapproval/poll$total
poll$`Net Approval` <- poll$Approval-poll$Disapproval
poll <- subset( poll, select = c(Date,`Net Approval`))


poll$Date<-as.numeric(poll$Date)
poll1$Date<-as.numeric(poll1$Date)
poll2$Date<-as.numeric(poll2$Date)
poll3$Date<-as.numeric(poll3$Date)
poll4$Date<-as.numeric(poll4$Date)
poll5$Date<-as.numeric(poll5$Date)
poll6$Date<-as.numeric(poll6$Date)
poll7$Date<-as.numeric(poll7$Date)
poll8$Date<-as.numeric(poll8$Date)
poll9$Date<-as.numeric(poll9$Date)

# poll$Date<-poll$Date-min(poll$Date)
# poll1$Date<-poll1$Date-min(poll1$Date)
# poll2$Date<-poll2$Date-min(poll2$Date)
# poll3$Date<-poll3$Date-min(poll3$Date)
# poll4$Date<-poll4$Date-min(poll4$Date)
# poll5$Date<-poll5$Date-min(poll5$Date)
# poll6$Date<-poll6$Date-min(poll6$Date)
# poll7$Date<-poll7$Date-min(poll7$Date)

poll$Date<-poll$Date-as.numeric(as.Date("5 7 2024", "%d %m %Y"))
poll1$Date<-poll1$Date-as.numeric(as.Date("25 10 2022", "%d %m %Y"))
poll2$Date<-poll2$Date-as.numeric(as.Date("6 9 2022", "%d %m %Y"))
poll3$Date<-poll3$Date-as.numeric(as.Date("24 7 2019", "%d %m %Y"))
poll4$Date<-poll4$Date-as.numeric(as.Date("13 7 2016", "%d %m %Y"))
poll5$Date<-poll5$Date-as.numeric(as.Date("8 7 2010", "%d %m %Y"))
poll6$Date<-poll6$Date-as.numeric(as.Date("27 6 2007", "%d %m %Y"))
poll7$Date<-poll7$Date-as.numeric(as.Date("2 5 1997", "%d %m %Y"))
poll8$Date<-poll8$Date-as.numeric(as.Date("28 12 1990", "%d %m %Y"))
poll9$Date<-poll9$Date-as.numeric(as.Date("4 5 1979", "%d %m %Y"))


names(poll)[names(poll) == 'Net Approval']<-'Starmer'
names(poll1)[names(poll1) == 'Net Approval']<-'Sunak'
names(poll2)[names(poll2) == 'Net Approval']<-'Truss'
names(poll3)[names(poll3) == 'Net Approval']<-'Johnson'
names(poll4)[names(poll4) == 'Net Approval']<-'May'
names(poll5)[names(poll5) == 'Net Approval']<-'Cameron'
names(poll6)[names(poll6) == 'Net Approval']<-'Brown'
names(poll7)[names(poll7) == 'Net Approval']<-'Blair'
names(poll8)[names(poll8) == 'Net Approval']<-'Major'
names(poll9)[names(poll9) == 'Net Approval']<-'Thatcher'


polls<-dplyr::bind_rows(poll,poll1,poll2,poll3,poll4,poll5,poll6,poll7,poll8,poll9)
d <- reshape2::melt(polls, id.vars="Date")
d$value<-formattable::percent(d$value)


plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_hline(yintercept = 0, size=1.25,colour="#000000",alpha=0.25)+
  geom_point(size=1, data=d,alpha=0.5) +
  scale_color_manual(values = c("#a60000","#f78c6b","#ffd166","#06d6a0","#ef476f",
                                "#073b4c","#911eb4","#118ab2","#f064fc","#009800"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d,alpha=0.75)+
  theme_minimal()+
  theme(
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text("italic"),
        axis.text.x = element_text(face="bold"),
        axis.title.x = element_text(face="bold.italic"),
        axis.text.y = element_text(face="bold"),
        axis.title.y = element_text(face="bold.italic"),
        plot.title = element_text(face="bold.italic"),
        plot.caption = element_text(hjust = 0,face="bold.italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(-1,1,0.05))+
  scale_x_continuous(name="Days",breaks=seq(0,400,10),limits=c(0,400),guide = guide_axis(angle = -90))+
  scale_x_continuous(name="Days",breaks=seq(0,800,20),limits=c(0,800),guide = guide_axis(angle = -90))+
  # scale_x_continuous(name="Days",breaks=seq(0,2300,50),limits=c(0,2300),guide = guide_axis(angle = -90))+
  ggtitle('Net Approval After Becoming Prime Minister')

plot1
  
ggsave(plot=plot1, file="UK/leadership_approval/Approval/PLOT.png",width = 15, height = 7.5, type="cairo-png")
