library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Polish/Seats/data.py")
poll <- read_csv("Polish/Seats/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
# d$value[d$value=='-'] <- NULL
h <- 231
election<-as.Date("11 11 2027", "%d %m %Y")
old<-min(d$Date)
# MAIN GRAPH

parties<-d[d$variable!='Korona',]
kass<-d[d$variable=='Korona',]
kass<-kass[!is.na(kass$value),]

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#263778","#F68F2D","#1BB100","#851A64","#122746","#a37919"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.75,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=kass)+
  # geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=kass)+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.25,linewidth=0.75, data=parties[parties$Date!=old&parties$Date!=election,])+
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
  geom_hline(aes(yintercept=h), colour="#000000")+
  geom_text(aes((election-5),h,label = "Majority (231 Seats)",hjust=1 ,vjust = -1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 months", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Seat Projection for the Next Polish Parliamentary Election')
plot1


# BAR CHART

poll <- read_csv("Polish/Seats/poll.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-15),]
d1 <- round(colMeans(poll[-1],na.rm=TRUE), digits=0)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")

d2 <- reshape2::melt(d2, id.vars="Date")

d3<-rbind(d2,d1)


plot3<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#7d87ae","#263778","#fabc81","#F68F2D",
                               "#76d066","#1BB100","#b676a2","#851A64",
                               "#717d90","#122746","#c8af75","#a37919"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=ifelse(d3$value<10,-1.45,-0.45), color="#000000",position = position_dodge(0.8), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),hjust=-0.1, color="#000000", position = position_dodge(0.8), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day average \n (2023 Result)')+
  scale_x_discrete(limits = d3$variable[order(d1$value,na.last = FALSE)])+
  coord_flip()
plot3


plotA<-ggarrange(plot1, plot3,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA



ggsave(plot=plotA, file="Polish/Seats/plot.png",width = 20, height = 10, type="cairo-png")

# EXTRA GRAPHIEK


d1$value<-ifelse(is.na(d1$value)==TRUE,0,d1$value)
d2$value<-ifelse(is.na(d2$value)==TRUE,0,d2$value)
d1$value<-d1$value/sum(d1$value,na.rm=TRUE)
d2$value<-d2$value/sum(d2$value,na.rm=TRUE)
d1$Date<-'14 Day Average'
d2$Date<-'2023 Result'

ordered<-c('KO','Trzecia Droga','Lewica','Korona','Konfederacja','PiS')

d1<-d1 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d2<-d2 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d3<-rbind(d1,d2)


plot3a<-ggplot(d3, aes(fill=interaction(rev(Date),variable), y=value, x=Date,label=round(value*460))) + 
  scale_fill_manual(values = c("#fabc81","#F68F2D","#76d066","#1BB100","#b676a2","#851A64",
                               "#c8af75","#a37919","#717d90","#122746","#7d87ae","#263778"))+
  geom_bar(position="fill", stat="identity")+
  geom_text(data=subset(d3,value != 0),size = 5.5, position = position_stack(vjust = 0.5),fontface=ifelse(d3$Date=='2023 Result',"bold.italic","bold"),color="#FFFFFF")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold",color="#000000",size=10),
        axis.text.y = element_text(face="bold.italic",size=15,color="#000000",hjust=1),
        # axis.text.y = element_blank(),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=0.5,alpha=0.25) +
  scale_x_discrete(limits=rev)+
  coord_flip()
plot3a

plot<-ggarrange(plot1, plot3a,ncol = 1, nrow = 2,heights=c(2,0.3))
plot



ggsave(plot=plot, file="Polish/Seats/plot_bloc.png",width = 15, height = 7.5, type = "cairo-png")

