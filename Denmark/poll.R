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

py_run_file("Denmark/data.py")
poll <- read_csv("Denmark/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.02)

election<-as.Date("31 10 2026", "%d %m %Y")
old <-min(d$Date)

parties<-d[d$variable!='H',]
new<-d[d$variable=='H',]
new<-new[!is.na(new$value),]
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c(
                                # "#ea3d34","#003f8d","#7f1a8d",
                                # "#bb0002","#0365b2","#2eafbb",
                                # "#003c21","#d20047","#ec0088",
                                # "#00424b","#01ff00","#fcd034"
                                  "#c82518","#01438e","#b48cd2",
                                  "#eb94d1","#1272c2","#3fb2be",
                                  "#6b9249","#f7660d","#733280",
                                  "#00505b","#00ff00","#fcd03b","#39c2f7"
                                ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=d[d$Date!=old,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=parties[parties$Date!=old,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=new[new$Date!=old,])+
  # geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=new[new$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "2% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Danish General Election Polling Since 2022')

plot1

poll <- read_csv("Denmark/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
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

d1<-d1[d1$variable!='D',]
d2<-d2[d2$variable!='D',]
d1<-droplevels(d1)
d2<-droplevels(d2)
d3<-rbind(d2,d1)


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c(
                               # "#f28b85","#ea3d34","#668cbb","#003f8d","#b276bb","#7f1a8d",
                               # "#d66667","#bb0002","#68a3d1","#0365b2","#82cfd6","#2eafbb",
                               # "#668a7a","#003c21","#e46691","#d20047","#f466b8","#ec0088",
                               # "#668e93","#00424b","#67ff66","#01ff00","#fde385","#fcd034"
                               "#de7c74","#c82518","#678ebb","#01438e","#d2bae4","#b48cd2",
                               "#f3bfe3","#eb94d1","#71aada","#1272c2","#8cd1d8","#3fb2be",
                               "#a6be92","#6b9249","#faa36e","#f7660d","#ab84b3","#733280",
                               # "#66969d","#00505b",
                               "#66ff66","#00ff00","#fde389","#fcd03b","#88dafa","#39c2f7"
                               ))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),ifelse(is.na(d3$value)==TRUE,paste("(New)"),(paste("(",d3$value,")"))),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(1), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 7 day average \n (2022 Result)')+
  scale_x_discrete(limits = d3$variable[order(d1$value,na.last=FALSE)])+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot


ggsave(plot=plot, file="Denmark/plot.png",width = 21, height = 7, type="cairo-png")
