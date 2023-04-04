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

# py_run_file("Finnish/data.py")
poll <- read_csv("Finnish/poll.csv")
election<-as.Date("02 04 2023", "%d %m %Y")
results <- data.frame("Date"= election,
                      "SDP"=19.9,
                      "PS"=20.1,
                      "KOK"=20.8,
                      "KESK"=11.3,
                      "VIHR"=7.0,
                      "VAS"=7.1,
                      "SFP"=4.3,
                      "KD"=4.2,
                      "LIIK"=2.4)
poll <- rbind(results,poll)
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
title<-"Polls of Parties and Results(98.1% counted)"
title2<- "Sums of Government and Opposition Polls and Results(98.1% counted)"

old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[(d$Date != old) & (d$Date != election), ],alpha=0.5)+
  scale_color_manual(values = c("#E84F4F","#FADF56","#246188","#489A27", "#226844", "#E21B67","#FADD93","#1B34A5", "#AA247A"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.4,linewidth=0.75, data=d[(d$Date != old) & (d$Date != election), ])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  ggtitle(title)+
  theme(plot.title = element_text(hjust = 0.5))

ggsave(plot=plot, file="Finnish/plot.png",width = 15, height = 7.5,type="cairo-png")



poll2 <- read_csv("Finnish/poll2.csv")
Government <- sum(results$SDP,results$KESK,results$VIHR,results$VAS,results$SFP)
Oppposition <- sum(results$PS,results$KOK,results$KD,results$LIIK)
results2 <- data.frame("Date"= election,
                      "Government"= Government,
                      "Opposition"= Oppposition)
poll2 <- rbind(results2,poll2)
d <- reshape2::melt(poll2, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("02 04 2023", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[(d$Date != old) & (d$Date != election), ],alpha=0.5)+
  scale_color_manual(values = c("#E84F4F","#246188"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.4,linewidth=0.75, data=d[(d$Date != old) & (d$Date != election), ])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  # geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  ggtitle(title2)+
  theme(plot.title = element_text(hjust = 0.5))

ggsave(plot=plot, file="Finnish/plot2.png",width = 15, height = 7.5,type="cairo-png")
