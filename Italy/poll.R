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
py_run_file("Italy/data.py")
poll <- read_csv("Italy/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.03)

election<-as.Date("22 12 2027", "%d %m %Y")
old <-min(d$Date)
# LOESS GRAPH

new<-d[d$variable!='Libertà'&d$variable!='SUE',]
new2<-d[d$variable=='Libertà'|d$variable=='SUE',]
new2<-new2[!is.na(new2$value),]

# TRUE M5S COLOURS
# "#fdf48c","#fcec3f"
plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.15)+
  scale_color_manual(values = c("#03386a","#ef1c27","#f4c01a","#048404",
                                "#0484dc","#f6d025","#0039aa","#bc3454",
                                "#b41317","#b04e4e","#2149a7","#075271",
                                "#d4448c","#fcd404","#346c9c","#0039aa"))+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.25,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.25,linewidth=0.75, data=new[new$Date!=old,])+
  geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "3% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, linewidth=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
plot1

d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=7, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="right"))



plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.15)+
  scale_color_manual(values = c("#03386a","#ef1c27","#f4c01a","#048404",
                                "#0484dc","#f6d025","#0039aa","#bc3454",
                                "#b41317","#b04e4e","#2149a7","#075271",
                                "#d4448c","#fcd404","#346c9c","#0039aa"))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "3% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
plot3
poll <- read_csv("Italy/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
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
d3<-d3[d3$variable!='IV',]
d3<-d3[d3$variable!='+E',]
d3<-d3[d3$variable!='Italexit',]
d3<-d3[d3$variable!='A-IV',]
d3<-d3[d3$variable!='NM',]
d3<-droplevels(d3)



plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date ))+
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#6888a6","#03386a","#f5777d","#ef1c27","#f8d976","#f4c01a","#68b568","#048404",
                               "#68b5ea","#0484dc","#fae37c","#f6d025","#6688cc","#0039aa","#d78598","#bc3454",
                               "#d27174","#b41317","#d09595","#b04e4e","#7a92ca","#2149a7","#6a97aa","#075271"))+
                               # "#e58fba","#d4448c","#fde568","#fcd404","#85a7c4","#346c9c","#6688cc","#0039aa"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 day average \n (2022 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Italy/plot.png",width = 15, height = 7.5, type="cairo-png")

plot<-ggarrange(plot3, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Italy/plot2.png",width = 15, height = 7.5, type="cairo-png")


