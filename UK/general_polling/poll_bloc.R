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
library(ggbreak)

poll <- read_csv("UK/general_polling/poll_bloc.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)
d$value<-formattable::percent(d$value)
old <-min(d$Date)
election<-max(d$Date)
election<-as.Date("15 08 2029", "%d %m %Y")

d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 14, Date), mean,na.rm=TRUE))
# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#c70000","#f5dc00","#e05e00","#0077b6"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=d[d$Date!=old,])+
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
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_hline(yintercept=0,alpha=0)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.8,0.05))+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "1 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Left-Right Polling for the Next United Kingdom General Election (Excl. Regional Parties)')

plot1

# BAR CHART

poll <- read_csv("UK/general_polling/poll_bloc.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-formattable::percent(d2$value, digits = 1)
d1$Date<-'Polling'
d2$Date<-'Election'
d3<-rbind(d2,d1)



plot2<-ggplot(d3, aes(fill=interaction(Date,variable), y=value, x=Date)) + 
  scale_fill_manual(values = c("#dd6666","#c70000",
                               "#f9ea66","#f5dc00",
                               "#ec9e66","#e05e00",
                               "#66add3","#0077b6"
  ))+
  geom_bar(position="fill", stat="identity")+
  geom_text(aes(label = ifelse(d3$Date==max(d3$Date),ifelse(d3$variable=="Left (Lab+Green)",paste("Left\n(Lab+Green):\n",d3$value),ifelse(d3$variable=="Right (Con+Ref)",paste("Right\n(Con+Ref):\n",d3$value),ifelse(d3$variable=="Lib Dem",paste("Lib Dem:\n",d3$value),paste("Nat\n(SNP+PC):\n",d3$value)))),
                               ifelse(d3$variable=="Left (Lab+Green)",paste("Left\n(Lab+Green):\n",d3$value),ifelse(d3$variable=="Right (Con+Ref)",paste("Right\n(Con+Ref):\n",d3$value),ifelse(d3$variable=="Lib Dem",paste("Lib Dem:\n",d3$value),paste("Nat \n(SNP+PC):\n",d3$value))))),
                hjust=0.5, vjust = 0.5,y = ifelse(d3$variable=="Left (Lab+Green)",0.89,ifelse(d3$variable=="Right (Con+Ref)",0.11,ifelse(d3$variable=="Nat (SNP+PC)",ifelse(d3$Date==min(d3$Date),0.55,0.64),ifelse(d3$Date==min(d3$Date),0.45,0.56))))),
            color="#000000",position =, size=5, fontface="bold")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold.italic",size=15),
        plot.title = ggtext::element_markdown(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=1,alpha=0.75) +
  coord_flip()

plot2


plotA<-ggarrange(plot1, plot2,ncol = 1, nrow = 2,heights=c(2,0.55))
plotA





ggsave(plot=plotA, file="UK/general_polling/plot_bloc.png",width = 20, height = 10, type="cairo-png")

