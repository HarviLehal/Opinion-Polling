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

py_run_file("French/data.py")
poll <- read_csv("French/poll.csv")
Sys.setlocale("LC_ALL", "French")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
# d$value[is.na(d$value)] <- 0
d$value<-formattable::percent(d$value)
start<-as.Date("10 06 2024", "%d %m %Y")
old<-as.Date("19 06 2022", "%d %m %Y")
election<-as.Date("30 06 2024", "%d %m %Y")
f<-formattable::percent(0.6)

d<-d[d$Date>start|d$Date==old,]

# d <- d %>%
#   group_by(variable) %>%
#   arrange(Date) %>%
#   mutate(Moving_Average = rollapply(value, width=3, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="right"))
d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 3, Date), mean,na.rm=TRUE))

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,,],alpha=0.25) +
  scale_color_manual(values = c("#bb0000","#e50241","#ffc0c0",
                                "#ffd600","#0043b0",
                                # "#adc1fd",
                                "#254671",
                                # "#170066",
                                "#393683",
                                # "#404040",
                                "#aaaaaa"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  # geom_rect(aes(xmin = as.Date("31 05 2024", "%d %m %Y"), xmax = as.Date("13 06 2024", "%d %m %Y"), ymin = 0, ymax = 0.6),fill = "palegreen", colour = NA, alpha = 0.5)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.75)+
  scale_x_break(c(old+0.5, start+1))+
  scale_x_date(date_breaks = "2 day", date_labels =  "%d %b %Y",limits = c(old-0.5,election),guide = guide_axis(angle = -90))+
  # ggtitle('Opinion Polling for the 2024 French Legislative Elections')
  ggtitle('Sondages sur les élections législatives françaises de 2024')

# shade region between 31st May and 13 June
plot1



# poll <- read_csv("UK/general_polling/poll.csv")
poll <- read_csv("French/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-3),]
d1 <- colMeans(poll[-1],na.rm = TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)

plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#d66666","#bb0000","#ef678d","#e50241","#ffd9d9","#ffc0c0",
                               "#ffe666","#ffd600","#668ed0","#0043b0",
                               # "#cedafe","#adc1fd",
                               "#7c90aa","#254671",
                               # "#7466a3","#170066",
                               # "#8c8c8c","#404040",
                               "#8886b5","#393683",
                               "#cccccc","#aaaaaa"))+
  
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, vjust = 0, color="#000000",position = position_dodge(0.7), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),y = 0),
            hjust=0, vjust = 0, color="#404040", position = position_dodge(1.1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  # ggtitle(' 3 day average \n (2019 Result)')+
  ggtitle(' Moyenne sur 3 jours \n (Résultats 2022)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2

plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="French/plot.png",width = 20, height = 7.5, type = "cairo-png")
Sys.setlocale("LC_ALL", "English")

