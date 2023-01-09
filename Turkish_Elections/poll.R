library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("Turkish_Elections/data.py")
poll <- read_csv("Turkish_Elections/poll.csv")
# z = length(poll$Date)
# for (i in 1:z){
#   print( i)
#   if (nchar(poll$Date[i]) < 10) {
#     print(nchar(poll$Date[i]))
#     poll$Date[i] <- paste("15 ", poll$Date[i])
#   }
# }


d <- melt(poll, id.vars="Date")
# d$Date<-as.Date(d$Date, "%d %b %Y")
# d$value<-as.numeric(sub("%","",d$value))/100
# d$value[is.nan(d$value)] <- 0
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("18 06 2023", "%d %m %Y")
old<-min(d$Date)

# MAIN GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=old,],alpha=0.75)+
  scale_color_manual(values = c("#FFCC00","#951b88","#3db5e6","#870000","#006aa7", "#2db34a" ,"#ff5f5f","#0d5ca6","#ed1c24"))+
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.3,linewidth=0.75, data=d[d$Date!=old,])+
  # bbplot::bbc_style()+
  xlim(old, election)+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  theme(axis.title=element_blank(),legend.title = element_blank())+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)

ggsave(plot=plot, file="Turkish_Elections/plot.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS

