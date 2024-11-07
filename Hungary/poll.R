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
py_run_file("Hungary/data.py")
poll <- read_csv("Hungary/poll.csv")
Sys.setlocale("LC_ALL", "French")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("3 04 2026", "%d %m %Y")
old <-min(d$Date)
colss <-c("Fidesz"          ="#ff6a00",
          "DK"              ="#0067aa",
          "MSZP"            ="#cc0000",
          "Zöldek"          ="#39b54a",
          "Momentum"        ="#8e6fce",
          "Jobbik"          ="#008371",
          "LMP"             ="#54b586",
          "MHM"             ="#688d1b",
          "MKKP"            ="#808080",
          "TISZA"           ="#ed4551",
          "Other"           ="#aaaaaa",
          "DK–MSZP–Dialogue"="#84cdfc")
# MAIN GRAPH3

split_date1 = as.Date("28 03 2024", "%d %m %Y")
split_date2 = as.Date("19 09 2024", "%d %m %Y")

merge<-d[d$variable!='DK'&d$variable!='MSZP'&d$variable!='Zöldek'&d$variable!='DK–MSZP–Dialogue',]
unmerge<-d[d$variable=='DK'|d$variable=='MSZP'|d$variable=='Zöldek'|d$variable=='DK–MSZP–Dialogue',]
unmerge<-unmerge[!is.na(unmerge$value),]

new<-unmerge[unmerge$Date<split_date1,]                           # Pre Merger
new2<-unmerge[unmerge$Date>split_date1&unmerge$Date<split_date2,] # Merger
new3<-unmerge[unmerge$Date>split_date2,]                          # Post Merger

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = colss)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=merge[merge$Date!=old&merge$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=new[new$Date!=old&new$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=new2[new2$Date!=old&new2$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=new3[new3$Date!=old&new3$Date!=election,])+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Sondages sur les élections législatives hongroises de 2026')



plot1


poll <- read_csv("Hungary/poll.csv")
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
d1<-d1[d1$variable!='DK–MSZP–Dialogue',]
d1<-droplevels(d1)
d2<-d2[d2$variable!='DK–MSZP–Dialogue',]
d2<-droplevels(d2)
d4<-d4[d4$variable!='DK–MSZP–Dialogue',]
d4<-droplevels(d4)
d4$value<-ifelse(is.nan(d4$value)==TRUE,NA,d4$value)
d4$value<-ifelse(d4$value==0.34440000,0.0000000001,d4$value)



plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  # scale_fill_manual(values = c("#d6d6ff","#c2c2ff","#9999ff",
  #                              "#f7c5c3","#f2a7a6","#ea6d6a",
  #                              "#fbdbbf","#f8c8a0","#f4a460",
  #                              "#d6e9bb","#c2df99","#99c955",
  #                              "#dddddd","#cccccc","#aaaaaa"))+
  scale_fill_manual(values = c("#ffa666","#ff6a00",
                               "#66a4cc","#0067aa",
                               "#e06666","#cc0000",
                               "#88d392","#39b54a",
                               "#bba9e2","#8e6fce",
                               "#66b5aa","#008371",
                               "#98d3b6","#54b586",
                               "#a4bb76","#688d1b",
                               "#b3b3b3","#808080",
                               "#f48f97","#ed4551",
                               "#d6d6d6","#BBBBBB"
                               ))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               ifelse(d4$Date == max(d4$Date),
                                      paste(formattable::percent(d4$value, digits = 2, decimal.mark = ",")),
                                      paste(formattable::percent(d4$value, digits = 1, decimal.mark = ","))), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               ifelse(d4$variable=="TISZA",paste("(Nouveau)"),
                                      ifelse(d4$value==0.0000000001,paste("(Membre de EM:",formattable::percent(0.3444, digits = 2, decimal.mark = ","),")"),
                               paste("(",formattable::percent(d4$value, digits = 2, decimal.mark = ","),")"))),""),
                y = 0),hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",
        axis.title=element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold",lineheight = 1.5),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  # ggtitle(' Résultats 2024 <br> Moyenne sur la semaine <br> *(Résultats 2020)*')+
  ggtitle('Moyenne sur la semaine <br> *(Résultats 2022)*')+
  scale_x_discrete(limits = d4$variable[order(d1$value,na.last = TRUE)])+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Hungary/plot.png",width = 15, height = 7.5, type="cairo-png")
Sys.setlocale("LC_ALL", "English")

