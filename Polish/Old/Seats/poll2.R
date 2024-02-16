library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

poll <- read_csv("Polish/Seats/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
# d$value[d$value=='-'] <- NULL
h <- 231
election<-as.Date("15 10 2023", "%d %m %Y")
old<-min(d$Date)

# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#A2A9B1","#20B2AA","#263778"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  theme(axis.title=element_blank(),legend.title = element_blank())+
  geom_hline(aes(yintercept=h))+
  geom_text(aes((election-5),h,label = "Majority (231 Seats)",hjust=1 ,vjust = -1),colour="#56595c")+
  xlim(old, election)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)
plot

ggsave(plot=plot, file="Polish/Seats/plot2.png",width = 15, height = 7.5, type = "cairo-png")

