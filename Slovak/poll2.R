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

py_run_file("Slovak/data2.py")
poll <- read_csv("Slovak/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)
g <- formattable::percent(0.07)
f <- formattable::percent(0.10)
election<-as.Date("30 09 2023", "%d %m %Y")
ending<-as.Date("28 02 2024", "%d %m %Y")
old <-as.Date("29 02 2020", "%d %m %Y")


# MAIN GRAPH

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old|d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#BED62F","#FDBB12","#D82222","#034B9F","#005222","#00BDFF",
                                "#4D0E90","#78fc04","#FFE17C","#173A70","#81163B","#000000","#08a454"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_hline(aes(yintercept=g), alpha=0.75, linetype="dashed", colour="#000000")+
  geom_hline(aes(yintercept=f), alpha=0.75, linetype="dotted", colour="#000000")+
  geom_text(aes(election,f,label = "10% Coalition Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_text(aes(election,g,label = "7% Coalition Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_text(aes(election,h,label = "5% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot

ggsave(plot=plot, file="Slovak/plot.svg",width = 15, height = 7.5)
aaa=readLines("Slovak/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Slovak/plot.svg")


# FRENCH

plot_fr<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#BED62F","#FDBB12","#D82222","#034B9F","#005222","#00BDFF",
                                "#4D0E90","#78fc04","#FFE17C","#173A70","#81163B","#000000","#08a454"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_hline(aes(yintercept=g), alpha=0.75, linetype="dashed", colour="#000000")+
  geom_hline(aes(yintercept=f), alpha=0.75, linetype="dotted", colour="#000000")+
  geom_text(aes(election,f,label = "seuil de coalition électorale 10%", vjust = -1, hjust=1),colour="#56595c")+
  geom_text(aes(election,g,label = "seuil de coalition électorale 7%", vjust = -1, hjust=1),colour="#56595c")+
  geom_text(aes(election,h,label = "seuil de parti électoral de 5%", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot_fr
ggsave(plot=plot_fr, file="Slovak/plot_fr.svg",width = 15, height = 7.5)

aaa=readLines("Slovak/plot_fr.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Slovak/plot_fr.svg")




poll <- read_csv("Slovak/poll2.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
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
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d4<-rbind(d1,d2,d3)
# result, average, previous

plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#BED62F","#dfeb97","#cbde59",
                               "#FDBB12","#fedd89","#fdc941",
                               "#D82222","#ec9191","#e04e4e",
                               "#034B9F","#81a5cf","#356fb2",
                               "#005222","#80a991","#33754e",
                               "#00BDFF","#80deff","#33caff",
                               "#4D0E90","#a687c8","#713ea6",
                               "#78fc04","#bcfe82","#93fd36",
                               "#FFE17C","#fff0be","#ffe796",
                               "#173A70","#8b9db8","#45618d",
                               "#81163B","#c08b9d","#9a4562",
                               "#000000","#808080","#333333",
                               "#08a454","#84d2aa","#39b676"))+
  geom_text(aes(label = formattable::percent(ifelse(d4$Date != min(d4$Date), d4$value, ""), digits = 2),
                y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),paste("(",d2$value,")"),""),
                y = 0),
            hjust=0, color="#000000", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' Results \n 7 day Average \n (2020 Election)')+
  scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  coord_flip()

plot<-plot+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")
plotA<-ggarrange(plot, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plotA

ggsave(plot=plotA, file="Slovak/plot_END.png",width = 15, height = 7.5, type="cairo-png")
