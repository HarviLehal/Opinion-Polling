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

poll <- read_csv("Polish/President/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)

old<-min(d$Date)
election2<-as.Date("18 05 2025", "%d %m %Y")
election<-as.Date("01 06 2025", "%d %m %Y")
# election<-max(d$Date)+14
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#263778","#F68F2D"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        # legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold.italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election2, linetype="dashed", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "4 days", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  guides(color = guide_legend(override.aes = list(fill = c("white", "white"), shape = c(NA, NA))))+
  ggtitle('Head-to-Head Opinion Polling for the 2025 Polish Presidential Election (Excluding Don\'t knows and Abstains)')
plot1

ggsave(plot=plot1, file="Polish/President/plot.svg",width = 15, height = 7.5)
aaa=readLines("Polish/President/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Polish/President/plot.svg")

plot1<-plot1 +   theme(legend.position = "none")

poll <- read_csv("Polish/President/poll2.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
poll<-poll[poll$Date>(max(poll$Date)-14),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)
d1$value<-formattable::percent(d1$value, digits = 1)

plot2<-ggplot(data=d1, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#263778","#F68F2D"))+
  geom_text(aes(label = formattable::percent(d1$value, digits = 1),y = 0),
            hjust=-0.1, color="#000000",position = position_dodge(1), size=3.5, fontface="bold.italic")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold.italic"),
        plot.title = element_text(face="bold.italic"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 Day Average')+
  scale_x_discrete(limits = d1$variable[order(d1$value,na.last = FALSE)])+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot
ggsave(plot=plot, file="Polish/President/plot2.png",width = 15, height = 7.5, type = "cairo-png")
