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
# new<-d[d$variable!='OĽaNO-ZĽ',]
# new2<-d[d$variable=='OĽaNO-ZĽ',]
# new2<-new2[!is.na(new2$value),]

# MAIN GRAPH

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#485454","#BED62F","#FDBB12","#D82222","#034B9F","#005222","#00BDFF",
                                "#4D0E90","#78fc04","#FFE17C","#173A70","#81163B","#000000","#08a454"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=new[new$Date!=old,])+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=1,linewidth=0.75, data=new2[new2$Date!=old,])+
  # bbplot::bbc_style()+
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

ggsave(plot=plot, file="Slovak/plot.svg",width = 15, height = 7.5)
aaa=readLines("Slovak/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Slovak/plot.svg")


# FRENCH

plot_fr<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#485454","#BED62F","#FDBB12","#D82222","#034B9F","#005222","#00BDFF",
                                "#4D0E90","#78fc04","#FFE17C","#173A70","#81163B","#000000","#08a454"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=new[new$Date!=old,])+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=1,linewidth=0.75, data=new2[new2$Date!=old,])+
  # bbplot::bbc_style()+
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
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
plot_fr
ggsave(plot=plot_fr, file="Slovak/plot_fr.svg",width = 15, height = 7.5)

aaa=readLines("Slovak/plot_fr.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Slovak/plot_fr.svg")

