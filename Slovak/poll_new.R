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

py_run_file("Slovak/data3.py")
poll <- read_csv("Slovak/poll_new.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)
g <- formattable::percent(0.07)
f <- formattable::percent(0.10)
election<-as.Date("31 12 2028", "%d %m %Y")
old <-min(d$Date)


# MAIN GRAPH

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#D82222","#00BDFF","#81163B",
                                "#BED62F","#FFE17C","#78fc04",
                                "#173A70","#e4010a","#f48c1f",
                                "#4D0E90","#034B9F","#005222"))+
  # geom_smooth(method="gam",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=d[d$Date!=old,])+
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
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
plot

# ggsave(plot=plot, file="Slovak/plot_new.png",width = 15, height = 7.5, type="cairo-png")



poll <- read_csv("Slovak/poll_new.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
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
# result, average, previous

plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#e87a7a","#D82222",
                               "#66d7ff","#00BDFF",
                               "#b37389","#81163B",
                               "#d8e682","#BED62F",
                               "#ffedb0","#FFE17C",
                               "#aefd68","#78fc04",
                               "#7489a9","#173A70",
                               "#ef676c","#e4010a",
                               "#f8ba79","#f48c1f",
                               "#946ebc","#4D0E90",
                               "#6893c5","#034B9F",
                               "#66977a","#005222"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),
                y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day Average \n (2023 Election)')+
  scale_x_discrete(limits = rev(levels(d3$variable)),labels = label_wrap(8))+
  coord_flip()

plot<-plot+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")
plotA<-ggarrange(plot, plot2,ncol = 2, nrow = 1,widths=c(2,0.6))
plotA

ggsave(plot=plotA, file="Slovak/plot_new.png",width = 15, height = 7.5, type="cairo-png")
