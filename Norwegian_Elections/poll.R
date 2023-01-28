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
py_run_file("Norwegian_Elections/data.py")
poll <- read_csv("Norwegian_Elections/poll.csv")
d <- melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("01 09 2025", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.5)+
  scale_color_manual(values = c("#D82C3C","#AC347D","#6F9323","#CB182D", "#2D843B", "#236666","#F9DA5A","#3064F1", "#2760A7"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.25,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none")+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)

poll2 <- setDT(poll)
cols <- names(poll2)[-1]
poll2[, paste0(cols, "_30_avg") := 
     lapply(.SD, function(x) fcoalesce(frollmean(x, n=30:1, na.rm=TRUE))), 
   .SDcols = cols]
poll2 <- poll2[,-2:-10]
d2=poll2[poll2$Date==max(poll2$Date),]
colnames(d2)[2] = "R"
colnames(d2)[3] = "SV"
colnames(d2)[4] = "MDG"
colnames(d2)[5] = "Ap"
colnames(d2)[6] = "Sp"
colnames(d2)[7] = "V"
colnames(d2)[8] = "KrF"
colnames(d2)[9] = "H"
colnames(d2)[10] = "FrP"


d2 <- melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value)

plot2<-ggplot(data=d2, aes(x=variable, y=value,fill=variable, group=variable)) +
geom_bar(stat="identity",width=0.8)+
scale_fill_manual(values = c("#D82C3C","#AC347D","#6F9323",
                             "#CB182D","#2D843B","#236666",
                             "#F9DA5A","#3064F1", "#2760A7"))+
geom_text(aes(label=value,y = 0)), hjust=0, color="black",
          position = position_dodge(1), size=3.5)+
theme_minimal()+
theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank())+
ggtitle('30 day average ')+
coord_flip()


plot<-ggarrange(plot1, plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
  

ggsave(plot=plot, file="Norwegian_Elections/plot.svg",width = 15, height = 7.5)
aaa=readLines("Norwegian_Elections/plot.svg",-1)
bbb <- gsub(".svglite ", "", aaa)
writeLines(bbb,"Norwegian_Elections/plot.svg")