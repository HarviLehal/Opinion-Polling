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

py_run_file("Icelandic_Elections/data.py")
poll <- read_csv("Icelandic_Elections/poll.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
h <- formattable::percent(0.05)

election<-as.Date("27 09 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#41A4DB","#A2D150","#6D9B3F","#EC3E48", "#F8CB3C", "#790581","#EDA823","#3B8F93", "#F13A52"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.6,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_hline(aes(yintercept=h), alpha=0.75, linetype="longdash", colour="#000000")+
  geom_text(aes(election,h,label = "5% Party Threshold", vjust = -1, hjust=1),colour="#56595c")+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)


poll <- read_csv("Icelandic_Elections/poll.csv")
# poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-30),]
d1 <- colMeans(poll[-1])
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)

# GERMAN WIKI
# c("#41A4DB","#A2D150","#6D9B3F","#EC3E48", "#F8CB3C", "#790581","#EDA823","#3B8F93", "#F13A52")
# c("#9ad5ed","#41A4DB","#cfe8a0","#A2D150",
#            "#b0cf93","#6D9B3F","#f79cbc","#EC3E48",
#            "#f7e199","#F8CB3C","#bc65c2","#790581",
#            "#f5d38e","#EDA823","#8dc3c9","#3B8F93",
#            "#f2a29b","#F13A52")


# ENGLISH WIKI
#  c("#46ACEF","#9BF792","#43B776","#D71C47", "#F8CB40", "#8A73BC","#F37F20","#0D2069", "#E24C3E")
# c("#a1d5f7","#46ACEF","#cdfac8","#9BF792",
#            "#97dbb4","#43B776","#eb839d","#D71C47",
#            "#fae39d","#F8CB40","#bfb4de","#8A73BC",
#            "#f7bc8b","#F37F20","#6576b5","#0D2069",
#            "#f2a29b","#E24C3E")


plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#9ad5ed","#41A4DB","#cfe8a0","#A2D150",
                               "#b0cf93","#6D9B3F","#f79cbc","#EC3E48",
                               "#f7e199","#F8CB3C","#bc65c2","#790581",
                               "#f5d38e","#EDA823","#8dc3c9","#3B8F93",
                               "#f2a29b","#F13A52"))+
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(1), size=3.5)+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),
                y = 0),hjust=0, color="#404040", position = position_dodge(1), size=3.5)+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle('30 day average \n (2021 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plot


ggsave(plot=plot, file="Icelandic_Elections/plot.svg",width = 15, height = 7.5)
aaa=readLines("Icelandic_Elections/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Icelandic_Elections/plot.svg")
