library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(ggpubr)

py_run_file("Lithuanian/data.py")
poll <- read_csv("Lithuanian/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("06 10 2024", "%d %m %Y")
old<-min(d$Date)
g<-formattable::percent(0.05)
h<-formattable::percent(0.07)

new<-d[d$variable!='NA',]
new2<-d[d$variable=='NA',]
new2<-new2[!is.na(new2$value),]
# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#3DA49A","#319032","#2D568C","#D41720",
                                "#D6136E","#E98313","#711625","#C2312F",
                                "#369C3A","#F3BB0C","#221DC1","#f25d23"))+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.5,linewidth=0.75, data=new[new$Date!=old,])+
  geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(aes(yintercept=g), alpha=0.75, linetype="dashed", colour="#000000")+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="dotted", colour="#000000")+
  geom_text(aes(election,g,label = "5% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_text(aes(election,h,label = "7% Coalition Threshold", vjust = -1, hjust=1),colour="#56595c")
  
ggsave(plot=plot, file="Lithuanian/plot.png",width = 15, height = 7.5, type = "cairo-png")
 


# BAR CHART!!
poll <- read_csv("Lithuanian/poll.csv")
# poll<-subset(poll,select=-c(Other))
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
# poll[-1][is.na(poll[-1])] <- 0
# d2[-1][is.na(d2[-1])] <- 0
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

plot4<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#90d1cb","#3DA49A","#85c785","#319032","#83a0c7","#2D568C","#eb8188","#D41720",
                               "#eb81b2","#D6136E","#f5bf84","#E98313","#b86e7c","#711625","#e08d90","#C2312F",
                               "#8ccf8f","#369C3A","#fadc84","#F3BB0C","#6c6aba","#221DC1","#f79e7b","#f25d23"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value,""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),ifelse(is.na(d3$value)==TRUE,paste("New"),(paste("(",d3$value,")"))),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background= element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill="#FFFFFF",color="#FFFFFF"))+
  ggtitle('30 day average \n (2020 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()

plot<-plot+theme(legend.position = "none")
plot2<-ggarrange(plot, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
plot2
ggsave(plot=plot2, file="Lithuanian/plot2.png",width = 15, height = 7.5, type = "cairo-png")

ggsave(plot=plot2, file="Lithuanian/plot.svg",width = 15, height = 7.5)
aaa=readLines("Lithuanian/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Lithuanian/plot.svg")
