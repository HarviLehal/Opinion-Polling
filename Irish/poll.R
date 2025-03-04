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

py_run_file("Irish/data.py")
poll <- read_csv("Irish/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("01 01 2030", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#74BC64","#729AFF","#39675F","#712C8D","#C11112",
                                "#445225","#3bee56","#45AD6E","#ff0090","#c99999"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d[d$Date!=election,])+
  # geom_smooth(method = "lm",formula=y ~ x+I(x^2) ,fullrange=FALSE,se=FALSE, linewidth=0.75, data=d[d$Date!=election,])+
  # geom_smooth(method = "lm",formula=y ~ x+I(x^2) ,fullrange=FALSE,se=FALSE, linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Irish General Election')
plot1



poll <- read_csv("Irish/poll.csv")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-15),]
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
  scale_fill_manual(values = c("#acd7a2","#74BC64",
                               "#aac2ff","#729AFF",
                               "#88a49f","#39675F",
                               "#aa80bb","#712C8D",
                               "#da7071","#C11112",
                               "#8f977c","#445225",
                               "#89f59a","#3bee56",
                               "#8fcea8","#45AD6E",
                               "#ff66bc","#ff0090",
                               "#dfc2c2","#c99999"))+
  # scale_fill_manual(values = c("#c7e4c1","#acd7a2","#74BC64",
  #                              "#c7d7ff","#aac2ff","#729AFF",
  #                              "#b0c2bf","#88a49f","#39675F",
  #                              "#c6abd1","#aa80bb","#712C8D",
  #                              "#e6a0a0","#da7071","#C11112",
  #                              "#b4baa8","#8f977c","#445225",
  #                              "#b1f8bb","#89f59a","#3bee56",
  #                              "#b5dec5","#8fcea8","#45AD6E",
  #                              "#ff99d3","#ff66bc","#ff0090",
  #                              "#e9d6d6","#dfc2c2","#c99999"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               ifelse(d4$Date == max(d4$Date),
                                      paste(formattable::percent(d4$value, digits = 2)),
                                      paste(formattable::percent(d4$value, digits = 1))), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               paste("(",formattable::percent(d4$value, digits = 2),")"),""),
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
  ggtitle('14 Day Average <br> *(2024 Results)*')+
  # scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  scale_x_discrete(limits = d4$variable[order(d1$value,na.last=FALSE)],labels = label_wrap(8))+
  coord_flip()
plot2

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Irish/plot.png",width = 15, height = 7.5,type="cairo-png")
ggsave(plot=plot, file="Irish/plot.svg",width = 15, height = 7.5)
aaa=readLines("Irish/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Irish/plot.svg")