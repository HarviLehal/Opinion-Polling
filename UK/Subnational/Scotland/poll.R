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
library(dplyr)

py_run_file("UK/Subnational/Scotland/data.py")
poll <- read_csv("UK/Subnational/Scotland/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(sub("%","",d$value))/100
d$value[is.nan(d$value)] <- 0
d$value<-formattable::percent(d$value)
old<-as.Date("12 12 2019", "%d %m %Y")
election<-as.Date("04 07 2024", "%d %m %Y")

Carlaw<-as.Date("14 02 2020", "%d %m %Y")
Ross<-as.Date("05 08 2020", "%d %m %Y")
Sarwar<-as.Date("27 02 2021", "%d %m %Y")
Alex<-as.Date("20 08 2021", "%d %m %Y")
Yousaf<-as.Date("29 03 2023", "%d %m %Y")
Swinney<-as.Date("06 05 2024", "%d %m %Y")
f<-formattable::percent(0.6)


# MAIN GRAPH (SCOTTISH WESTMINSTER)

d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapply(value, width=7, FUN=function(x) mean(x, na.rm=TRUE), by=1, by.column=TRUE, partial=TRUE, fill=NA, align="right"))
# d<- d %>%
#   group_by(variable) %>%
#   arrange(Date) %>%
#   mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 30, Date), mean,na.rm=TRUE))


plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.75, data=d[d$Date!=old&d$Date!=election,]) +
  scale_color_manual(values = c("#decb10","#0077b6","#c70000","#e05e00","#33a22b","#13bece"))+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_line(aes(y = Moving_Average), linetype = "solid", size=0.75)+
  geom_vline(xintercept=Sarwar, linetype="dashed", color = "#c70000", alpha=0.5, size=1)+
  geom_vline(xintercept=Alex, linetype="dashed", color = "#e05e00", alpha=0.5, size=1)+
  geom_vline(xintercept=Yousaf, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_vline(xintercept=Swinney, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_vline(xintercept=Carlaw, linetype="dashed", color = "#0077b6", alpha=0.5, size=1)+
  geom_vline(xintercept=Ross, linetype="dashed", color = "#0077b6", alpha=0.5, size=1)+
  geom_text(aes(Sarwar,f,label = "Sarwar", vjust = -1, hjust=0, angle=-90),colour="#c70000")+
  geom_text(aes(Alex,f,label = "Cole-Hamilton", vjust = -1, hjust=0, angle=-90),colour="#e05e00")+
  geom_text(aes(Swinney,f,label = "Swinney", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_text(aes(Yousaf,f,label = "Yousaf", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_text(aes(Carlaw,f,label = "Carlaw", vjust = -1, hjust=0, angle=-90),colour="#0077b6")+
  geom_text(aes(Ross,f,label = "Ross", vjust = -1, hjust=0, angle=-90),colour="#0077b6")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(yintercept = 0, size = 1, colour="#333333")+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle("Opinion Polling for the 2024 United Kingdom General Election In Scotland")
plot1

# LOESS GRAPH

plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.75, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#decb10","#0077b6","#c70000","#e05e00","#33a22b","#13bece"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  geom_vline(xintercept=Sarwar, linetype="dashed", color = "#c70000", alpha=0.5, size=1)+
  geom_vline(xintercept=Alex, linetype="dashed", color = "#e05e00", alpha=0.5, size=1)+
  geom_vline(xintercept=Yousaf, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_vline(xintercept=Swinney, linetype="dashed", color = "#decb10", alpha=0.5, size=1)+
  geom_vline(xintercept=Carlaw, linetype="dashed", color = "#0077b6", alpha=0.5, size=1)+
  geom_vline(xintercept=Ross, linetype="dashed", color = "#0077b6", alpha=0.5, size=1)+
  geom_text(aes(Sarwar,f,label = "Sarwar", vjust = -1, hjust=0, angle=-90),colour="#c70000")+
  geom_text(aes(Alex,f,label = "Cole-Hamilton", vjust = -1, hjust=0, angle=-90),colour="#e05e00")+
  geom_text(aes(Swinney,f,label = "Swinney", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_text(aes(Yousaf,f,label = "Yousaf", vjust = -1, hjust=0, angle=-90),colour="#decb10")+
  geom_text(aes(Carlaw,f,label = "Carlaw", vjust = -1, hjust=0, angle=-90),colour="#0077b6")+
  geom_text(aes(Ross,f,label = "Ross", vjust = -1, hjust=0, angle=-90),colour="#0077b6")+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  geom_hline(yintercept = 0, size = 1, colour="#333333")+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle("Opinion Polling for the 2024 United Kingdom General Election In Scotland")
plot2



# BAR CHART!!
poll <- read_csv("UK/Subnational/Scotland/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d3 <- poll[poll$Date==max(poll$Date),]
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date!=election,]
Date <- c(max(poll$Date))
poll<-poll[poll$Date>(max(poll$Date)-7),]
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
d2$value<-formattable::percent(d2$value, digits = 2)

d3 <- reshape2::melt(d3, id.vars="Date")
d3$value<-as.numeric(d3$value)/100
d3$value<-formattable::percent(d3$value, digits = 2)
d4<-rbind(d1,d2,d3)


plot4<-ggplot(data=d4, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#fbf199","#f9ea66","#f5dc00","#99c9e2","#66add3","#0077b6","#e99999","#dd6666","#c70000",
                               "#f3bf99","#ec9e66","#e05e00","#addaaa","#85c780","#33a22b","#a0e2ec","#80dae8","#12B6CF"))+
  geom_text(aes(label = formattable::percent(ifelse(d4$Date != min(d4$Date), d4$value, ""), digits = 1),y = 0),
            hjust=-0.5, color="#000000",position = position_dodge(0.8), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d4$Date == min(d4$Date),ifelse(is.na(d4$value)==TRUE,paste("New"),(paste("(",formattable::percent(d4$value,digits=1),")"))),""),y = 0),
            hjust=-0.15, color="#404040", position = position_dodge(0.8), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 2024 Result \n 7 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d4$variable)))+
  coord_flip()
plot4

plot1a<-ggarrange(plot1, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
plot2a<-ggarrange(plot2, plot4,ncol = 2, nrow = 1,widths=c(2,0.5))
ggsave(plot=plot1a, file="UK/Subnational/Scotland/plot1_Westminster.png",width = 15, height = 7.5, type = "cairo-png")
ggsave(plot=plot2a, file="UK/Subnational/Scotland/plot2_Westminster.png",width = 15, height = 7.5, type = "cairo-png")
