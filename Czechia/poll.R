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
library(ggtext)

py_run_file("Czechia/data2.py")
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
parties<-d[d$variable!='AUTO',]
auto<-d[d$variable=='AUTO',]
auto<-auto[!is.na(auto$value),]
colss <-c("SPOLU"    ="#fc6e00",
          "ANO"      ="#5228ba",
          "STAN"     ="#cd0f69",
          "Piráti"   ="#555555",
          "SPD"      ="#0578bc",
          "Trikolora"="#034ea2",
          "Svobodní" ="#009685",
          "PRO"      ="#0b9dc2",
          "PŘÍSAHA"  ="#0033ff",
          "AUTO"     ="#0080c8",
          "SOCDEM"   ="#ff5f61",
          "Stačilo!" ="#c10506",
          "Zelení"   ="#60b44c")
# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = colss)+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=auto[auto$Date!=old&auto$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=parties[parties$Date!=old&parties$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        plot.caption = element_text(hjust = 0,face="bold.italic"),
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
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)
d3 <- as.data.frame(d3)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 2)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d4<-rbind(d1,d2,d3)
d4<-rbind(d1,d2)

plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c(
    "#fda866","#fc6e00",
    "#977ed6","#5228ba",
    "#e16fa5","#cd0f69",
    "#999999","#555555",
    "#69aed7","#0578bc",
    "#6895c7","#034ea2",
    "#66c0b6","#009685",
    "#6dc4da","#0b9dc2",
    # "#f78f91","#f14548",
    "#6685ff","#0033ff",
    "#66b3de","#0080c8",
    "#ff9fa0","#ff5f61",
    "#da696a","#c10506",
    "#a0d294","#60b44c"
    ))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               ifelse(d4$Date == max(d4$Date),ifelse(d4$variable=='Trikolora'|d4$variable=='Svobodní'|d4$variable=='PRO',paste("‡"),
                                      paste(formattable::percent(d4$value, digits = 1, decimal.mark = ","))),
                                      paste(formattable::percent(d4$value, digits = 1, decimal.mark = ","))), ""),
                y = 0),hjust=-0.001, color="#000000",position = position_dodge(0.8), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),ifelse(is.na(d4$value)==TRUE,paste("Nový"),
                                                              ifelse(d4$variable=='STAN'|d4$variable=='Piráti',paste("(",formattable::percent(d4$value,digits=2, decimal.mark = ","),") †"),
                                                              (paste("(",formattable::percent(d4$value,digits=2, decimal.mark = ","),")")))),""),y = 0),
            hjust=-0.001, color="#000000", position = position_dodge(0.8), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold"),
        plot.caption = ggtext::element_markdown(hjust = 0,face="bold.italic"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' Týdenní průměr <br> *(Výsledky 2021)*')+
  scale_x_discrete(limits = d4$variable[order(d1$value,d2$value,na.last = FALSE)])+
  labs(caption = '† Piráti a Starostové <br> ‡ Seskupené Pod SPD')+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Czechia/plot.png",width = 21, height = 7, type="cairo-png")
ggsave(plot=plot, file="Czechia/plot.svg",width = 15, height = 7.5)
aaa=readLines("Czechia/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Czechia/plot.svg")

Sys.setlocale("LC_ALL", "English")
