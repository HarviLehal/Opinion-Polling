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
poll1 <- read_csv("Japan/old/approval/Kishida/poll_approval2.csv")
poll2 <- read_csv("Japan/approval/poll_approval2.csv")
poll<-dplyr::bind_rows(poll2,poll1)
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("29 10 2025", "%d %m %Y")
old <-min(d$Date)
slush<-as.Date("08 12 2023", "%d %m %Y")
abe<-as.Date("08 07 2022", "%d %m %Y")
Ishiba<-as.Date("27 09 2024", "%d %m %Y")
f<-formattable::percent(1)
# MAIN GRAPH

# LOESS GRAPH
d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 9, Date), mean,na.rm=TRUE))


plot1<-ggplot(data=d[d$Date!=old,],aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#3ca324","#db001c"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d[d$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Approval",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.1))+
  geom_vline(xintercept=slush, linetype="dashed", color = "#000000", alpha=0.25, size=1)+
  geom_vline(xintercept=abe, linetype="dashed", color = "#000000", alpha=0.25, size=1)+
  geom_vline(xintercept=Ishiba, linetype="dashed", color = "#000000", alpha=0.25, size=1)+
  geom_text(aes(slush,f,label = "Slush Scandal", vjust = -1,hjust="left", angle=-90),colour="#000000", size=3.5, alpha=0.5)+
  geom_text(aes(abe,f,label = "Abe Assassination", vjust = -1,hjust="left", angle=-90),colour="#000000", size=3.5, alpha=0.5)+
  geom_text(aes(Ishiba,f,label = "Ishiba Elected", vjust = -1,hjust="left", angle=-90),colour="#000000", size=3.5, alpha=0.5)+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(min(d$Date),max(d$Date)),guide = guide_axis(angle = -90))+
  ggtitle('Prime Minister of Japan Approval (Excluding Undecided)')
plot1 

poll1 <- read_csv("Japan/old/approval/Kishida/poll_approval2.csv")
poll2 <- read_csv("Japan/approval/poll_approval2.csv")
poll<-dplyr::bind_rows(poll2,poll1)
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

plot2<-ggplot(data=d1, aes(x=forcats::fct_rev(variable), y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#3ca324","#db001c"))+
  geom_text(aes(label = formattable::percent(ifelse(d1$Date != min(d1$Date), d1$value, ""), digits = 1),
                y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d1$Date == min(d1$Date),paste("(",d1$value,")"),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 day average')+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Japan/approval/plot_approval_reweighted.png",width = 15, height = 7.5, type = "cairo-png")




# NET APPROVAL

poll1 <- read_csv("Japan/old/approval/Kishida/poll_approval_net2.csv")
poll2 <- read_csv("Japan/approval/poll_approval_net2.csv")
poll<-dplyr::bind_rows(poll2,poll1)
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("29 10 2025", "%d %m %Y")
old <-min(d$Date)
f<-0.6
# MAIN GRAPH

# LOESS GRAPH
d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 10, Date), mean,na.rm=TRUE))

plot1<-ggplot(data=d[d$Date!=old,],aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_hline(yintercept = 0, size=1.25,colour="#000000",alpha=0.25)+
  geom_text(aes(Ishiba,f,label = "Ishiba Elected", vjust = -1,hjust="left", angle=-90),colour="#000000", size=4, alpha=0.5,fontface="italic")+
  geom_vline(xintercept=Ishiba, linetype="dashed", color = "#000000", alpha=0.25, size=1.5)+
  geom_point(size=1.25, data=d[d$Date!=old,],alpha=0.5)+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75,alpha=1)+
  scale_color_manual(values = c("#5f3976"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.2,linewidth=0.75, data=d[d$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Approval",labels = scales::percent_format(accuracy = 5L),breaks=seq(-0.9,0.9,0.1))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(min(d$Date),max(d$Date)),guide = guide_axis(angle = -90))+
  ggtitle('Prime Minister of Japan Approval (Excluding Undecided)')
plot1 


ggsave(plot=plot1, file="Japan/approval/plot_approval_reweighted_net.png",width = 15, height = 7.5, type = "cairo-png")

