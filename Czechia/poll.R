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

py_run_file("Czechia/data.py")
poll <- read_csv("Czechia/poll.csv")
Sys.setlocale("LC_ALL", "Czech")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h1 <- formattable::percent(0.05)
h2 <- formattable::percent(0.08)
h3 <- formattable::percent(0.11)

election<-as.Date("01 10 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c(
    "#004da3","#5228ba","#cd0f69","#555555","#0578bc",
    "#0033ff","#ff5f61","#c10506","#60b44c","#0b9dc2"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=d[d$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        plot.caption = element_text(hjust = 0,face="italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_hline(aes(yintercept=h1), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_hline(aes(yintercept=h2), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_hline(aes(yintercept=h3), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election-5,h1,label = "5% hranice*", vjust = -1, hjust=1),colour="#333333",fontface="italic")+
  geom_text(aes(election-5,h2,label = "8% hranice*", vjust = -1, hjust=1),colour="#333333",fontface="italic")+
  geom_text(aes(election-5,h3,label = "11% hranice*", vjust = -1, hjust=1),colour="#333333",fontface="italic")+
  geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Průzkumy k volbám do Poslanecké sněmovny Parlamentu České republiky 2025')+
  labs(caption = "* 5 % pro jednotlivé strany, resp. 8 % pro dvoučlenné koalice a 11 % pro vícečetné koalice")


plot1


poll <- read_csv("Czechia/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
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
  scale_fill_manual(values = c(
    "#6694c8","#004da3","#977ed6","#5228ba","#e16fa5","#cd0f69","#999999","#555555","#69aed7","#0578bc",
    "#6685ff","#0033ff","#ff9fa0","#ff5f61","#da696a","#c10506","#a0d294","#60b44c","#6dc4da","#0b9dc2"
  ))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=-0.35, color="#000000",position = position_dodge(0.8), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),ifelse(is.na(d3$value)==TRUE,paste("Nový"),(paste("(",formattable::percent(d3$value,digits=1),")"))),""),y = 0),
            hjust=-0.00, color="#000000", position = position_dodge(0.8), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' Týdenní průměr \n (Výsledky 2022)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Czechia/plot.png",width = 21, height = 7, type="cairo-png")

Sys.setlocale("LC_ALL", "English")