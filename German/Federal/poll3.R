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
poll <- read_csv("German/Federal/poll3.csv")
Sys.setlocale("LC_ALL", "German")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
# h <- formattable::percent(0.425)
h <- read.csv("German/Federal/poll4.csv")  # this is the majority line, plot it for each poll and join them
h <- reshape2::melt(h, id.vars="Date")
h$value<-as.numeric(h$value)/100
hy<-formattable::percent(h$value[h$Date==min(h$Date)]-0.01)
h$value<-formattable::percent(h$value)
h$Date <- as.Date(h$Date, "%Y-%m-%d")

election<-as.Date("25 03 2029", "%d %m %Y")
old <-min(d$Date)

colss <-c("Rot²-Grün"   ="#770004",
          "GroKo"       ="#005974",
          "Rot-Grün"    ="#DD1529",
          "Jamaika"     ="#509A3A",
          "Deutschland" ="#FBBE00",
          "Kenia"       ="#E5963F",
          "Kiwi"        ="#8EE53F",
          "Rechts"      ="#0489DB",
          "Kemmerich"   ="#AA692F",
          "Brombeer"    ="#792350",
          "Mehrheit"    ="#000000")
# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = colss)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=1.2, data=h, alpha=0.5, linetype="longdash")+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.8,0.05))+
  geom_text(aes(old,hy,label = "Mehrheit", vjust = -1, hjust=1),colour="#000000")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date)-12, election)+
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old-12,election),guide = guide_axis(angle = -90))+
  ggtitle('Wahlumfragen zur nächsten Bundestagswahl nach möglichen Koalitionen')

plot1


d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 7, Date), mean,na.rm=TRUE))


plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = colss)+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.8,0.05))+
  geom_hline(aes(yintercept=max(h$value[h$Date==max(h$Date)])), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,max(h$value[h$Date==max(h$Date)]),label = "Mehrheit", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Wahlumfragen zur nächsten Bundestagswahl nach möglichen Koalitionen')
plot3

poll <- read_csv("German/Federal/poll3.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
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

hx <- read.csv("German/Federal/poll4.csv")
hx$Date <- as.Date(hx$Date, "%Y-%m-%d")
hx<-hx[hx$Date>(max(h$Date)-7),]
hx <- colMeans(hx[-1],na.rm=TRUE)
hx <- reshape2::melt(hx, id.vars="Date")
hx$value<-as.numeric(hx$value)/100
hx$value<-formattable::percent(hx$value, digits = 1)


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
geom_bar(stat="identity",width=0.9, position=position_dodge())+
scale_fill_manual(values = c("#ad6668","#770004","#669bac","#005974",
                             "#eb737f","#DD1529","#96c289","#509A3A",
                             "#fdd866","#FBBE00","#f5bb7b","#Ee8d23",
                             "#bbef8c","#8EE53F","#68b8e9","#0489DB",
                             "#cca582","#AA692F","#af7b96","#792350"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),
                y = 0), hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0), hjust=0, color="#404040", position = position_dodge(1), size=3.5, fontface="bold")+
  geom_hline(aes(yintercept=hx$value), alpha=0.75, linetype="longdash", colour="#000000")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
ggtitle(' Mittelwert des Woches \n (Ergebnisse 2025)')+
scale_x_discrete(limits = d3$variable[order(d1$value,d2$value,na.last = FALSE)])+
coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="German/Federal/plot_coalition.png",width = 21, height = 7, type="cairo-png")

plot<-ggarrange(plot3, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="German/Federal/plot2_coalition.png",width = 21, height = 7, type="cairo-png")


Sys.setlocale("LC_ALL", "English")
