library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("German/State/Thuringia/data.py")
poll <- read_csv("German/State/Thuringia/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)
old <-min(d$Date)
election<-as.Date("01 09 2024", "%d %m %Y")
# MAIN GRAPH

new<-d[d$variable!='BSW',]
new2<-d[d$variable=='BSW',]
new2<-new2[!is.na(new2$value),]

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.75)+
  scale_color_manual(values = c("#BE3075","#009EE0","#000000",
                                "#E3000F","#46962b","#ffed00",
                                "#792350","#A2A9B1"))+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=new[new$Date!=old,])+
  # geom_smooth(method = "lm",formula=y ~ x + I(x^3),fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=old,])+
  geom_smooth(method = "lm",fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(old, election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(aes(yintercept=h), alpha=0.75)+
  geom_text(aes(election,h,label = "5% Party Threshold", vjust = -1, hjust=1),colour="#56595c")
plot1

ggsave(plot=plot1, file="German/State/Thuringia/plot.png",width = 15, height = 7.5, type = "cairo-png")


poll <- read_csv("German/State/Thuringia/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
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




plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#dba2b6","#B43377","#66c5ec","#009EE0",
                               "#6686ad","#10305B","#f08490","#DD1529",
                               "#9bcca1","#509A3A","#fadc7d","#FBBE00",
                               "#af7b96","#792350","#c7cbd0","#A2A9B1"))+
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
  ggtitle('7 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2
plot1<-plot1+theme(legend.position = "none")
plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="German/State/Thuringia/plot2.png",width = 15, height = 7.5, type = "cairo-png")
