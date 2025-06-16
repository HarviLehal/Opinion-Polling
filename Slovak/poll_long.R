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
library(dplyr)

poll1 <- read_csv("Slovak/Old/poll2.csv")
poll2 <- read_csv("Slovak/poll.csv")
poll<-dplyr::bind_rows(poll1,poll2)
# poll <- rbind(poll1,poll2) 
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
next_election<-as.Date("31 12 2028", "%d %m %Y")
election<-as.Date("30 09 2023", "%d %m %Y")
old_election <-min(d$Date)
maxdate<-max(d$Date)+14

d_old <- reshape2::melt(poll1, id.vars="Date")
d_old$value<-as.numeric(d_old$value)/100
d_old$value<-formattable::percent(d_old$value)
d_new <- reshape2::melt(poll2, id.vars="Date")
d_new$value<-as.numeric(d_new$value)/100
d_new$value<-formattable::percent(d_new$value)

d <- d %>%
  mutate(variable = recode(variable, 'OLaNO'  = 'OĽaNOap', Rep='Republika', 'MKP/Alliance'='Aliancia','SPOLU/Dem'='Demokrati'))
d_new <- d_new %>%
  mutate(variable = recode(variable, 'OLaNO'  = 'OĽaNOap', Rep='Republika', 'MKP/Alliance'='Aliancia','SPOLU/Dem'='Demokrati'))
d_old <- d_old %>%
  mutate(variable = recode(variable, 'OLaNO'  = 'OĽaNOap', Rep='Republika', 'MKP/Alliance'='Aliancia','SPOLU/Dem'='Demokrati'))

d<-d[d$variable!='OLaNO',]
d_new<-d_new[d_new$variable!='OLaNO',]
d_old<-d_old[d_old$variable!='OLaNO',]

d<-droplevels(d)
d_new<-droplevels(d_new)
d_old<-droplevels(d_old)



d$variable <- factor(d$variable, levels = c("Smer","PS","Hlas","OĽaNOap","KDH","SASKA","SNS","Republika","Aliancia","Demokrati","SR","ĽSNS","ZL"))

# MAIN GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old_election&d$Date!=election,],alpha=0.25)+
  scale_color_manual(values = c("#c21f1f","#00BDFF","#81163B",
                                "#BED62F","#FFE17C","#78fc04",
                                "#173A70","#e4010a","#f48c1f",
                                "#4D0E90","#034B9F","#005222","#FDBB12"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.35,linewidth=0.75, data=d_old[d_old$Date!=election&d_old$Date!=old_election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d_new[d_new$Date!=election,])+
  # geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=d_new[d_new$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=old_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), max(d$Date)+30)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old_election|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old_election,maxdate),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Slovak Parliamentary Election')
plot1

# poll1 <- read_csv("Slovak/poll2.csv")
# poll1 %>% rename('OĽaNOap'=OLaNO, 'Republika'=Rep, 'Aliancia'='MKP/Aliancia','Demokrati'='SPOLU/Dem')
poll <- read_csv("Slovak/poll.csv")
# poll<-dplyr::bind_rows(poll1,poll2)
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==election,]
poll<-poll[poll$Date>(max(poll$Date)-7),]
d1 <- colMeans(poll[-1],na.rm=TRUE)
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

d3$variable <- factor(d3$variable, levels = c("Smer","PS","Hlas","OĽaNOap","KDH","SASKA","SNS","Republika","Aliancia","Demokrati","SR","ĽSNS"))

plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  
  scale_fill_manual(values = c("#da7979","#c21f1f",
                               "#66d7ff","#00BDFF",
                               "#b37389","#81163B",
                               "#d8e682","#BED62F",
                               "#ffedb0","#FFE17C",
                               "#aefd68","#78fc04",
                               "#7489a9","#173A70",
                               "#ef676c","#e4010a",
                               "#f8ba79","#f48c1f",
                               "#946ebc","#4D0E90",
                               "#6893c5","#034B9F",
                               "#66977a","#005222"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=-0.35, vjust = 0, color="#000000",position = position_dodge(0.7), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),y = 0),
            hjust=-0.1, vjust = 0, color="#404040", position = position_dodge(1.1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('7 day Average \n (2023 Election)')+
  # scale_x_discrete(limits = rev(levels(d3$variable)),labels = label_wrap(8))+
  scale_x_discrete(limits = d3$variable[order(d1$value,d2$value,na.last = FALSE)])+
  coord_flip()


plotA<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA

ggsave(plot=plotA, file="Slovak/plot_long.png",width = 15, height = 7.5, type="cairo-png")
