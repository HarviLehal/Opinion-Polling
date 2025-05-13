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
  ggtitle('Opinion Polling for the 2025 South Korean Presidential Election*')+
  labs(caption = "*Finalised Nominees")

plot1

poll <- read_csv("Korea/poll2a.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
# poll[-1]<-data.frame(apply(poll[-1], 2, function(x)
#   as.numeric(sub("%","",as.character(x)))))
poll<-poll[poll$Date>(max(poll$Date)-5),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-ifelse(is.nan(d1$value)==TRUE,0.5,d1$value+0.5)

d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 4)

# d1<-d1[d1$variable!='Cho Kuk',]
# d1<-d1[d1$variable!='Kim Dong-yeon'&d1$variable!='Kim Kyoung-soo'&d1$variable!='Oh Se-hoon'&d1$variable!='Hong Joon-pyo'&d1$variable!='Yoo Seong-min'&d1$variable!='Won Hee-ryong'&d1$variable!='Anh Cheol-soo',]

# d1<-droplevels(d1)

plot2<-ggplot(data=d1, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#004ea2","#e61e2b","#ff7920","#ffcc00","#080b9e","#99c9c9","#c99999","#777777"))+
  geom_text(aes(label = ifelse(d1$value>0.006,paste(formattable::percent(d1$value-0.005, digits = 2)),paste(" ")),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('Latest Poll')+
  # scale_x_discrete(limits = rev(levels(d1$variable)))+
  scale_x_discrete(limits = d1$variable[order(d1$value)])+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot


ggsave(plot=plot, file="Korea/plot2a.png",width = 21, height = 7, type="cairo-png")
ggsave(plot=plot, file="Korea/plot2a_wiki.svg",width = 21, height = 7)
aaa=readLines("Korea/plot2a_wiki.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Korea/plot2a_wiki.svg")

