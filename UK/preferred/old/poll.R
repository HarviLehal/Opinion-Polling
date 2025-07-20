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

poll3 <- read_csv("UK/preferred/old/poll3.csv")
poll2 <- read_csv("UK/preferred/old/poll2.csv")
poll1 <- read_csv("UK/preferred/old/poll.csv")
poll0 <- read_csv("UK/preferred/poll.csv")


poll<-dplyr::bind_rows(poll3,poll2,poll1,poll0)

# create list of all polls
polls<-c("poll3","poll2","poll1","poll0")

d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
# d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
f<-formattable::percent(0.9)

next_election<-as.Date("15 10 2029", "%d %m %Y")
next_election<-max(d$Date)+14
election<-as.Date("4 07 2024", "%d %m %Y")
truss<-as.Date("06 09 2022", "%d %m %Y")
sunak<-as.Date("25 10 2022", "%d %m %Y")
baden<-as.Date("02 11 2024", "%d %m %Y")
starm<-as.Date("04 04 2020", "%d %m %Y")
start <-min(d$Date)

colss <-c("Starmer" ="#c70000",
          "Badenoch"="#0066b7",
          "Sunak"   ="#0066b7",
          "Truss"   ="#0066b7",
          "Johnson"   ="#0066b7")

for (i in 1:4){
  assign(paste0("d_",i),reshape2::melt(get(paste0(polls[i])), id.vars="Date"))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=formattable::percent(value)))
}



plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.15)+
  scale_color_manual(values = colss)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.15,linewidth=0.75, data=d_1,alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d_2,alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d_3,alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d_4,alpha=0.5)+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.05))+
  # geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="dashed", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=truss, linetype="solid", color = "#0066b7", alpha=0.5, size=0.75)+
  geom_vline(xintercept=sunak, linetype="solid", color = "#0066b7", alpha=0.5, size=0.75)+
  geom_vline(xintercept=baden, linetype="solid", color = "#0066b7", alpha=0.5, size=0.75)+
  geom_vline(xintercept=starm, linetype="solid", color = "#c70000", alpha=0.5, size=0.75)+
  geom_text(aes(starm-5,f,label = "Starmer", vjust = -1, hjust=0, angle=-90),colour="#c70000")+
  geom_text(aes(truss-5,f,label = "Truss", vjust = -1, hjust=0, angle=-90),colour="#0066b7")+
  geom_text(aes(sunak-5,f,label = "Sunak", vjust = -1, hjust=0, angle=-90),colour="#0066b7")+
  geom_text(aes(baden-5,f,label = "Badenoch", vjust = -1, hjust=0, angle=-90),colour="#0066b7")+
  xlim(start,next_election)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(starm-5,next_election),guide = guide_axis(angle = -90))+
  ggtitle("Preferred Prime Minister Polling (Excluding Don't Knows and Neithers")
plot1

ggsave(plot=plot1, file="UK/preferred/old/plot.png",width = 20, height = 7.5, type = "cairo-png")
