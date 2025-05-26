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
poll <- read_csv("UK/Subnational/Northern Ireland/poll2.csv")
d <- reshape2::melt(poll, id.vars="Date")

election<-as.Date("27 06 2027", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH


# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old&d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#326760","#d46a4c","#f6cb2f",
                                "#48a5ee","#2aa82c","#0c3a6a",
                                "#8dc63f","#44532a","#e91d50","#AAAAAA"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d[d$Date!=old&d$Date!=election,])+
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
  scale_y_continuous(name="Seats",breaks=seq(0,50,5))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old|d$Date==election,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the Next Northern Ireland Assembly Election')

plot1


poll <- read_csv("UK/Subnational/Northern Ireland/poll2.csv")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(x)))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-14),]
# d1 <- round(colMeans(poll[-1],na.rm=TRUE), digits=0)
# d1 <- as.data.frame(d1)
# d1 <- t(d1)
# d1 <- cbind(Date, d1)
# d1 <- as.data.frame(d1)
# d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)
d1<- as.data.frame(poll)

d1 <- reshape2::melt(d1, id.vars="Date")

d2 <- reshape2::melt(d2, id.vars="Date")

d3<-rbind(d2,d1)


# EXTRA GRAPHIEK


d1$value<-ifelse(is.na(d1$value)==TRUE,0,d1$value)
d2$value<-ifelse(is.na(d2$value)==TRUE,0,d2$value)
d1$value<-d1$value/sum(d1$value)
d2$value<-d2$value/90
d1$Date<-'Polling'
d2$Date<-'Results'

# ordered<-c('Aontú','SF','SDLP','PBP','Green','APNI','UUP','DUP','TUV')
ordered<-c('TUV','DUP','UUP','Other','APNI','Green','PBP','SDLP','SF','Aontú')
ordered<-rev(ordered)
d1<-d1 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d2<-d2 %>%
  mutate(variable =  factor(variable, levels = ordered)) %>%
  arrange(variable)

d3<-rbind(d2,d1)

d3<-rbind(d1,d2)


plot2<-ggplot(d3, aes(fill=interaction(Date,variable), y=value, x=Date,label=round(value*90))) + 
  scale_fill_manual(values = c("#8f987f","#44532a",
                               "#84a4a0","#326760",
                               "#7fcb80","#2aa82c",
                               "#f27796","#e91d50",
                               "#bbdd8c","#8dc63f",
                               "#fae082","#f6cb2f",
                               "#CCCCCC","#AAAAAA",
                               "#91c9f5","#48a5ee",
                               "#e5a694","#d46a4c",
                               "#6d89a6","#0c3a6a"
                               ))+
  geom_bar(position="fill", stat="identity")+
  geom_text(data=subset(d3,value != 0),size = 5.5, position = position_stack(vjust = 0.5),fontface="bold",color="#000000")+
  scale_y_continuous(labels = scales::percent)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),
        axis.text.x = element_text(face="bold",color="#000000",size=10),
        axis.text.y = element_text(face="bold.italic",size=15,color="#000000",hjust=1),
        # axis.text.y = element_blank(),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  geom_hline(yintercept = 0.5,color = "#000000", linetype = "dashed",linewidth=0.5,alpha=0.25) +
  coord_flip()
plot2


plot<-aplot::plot_list(plot1, plot2,ncol = 1, nrow = 2,heights=c(2,0.3))
plot

ggsave(plot=plot, file="UK/Subnational/Northern Ireland/plot2.png",width = 15, height = 7.5, type="cairo-png")

