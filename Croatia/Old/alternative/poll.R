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

py_run_file("Croatia/alternative/data.py")
poll <- read_csv("Croatia/alternative/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("17 04 2024", "%d %m %Y")
old<-min(d$Date)

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#005baa","#ed1c24","#082464","#e85726",
                                "#c9e265","#cc0000","#cc1c74","#05accc",
                                "#e4bc42","#ff931e","#0cb14b","#02b14b",
                                "#004b88","#043c7c","#841116","#bbbdbe","#56595c"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)
  # geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  # geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
plot1


poll <- read_csv("Croatia/alternative/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
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
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)
# d1 <- sapply(d1, as.character)

plot2<-ggplot(data=d1, aes(x=forcats::fct_rev(variable), y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#005baa","#ed1c24","#082464","#e85726",
                               "#c9e265","#cc0000","#cc1c74","#05accc",
                               "#e4bc42","#ff931e","#0cb14b","#02b14b",
                               "#004b88","#043c7c","#841116","#bbbdbe","#56595c"))+
  geom_text(aes(label = formattable::percent(ifelse(d1$Date != min(d1$Date), d1$value, ""), digits = 1),
                y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(!is.nan(d1$value),paste(d1$value),""),
                y = 0),
            hjust=0, color="#000000", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day average')+
  coord_flip()
plot2

plot1<-plot1+theme(legend.position = "none")

plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot

ggsave(plot=plot, file="Croatia/alternative/plot.png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot, file="Croatia/alternative/plot.svg",width = 15, height = 7.5)
aaa=readLines("Croatia/alternative/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Croatia/alternative/plot.svg")






poll <- read_csv("Croatia/alternative/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
# d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
election<-as.Date("17 04 2024", "%d %m %Y")
old<-min(d$Date)

# LOESS GRAPH

plot1a<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#005baa","#ed1c24","#082464","#e85726",
                                "#c9e265","#cc0000","#cc1c74","#05accc",
                                "#e4bc42","#ff931e","#0cb14b","#02b14b",
                                "#004b88","#043c7c","#841116","#bbbdbe"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.text = element_text(size=16))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)
plot1a

poll <- read_csv("Croatia/alternative/poll2.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
d1 <- colMeans(poll[-1],na.rm = TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)


plot2a<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#669dcc","#005baa","#f4777c","#ed1c24","#6b7ca2","#082464","#f19a7d","#e85726",
                               "#dfeea3","#c9e265","#e06666","#cc0000","#e077ac","#cc1c74","#69cde0","#05accc",
                               "#efd78e","#e4bc42","#ffbe78","#ff931e","#6dd093","#0cb14b","#67d093","#02b14b",
                               "#6693b8","#004b88","#688ab0","#043c7c","#b57073","#841116","#d6d7d8","#bbbdbe"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('14 day average \n (2020 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2a

plot1a<-plot1a+theme(legend.position = "none")

plota<-ggarrange(plot1a, plot2a,ncol = 2, nrow = 1,widths=c(2,0.5))
plota

ggsave(plot=plota, file="Croatia/alternative/plot2.png",width = 15, height = 7.5, type = "cairo-png")
