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
library(ggtext)

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
                                "#792350","#888888"))+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.35,linewidth=0.75, data=d[d$Date!=old,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.35,linewidth=0.75, data=new[new$Date!=old,])+
  # geom_smooth(method = "lm",formula=y ~ I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=old,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=new2[new2$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(aes(yintercept=h), alpha=0.75,linetype="dashed",colour="#000000")+
  geom_text(aes(old+4,h,label = "5% Party Threshold", vjust = -1, hjust=0),colour="#000000", alpha=0.75)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2024 Thuringian State Election')
plot1

ggsave(plot=plot1, file="German/State/Thuringia/plot.png",width = 15, height = 7.5, type = "cairo-png")


poll <- read_csv("German/State/Thuringia/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
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




plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#e2b5c5","#d285ad","#B43377","#85d1f0","#66c5ec","#009EE0",
                               "#859ebd","#70839d","#10305B","#f39da6","#eb737f","#DD1529",
                               "#afd6b4","#96c289","#509A3A","#fbe397","#fdd866","#FBBE00",
                               "#bf95ab","#af7b96","#792350","#c6c6c6","#b8b8b8","#888888"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),
                               paste(formattable::percent(d4$value, digits = 1)), ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               ifelse(is.na(d4$value)==TRUE,"(New)",
                                      (paste("(",formattable::percent(d4$value, digits = 1),")"))),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold"),
        # plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' Results <br> 7 day Average <br> *(2019 Election)*')+
  scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  coord_flip()
plot2
# plot1<-plot1+theme(legend.position = "none")
plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="German/State/Thuringia/plot2.png",width = 15, height = 7.5, type = "cairo-png")
