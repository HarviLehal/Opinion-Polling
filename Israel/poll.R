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

py_run_file("Israel/data.py")
poll <- read_csv("Israel/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")

election<-as.Date("27 10 2026", "%d %m %Y")
old <-min(d$Date)
d$value[is.na(d$value)]<-0
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#1c5a9f","#1a3581","#00bce0",
                                "#0082b3","#032470","#003066",
                                "#9bc1e3","#0d7a3a","#d51f33",
                                "#ef1520","#1be263","#f66004","#ff4300"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  # scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  ylim(0,45)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "3 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -45))+
  ggtitle('Israeli General Election Seat Projection Since 2022')

plot1

poll <- read_csv("Israel/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>=(max(poll$Date)-7),]
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


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#779cc5","#1c5a9f","#7686b3","#1a3581","#66d7ec","#00bce0",
                               "#66b4d1","#0082b3","#687ca9","#032470","#6683a3","#003066",
                               "#c3daee","#9bc1e3","#6eaf89","#0d7a3a","#e67985","#d51f33",
                               "#f57379","#ef1520","#76eea1","#1be263","#faa068","#f66004","#ff8e66","#ff4300"))+
  geom_text(aes(label = ifelse(d3$Date == max(d3$Date),
                               ifelse(is.na(d3$value)==FALSE,paste(d3$value),"Below Threshold"),
                               ifelse(is.na(d3$value)==FALSE,paste("(",d3$value,")"),
                                      ifelse(d3$variable=='New Hope','(Part of National Unity)',"(Below Threshold)"))),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  # geom_text(aes(label = ifelse(is.na(d3$value), "New", ""),y = 0),
  #           hjust=0, color="#000000",position = position_dodge(1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 14 day average \n (2022 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot


ggsave(plot=plot, file="Israel/plot.png",width = 21, height = 7, type="cairo-png")
