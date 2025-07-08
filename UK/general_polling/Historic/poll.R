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

poll97 <- read_csv("UK/general_polling/Historic/poll97.csv")
poll97<-poll97[poll97$Date==max(poll97$Date),]
poll01 <- read_csv("UK/general_polling/Historic/poll01.csv")
poll01<-dplyr::bind_rows(poll01,poll97)
poll05 <- read_csv("UK/general_polling/Historic/poll05.csv")
poll10 <- read_csv("UK/general_polling/Historic/poll10.csv")
poll15 <- read_csv("UK/general_polling/Historic/poll15.csv")
poll17 <- read_csv("UK/general_polling/Historic/poll17.csv")
poll19 <- read_csv("UK/general_polling/Historic/poll19.csv")
poll24 <- read.csv("UK/general_polling/2024 election/poll.csv")
# poll29 <- read.csv("UK/general_polling/poll.csv")
poll29 <- read_csv("UK/general_polling/unbiased_polls.csv")

# convert poll24 to a tibble
poll24 <- as_tibble(poll24)
poll29 <- as_tibble(poll29)
poll24$Date <- as.Date(poll24$Date, "%Y-%m-%d")
poll29$Date <- as.Date(poll29$Date, "%Y-%m-%d")
# correct poll24 column name for Lib Dem which is currently "Lib.Dem"
names(poll24)[names(poll24) == "Lib.Dem"] <- "Lib Dem"
names(poll29)[names(poll29) == "Lib.Dem"] <- "Lib Dem"

poll<-dplyr::bind_rows(poll01,poll05,poll10,poll15,poll17,poll19,poll24,poll29)

# create list of all polls
polls<-c("poll01","poll05","poll10","poll15","poll17","poll19","poll24","poll29")

d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("01 07 2029", "%d %m %Y")
election<-max(d$Date)+1
mindate<-min(d$Date)
old<-c(as.Date("04 07 2024", "%d %m %Y"),
       as.Date("12 12 2019", "%d %m %Y"),
       as.Date("08 06 2017", "%d %m %Y"),
       as.Date("07 05 2015", "%d %m %Y"),
       as.Date("06 05 2010", "%d %m %Y"),
       as.Date("05 05 2005", "%d %m %Y"),
       as.Date("07 06 2001", "%d %m %Y"),
       as.Date("01 05 1997", "%d %m %Y"))


h3<-reshape2::melt(poll15[1,],id.vars="Date")
h3$value<-as.numeric(h3$value)/100
h3$value<-formattable::percent(h3$value)

h4<-reshape2::melt(poll19[1,],id.vars="Date")
h4$value<-as.numeric(h4$value)/100
h4$value<-formattable::percent(h4$value)

h6<-reshape2::melt(poll17[1,],id.vars="Date")
h6$value<-as.numeric(h6$value)/100
h6$value<-formattable::percent(h6$value)
# GRAPH

#Reshape every poll individually using a for loop
for (i in 1:8){
  assign(paste0("d_",i),reshape2::melt(get(paste0(polls[i])), id.vars="Date"))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=as.numeric(value)/100))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=formattable::percent(value)))
}

#set span for each poll based on range of dates

spans <- c()
  
for (i in 1:8){
  spans[i]<-min(1,1000/as.numeric(max(get(paste0("d_",i))$Date)-min(get(paste0("d_",i))$Date)))
  # if (spans[i]>=1){
  spans[i]<-spans[i]/4
  # }
}
d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 14, Date), mean,na.rm=TRUE))

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#c70000","#0077b6","#e05e00","#6D3177",
                                "#528D6B","#f5dc00","#12B6CF","#222221","#005b54"))+
  geom_line(aes(y = Moving_Average), size=0.75, alpha=0.7)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.8)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.8)+
  geom_point(data=d[d$Date==old[1],],size=5, shape=18, alpha=0.8)+
  geom_point(data=d[d$Date==old[1],],size=5.25, shape=5, alpha=0.8)+
  geom_point(data=h4,size=5, shape=18, alpha=0.8)+
  geom_point(data=h4,size=5.25, shape=5, alpha=0.8)+
  geom_point(data=h6,size=5, shape=18, alpha=0.8)+
  geom_point(data=h6,size=5.25, shape=5, alpha=0.8)+
  geom_point(data=h3,size=5, shape=18, alpha=0.8)+
  geom_point(data=h3,size=5.25, shape=5, alpha=0.8)+
  geom_point(data=d[d$Date==old[5],],size=5, shape=18, alpha=0.8)+
  geom_point(data=d[d$Date==old[5],],size=5.25, shape=5, alpha=0.8)+
  geom_point(data=d[d$Date==old[6],],size=5, shape=18, alpha=0.8)+
  geom_point(data=d[d$Date==old[6],],size=5.25, shape=5, alpha=0.8)+
  geom_point(data=d[d$Date==old[7],],size=5, shape=18, alpha=0.8)+
  geom_point(data=d[d$Date==old[7],],size=5.25, shape=5, alpha=0.8)+
  geom_point(data=d[d$Date==old[8],],size=5, shape=18, alpha=0.8)+
  geom_point(data=d[d$Date==old[8],],size=5.25, shape=5, alpha=0.8)+
  scale_x_date(date_breaks = "1 year", date_labels =  "%Y",limits = c(mindate,election),guide = guide_axis(angle = -90))+
  ggtitle('United Kingdom General Election Opinion Polling Since 1997')

ggsave(plot=plot1, file="UK/general_polling/Historic/plot_modern.png",width = 20, height = 10, type = "cairo-png",limitsize=FALSE)

