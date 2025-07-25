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
poll <- read_csv("Italy/poll_bloc.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.03)

election<-as.Date("22 12 2027", "%d %m %Y")
EU<-as.Date("09 06 2024", "%d %m %Y")
old <-min(d$Date)
# LOESS GRAPH
new<-d[d$variable!='Libertà'&d$variable!='SUE'&d$variable!='PTD'&d$variable!='Italexit'&d$variable!='AP'&d$variable!='DSP'&d$variable!='ScN'&d$variable!='A-IV',]
new2<-d[d$variable=='Libertà'|d$variable=='SUE'|d$variable=='PTD'|d$variable=='Italexit'|d$variable=='AP'|d$variable=='DSP'|d$variable=='ScN'|d$variable=='A-IV',]
new2<-new2[!is.na(new2$value),]

# TRUE M5S COLOURS
# "#fdf48c","#fcec3f"
plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.15)+
  scale_color_manual(values = c("#03386a","#ef1c27","#0039aa","#d4448c","#e9a513","#b41317","#fcd404","#b04e4e","#075271","#2149a7","#346c9c","#0039aa"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.15,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.075,linewidth=0.75, data=new[new$Date!=old,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=new2[new2$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=EU, linetype="dashed", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, linewidth=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Italian general election')
  
plot1

d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 14, Date), mean,na.rm=TRUE))


plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.15)+
  scale_color_manual(values = c("#03386a","#ef1c27"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=EU, linetype="dashed", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, linewidth=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Italian general election')
plot3


poll <- read_csv("Italy/poll_bloc.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
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



plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date ))+
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#6888a6","#03386a","#f5777d","#ef1c27"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),ifelse(is.na(d3$value)==TRUE,paste("New"),(paste("(",d3$value,")"))),""),y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average \n (2022 Result)')+
  scale_x_discrete(limits = d3$variable[order(d1$value,d2$value,na.last = FALSE)])+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Italy/plot_bloc.png",width = 15, height = 7.5, type="cairo-png")

plot<-ggarrange(plot3, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Italy/plot_bloc2.png",width = 15, height = 7.5, type="cairo-png")


poll <- read_csv("Italy/poll_bloc2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
# d$value<-formattable::percent(d$value)
d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 14, Date), mean, na.rm=TRUE)) %>%
  ungroup() %>%
  mutate(Moving_Average = if_else(
    variable %in% c("A-IV") & is.na(value),
    NA_real_,
    Moving_Average
  ))

Date<-d$Date
Vote<-d$Moving_Average
Party<-d$variable
data <- data.frame(Date,Vote,Party)


rowSums(poll[, -1],na.rm=TRUE)

colss <-c("CDX"     ="#03386a",
          "A"       ="#003dff",
          "IV"      ="#d4448c",
          "PTD"     ="#e9a513",
          "ScN"     ="#b41317",
          "SUE"     ="#fcd404",
          "DSP"     ="#b04e4e",
          "Libertà" ="#075271",
          "AP"      ="#2149a7",
          "Italexit"="#346c9c",
          "A-IV"    ="#0039aa",
          "CSX"     ="#ef1c27")


election<-as.Date("22 12 2027", "%d %m %Y")
EU<-as.Date("09 06 2024", "%d %m %Y")
old <-min(d$Date)


plot1<-ggplot(data, aes(x=Date, y=Vote, fill=Party)) + 
  geom_area(alpha=0.95,na.rm=TRUE,position="fill",colour="white",size=0.1)+
  scale_fill_manual(values = colss)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        # legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_vline(xintercept=EU, linetype="dashed", color = "#000000", alpha=0.5, size=0.75)+
  geom_hline(yintercept=0.5, linetype="dashed", color = "#000000", size=0.75)+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, linewidth=0.75)+
  # geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  # geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('14 Day Bloc Average Polling for the Next Italian general election')
plot1
ggsave(plot=plot1, file="Italy/plot_bloc3.png",width = 15, height = 7.5, type="cairo-png")

