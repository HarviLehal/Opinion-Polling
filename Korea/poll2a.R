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

py_run_file("Korea/data2a.py")
poll <- read_csv("Korea/poll2a.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100

election<-as.Date("03 06 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1.5, data=d[d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c(
    "#004ea2","#e61e2b","#ff7920","#ffcc00","#080b9e","#99c9c9","#c99999","#777777"
    
  ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.6,linewidth=0.75, data=d[d$Date!=election,])+
  # geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        plot.caption = element_text(hjust = 0,face="italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Finalised Opinion Polling for the 2025 South Korean Presidential Election')

plot1

poll <- read_csv("Korea/poll2a.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
# poll[-1]<-data.frame(apply(poll[-1], 2, function(x)
#   as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==max(poll$Date),]
poll<-poll[poll$Date!=election,]
poll<-poll[poll$Date>(max(poll$Date)-2),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
Date<-Date-1
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d2 <- colMeans(d2[-1],na.rm=TRUE)
d2 <- as.data.frame(d2)
d2 <- t(d2)
Date <- c(election)
d2 <- cbind(Date, d2)
d2 <- as.data.frame(d2)
d1$Date <- as.Date(d1$Date)
d2$Date <- as.Date(d2$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 4)
d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-ifelse(is.nan(d2$value)==TRUE,0.05,d2$value+0.05)
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 4)
d3<-rbind(d1,d2)



plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#6695c7","#004ea2",
                               "#f07880","#e61e2b",
                               "#ffaf79","#ff7920",
                               "#ffe066","#ffcc00",
                               "#6b6dc5","#080b9e",
                               "#c2dfdf","#99c9c9",
                               "#dfc2c2","#c99999",
                               "#adadad","#777777"))+
  # geom_text(aes(label = ifelse(d3$Date==min(d3$Date),
  #                              ifelse(d1$value>0.006,paste(formattable::percent(d1$value-0.005, digits = 2)),paste(" ")),
  #                              ifelse(is.nan(d2$value==TRUE),"",paste(formattable::percent(d2$value, digits = 2))))
  #               
  #               ,y = 0),
  #           hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  # geom_text(aes(label = ifelse(d3$value>0.006,paste(formattable::percent(d2$value-0.005, digits = 2)),paste(" ")),y = 0),
  #           hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date),
                               ifelse(d3$Date == max(d3$Date),ifelse(d3$value<0.0006,"",
                                      paste(formattable::percent(d3$value-0.0005, digits = 2))),
                                      paste(formattable::percent(d3$value, digits = 1))), ""),
                y = 0),hjust=0, color="#000000",position = position_dodge(0.9), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),ifelse(is.nan(d3$value)==TRUE,"",
                               paste("(",formattable::percent(d3$value, digits = 2),")")),""),
                y = 0),hjust=0, color="#000000", position = position_dodge(0.9), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = ggtext::element_markdown(face="bold",lineheight = 1.5),
        plot.caption = element_text(face="italic"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('Results <br> *(2 day average)*')+
  # scale_x_discrete(limits = rev(levels(d1$variable)))+
  scale_x_discrete(limits = d3$variable[order(d2$value,na.last=FALSE)])+
  coord_flip()+
  labs(caption = "*Withdrew and Endorsed Kim Mon-soo")
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot


ggsave(plot=plot, file="Korea/plot2a.png",width = 15, height = 7.5, type="cairo-png")
ggsave(plot=plot, file="Korea/plot2a_wiki.svg",width = 15, height = 7.5)
aaa=readLines("Korea/plot2a_wiki.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Korea/plot2a_wiki.svg")

