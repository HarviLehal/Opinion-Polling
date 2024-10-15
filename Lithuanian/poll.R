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
election<-as.Date("13 10 2024", "%d %m %Y")
old<-min(d$Date)
g<-formattable::percent(0.05)
h<-formattable::percent(0.07)

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#3DA49A","#319032","#2D568C","#D41720",
                                "#D6136E","#E98313","#711625","#C2312F",
                                "#369C3A","#F3BB0C","#4e4acd","#f25d23"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(aes(yintercept=g), alpha=0.75, linetype="dashed", colour="#000000")+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="dotted", colour="#000000")+
  geom_text(aes(old+14,g,label = "5% Party Threshold", vjust = -0.5, hjust=0),colour="#000000", fontface="italic", alpha=0.5,size=3.5)+
  geom_text(aes(old+14,h,label = "7% Coalition Threshold", vjust = -0.5, hjust=0),colour="#000000", fontface="italic", alpha=0.5,size=3.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2024 Lithuanian Parliamentary Election')
plot1
  
 


# BAR CHART!!
poll <- read_csv("Lithuanian/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date)-1)
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-14),]
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
d2$value<-formattable::percent(d2$value, digits = 1)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 1)

d4<-rbind(d1,d2,d3)




plot2<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#b1dbd7","#8bc8c2","#3DA49A","#add3ad","#83bc84","#319032","#abbbd1","#819aba","#2D568C","#eea2a6","#e57479","#D41720",
                               "#efa1c5","#e671a8","#D6136E","#f6cda1","#f2b571","#E98313","#c6a2a8","#aa737c","#711625","#e7adac","#da8382","#C2312F",
                               "#afd7b0","#86c489","#369C3A","#fae49e","#f8d66d","#F3BB0C","#d3d2f3","#a7a5e6","#4e4acd","#fabea7","#f79e7b","#f25d23"))+
  geom_text(aes(label = ifelse(d4$Date != min(d4$Date),ifelse(d4$Date == max(d4$Date),paste(formattable::percent(d4$value, digits = 2)),paste(formattable::percent(d4$value, digits = 1))), ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),
                               ifelse(is.na(d4$value)==TRUE,"(New)",
                                      (paste("(",formattable::percent(d4$value, digits = 1),")"))),""),y = 0),
            hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('Results <br> 14 day Average <br> *(2020 Election)*')+
  scale_x_discrete(limits = rev(levels(d4$variable)),labels = label_wrap(8))+
  coord_flip()

# plot<-plot+theme(legend.position = "none")
plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Lithuanian/plot.png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot1, file="Lithuanian/plot2.png",width = 15, height = 7.5, type = "cairo-png")

ggsave(plot=plot, file="Lithuanian/plot.svg",width = 15, height = 7.5)
aaa=readLines("Lithuanian/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Lithuanian/plot.svg")
