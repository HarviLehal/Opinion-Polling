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
library(zoo)
library(tidyverse)
library(data.table)
library(hrbrthemes)
py_run_file("Japan/approval/data.py")
poll <- read_csv("Japan/approval/poll_approval.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

# old <-min(d$Date)
f<-formattable::percent(0.9)
# MAIN GRAPH

# LOESS GRAPH



plotwiki<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d,alpha=0.5)+
  scale_color_manual(values = c("#3ca324","#db001c","#666666"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        # legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Approval",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.9,0.05))+
  # scale_x_date(date_breaks = "2 day", date_labels =  "%d %b %Y",limits = c(min(d$Date)-2,max(d$Date)+10),guide = guide_axis(angle = -90))+
  scale_x_date(date_breaks = "2 week", date_labels =  "%d %b %Y",limits = c(min(d$Date),max(d$Date)),guide = guide_axis(angle = -90))+
  ggtitle('Ishiba Cabinet Approval')
plotwiki
ggsave(plot=plotwiki, file="Japan/approval/plot_wiki.svg",width = 15, height = 7.5)
aaa=readLines("Japan/approval/plot_wiki.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Japan/approval/plot_wiki.svg")

poll <- read_csv("Japan/approval/poll_approval.csv")
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

plot2<-ggplot(data=d1, aes(x=forcats::fct_rev(variable), y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#3ca324","#db001c","#666666"))+
  geom_text(aes(label = formattable::percent(ifelse(d1$Date != min(d1$Date), d1$value, ""), digits = 1),
                y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d1$Date == min(d1$Date),paste("(",d1$value,")"),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  coord_flip()+
  ggtitle('7 day average')
plot2


plot<-ggarrange(plotwiki, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Japan/approval/plot_approval.png",width = 15, height = 7.5, type = "cairo-png")




# NET APPROVAL

poll <- read_csv("Japan/approval/poll_approval_net.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)


# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_hline(yintercept = 0, size=1.25,colour="#000000",alpha=0.25)+
  geom_point(size=2, data=d,alpha=1)+
  scale_color_manual(values = c("#999999","#5f3976"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Approval",labels = scales::percent_format(accuracy = 5L),breaks=seq(-0.9,0.9,0.1))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # scale_x_date(date_breaks = "2 day", date_labels =  "%d %b %Y",limits = c(min(d$Date)-2,max(d$Date)+10),guide = guide_axis(angle = -90))+
  scale_x_date(date_breaks = "1 months", date_labels =  "%b %Y",limits = c(min(d$Date)-2,max(d$Date)+20),guide = guide_axis(angle = -90))+
  ggtitle('Ishiba Cabinet Net Approval')
plot1 


ggsave(plot=plot1, file="Japan/approval/plot_approval_net.png",width = 15, height = 7.5, type = "cairo-png")
