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

py_run_file("South Africa/data.py")
poll <- read_csv("South Africa/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("29 05 2024", "%d %m %Y")
old <-min(d$Date)
new<-d[d$variable!='MKP',]
new2<-d[d$variable=='MKP',]
new2<-new2[!is.na(new2$value),]

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,]) +
  scale_color_manual(values = c("#006600","#005ba6","#56aa48","#852a2a","#ff0000","#ec8713","#009ddf","#05b615"))+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.6,linewidth=0.75, data=new[new$Date!=old&new$Date!=election,])+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=1,linewidth=0.75, data=new2[new2$Date!=old,])+
  geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=old&new2$Date!=election,])+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "6 month", date_labels =  "%b %Y",limits = c(old-64,election),guide = guide_axis(angle = -45))+
  ggtitle('Polling for the 2024 South African General Election')

plot1


# BAR CHART!!
poll <- read_csv("South Africa/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
Date <- c(max(poll$Date))
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
d1$value<-formattable::percent(d1$value, digits = 2)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 2)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 2)

d4<-rbind(d1,d2,d3)
plot4<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#99c299","#66a366","#006600","#99bddb","#669dca","#005ba6",
                               "#bbddb6","#9acc91","#56aa48","#ceaaaa","#b67f7f","#852a2a",
                               "#ff9999","#ff6666","#ff0000","#f7cfa1","#f4b771","#ec8713",
                               "#99d8f2","#66c4ec","#009ddf","#9be2a1","#69d473","#05b615"))+
  geom_text(aes(label = formattable::percent(ifelse(d4$Date != min(d4$Date), d4$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),ifelse(is.na(d4$value)==TRUE,paste("New"),(paste("(",formattable::percent(d4$value,digits=1),")"))),""),y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 2024 Result \n 7 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d4$variable)))+
  coord_flip()


plot<-ggarrange(plot1, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="South Africa/plot.png",width = 15, height = 7.5, type = "cairo-png")
