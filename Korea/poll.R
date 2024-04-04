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
library(ggbreak)

py_run_file("Korea/data.py")
poll <- read_csv("Korea/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("10 04 2024", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

e <- d[d$Date!=old,]

e <- e %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=7, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="right"))


plot1<-ggplot(data=e,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#004ea2","#e61e2b","#007c36",
                                "#ff7920","#45babd","#666666"))+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old,])+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_break(c(old+5, as.Date("01 10 2023", "%d %m %Y")))+
  scale_x_date(date_breaks = "1 month", date_labels =  "%m %Y",limits = c(old-15,election+10))
plot1

poll <- read_csv("Korea/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1])
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




plot2<-ggplot(data=d3, aes(x=forcats::fct_rev(variable), y=value,fill=interaction(Date,variable), group=Date )) +
geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#6695c7","#004ea2","#f07880","#e61e2b","#66b086","#007c36",
                               "#ffaf79","#ff7920","#8fd6d7","#45babd","#a3a3a3","#666666"))+
geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),
              y = 0),
          hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
              y = 0),
          hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
theme_minimal()+
theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
      panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
      panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
      plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
ggtitle('7 day average \n (2020 Result)')+
coord_flip()
plot2


plot1a<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))

ggsave(plot=plot1a, file="Korea/plot1.png",width = 15, height = 7.5, type = "cairo-png")






# PR VOTE

poll <- read_csv("Korea/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("10 04 2024", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

e <- d[d$Date!=old,]

e <- e %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=7, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="right"))


plot1<-ggplot(data=e,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#004ea2","#e61e2b","#007c36",
                                "#ff7920","#45babd","#0073cf","#666666"))+
  # geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=old,])+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_break(c(old+5, as.Date("01 09 2023", "%d %m %Y")))+
  scale_x_date(date_breaks = "1 month", date_labels =  "%m %Y",limits = c(old-15,election+10))
plot1

poll <- read_csv("Korea/poll2.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1])
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




plot2<-ggplot(data=d3, aes(x=forcats::fct_rev(variable), y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#6695c7","#004ea2","#f07880","#e61e2b","#66b086","#007c36",
                               "#ffaf79","#ff7920","#8fd6d7","#45babd","#66abe2","#0073cf","#a3a3a3","#666666"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),
                y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d2$value,")"),""),
                y = 0),
            hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 day average \n (2020 Result)')+
  coord_flip()
plot2


plot1a<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot1a
ggsave(plot=plot1a, file="Korea/plot2.png",width = 15, height = 7.5, type = "cairo-png")
