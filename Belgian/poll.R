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
library(dplyr)

py_run_file("Belgian/data.py")
poll <- read_csv("Belgian/poll_vlaanderen.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("09 06 2024", "%d %m %Y")
old <-min(d$Date)

# VLAANDEREN
#e0b917 <- #f9ce19 (original) VB
#e6ce00 <- #ffe500 (original) n-va
plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old|d$Date!=election,],alpha=0.75)+
  scale_color_manual(values = c("#e0b917","#e6ce00","#ff6200",
                                "#0087dc","#ff2900","#01796f","#8b0000"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)

plot1

# BAR
poll <- read_csv("Belgian/poll_vlaanderen.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
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

plot1a<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#ecd574","#e0b917","#f0e266","#e6ce00",
                               "#ffa166","#ff6200","#66b7ea","#0087dc",
                               "#ff7f66","#ff2900","#67afa9","#01796f",
                               "#b96666","#8b0000"))+
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
  ggtitle('30 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot1b<-ggarrange(plot1, plot1a,ncol = 2, nrow = 1,widths=c(2,0.5))


ggsave(plot=plot1b, file="Belgian/plot_vlaanderen.png",width = 15, height = 7.5, type="cairo-png")




# WALLONIE

poll <- read_csv("Belgian/poll_wallonie.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("09 06 2024", "%d %m %Y")
old <-min(d$Date)


plot2<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old|d$Date!=election,],alpha=0.75)+
  scale_color_manual(values = c("#ff0000","#0047ab","#5aad39",
                                "#8b0000","#40e0d0","#dd0081"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)

plot2

# BAR
poll <- read_csv("Belgian/poll_wallonie.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
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
  scale_fill_manual(values = c("#ff6666","#ff0000","#6691cd","#0047ab",
                               "#9cce88","#5aad39","#b96666","#8b0000",
                               "#8cece3","#40e0d0","#eb66b3","#dd0081"))+
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
  ggtitle('30 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2b<-ggarrange(plot2, plot2a,ncol = 2, nrow = 1,widths=c(2,0.5))

ggsave(plot=plot2b, file="Belgian/plot_wallonie.png",width = 15, height = 7.5, type="cairo-png")



# BRUSSEL

poll <- read_csv("Belgian/poll_brussel.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("09 06 2024", "%d %m %Y")
old <-min(d$Date)


plot3<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old|d$Date!=election,],alpha=0.75)+
  scale_color_manual(values = c("#5aad39","#ff0000","#0047ab",
                                "#8b0000","#dd0081","#40e0d0",
                                "#e0b917","#0087dc","#e6ce00",
                                "#ff6200","#01796f","#ff2900"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)

plot3

# BAR
poll <- read_csv("Belgian/poll_brussel.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
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

plot3a<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#9cce88","#5aad39","#ff6666","#ff0000","#6691cd","#0047ab",
                               "#b96666","#8b0000","#eb66b3","#dd0081","#8cece3","#40e0d0",
                               "#ecd574","#e0b917","#66b7ea","#0087dc","#f0e266","#e6ce00",
                               "#ffa166","#ff6200","#67afa9","#01796f","#ff7f66","#ff2900"))+
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
  ggtitle('30 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot3b<-ggarrange(plot3, plot3a,ncol = 2, nrow = 1,widths=c(2,0.5))


ggsave(plot=plot3b, file="Belgian/plot_brussel.png",width = 15, height = 7.5, type="cairo-png")



# SEATS

poll <- read_csv("Belgian/seats.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
election<-as.Date("09 06 2024", "%d %m %Y")
old <-min(d$Date)


plot4<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.75)+
  scale_color_manual(values = c("#e0b917","#ff0000","#e6ce00",
                                "#0047ab","#5aad39","#ff6200",
                                "#0087dc","#8b0000","#ff2900",
                                "#01796f","#40e0d0","#dd0081"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)

plot4
ggsave(plot=plot4, file="Belgian/plot_seats.png",width = 15, height = 7.5, type="cairo-png")


# COALITION

poll <- read_csv("Belgian/seats_coalition.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
election<-as.Date("09 06 2024", "%d %m %Y")
old <-min(d$Date)


plot5<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.75)+
  scale_color_manual(values = c("#8b0000","#01796f","#ff0000",
                                "#0047ab","#ff6200","#e0b917","#e6ce00"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.45,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election,
             linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)

plot5

# BAR CHART

poll <- read_csv("Belgian/seats_coalition.csv")
Date <- c(max(poll$Date))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
# poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
#   as.numeric(x)))
d1 <- round(colMeans(poll[-1],na.rm = TRUE), digits=0)
d1 <- as.data.frame(d1)
d1[d1 == 0] <- 1   # ADDS 1 TO PARTY WITH 0 SEATS BUT REMOVE IF SUM OF PARTIES >150
sum(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2[-1]<-lapply(d2[-1],as.numeric)

d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d2 <- reshape2::melt(d2, id.vars="Date")
d2$value[is.na(d2$value)] <- 0 # FIXES 0 SEATS OLD ELECTION PARTIES

d3<-rbind(d2,d1)

plot6<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#b96666","#8b0000","#67afa9","#01796f",
                               "#ff6666","#ff0000","#6691cd","#0047ab",
                               "#ffa166","#ff6200","#ecd574","#e0b917",
                               "#f0e266","#e6ce00"))+
  geom_text(aes(label = ifelse(d3$Date != min(d3$Date), d3$value, ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('30 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()

plotA<-ggarrange(plot5, plot6,ncol = 2, nrow = 1,widths=c(2,0.5))
ggsave(plot=plotA, file="Belgian/plot_coalition.png",width = 15, height = 7.5, type="cairo-png")
