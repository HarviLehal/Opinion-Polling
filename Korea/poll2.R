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

py_run_file("Korea/data2.py")
poll <- read_csv("Korea/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100

election<-as.Date("03 03 2027", "%d %m %Y")
old <-as.Date("09 03 2022", "%d %m %Y")
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c(
    "#004ea2","#3371b5","#e61e2b","#eb4b55","#b81822","#8a121a","#f39399","#0073cf","#ff7920","#45babd"
  ))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.35,linewidth=0.75, data=d[d$Date!=election,])+
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
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2027 South Korean Presidential Election*')+
  labs(caption = "*Before Nominees are Finalised")

plot1

poll <- read_csv("Korea/poll2.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

plot2<-ggplot(data=d1, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#004ea2","#3371b5","#e61e2b","#eb4b55","#b81822","#8a121a","#f39399",
                               "#0073cf","#ff7920","#45babd" ))+
  geom_text(aes(label = formattable::percent(d1$value, digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 day average')+
  scale_x_discrete(limits = rev(levels(d1$variable)))+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot


ggsave(plot=plot, file="Korea/plot2.png",width = 21, height = 7, type="cairo-png")
ggsave(plot=plot, file="Korea/plot2_wiki.svg",width = 21, height = 7)
aaa=readLines("Korea/plot2_wiki.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Korea/plot2_wiki.svg")