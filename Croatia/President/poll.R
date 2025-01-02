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
py_run_file("Croatia/President/data.py")
poll <- read_csv("Croatia/President/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

election<-as.Date("29 12 2024", "%d %m %Y")
old <-min(d$Date)
# MAIN GRAPH

# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=election,],alpha=0.5)+
  scale_color_manual(values = c("#ed1c24","#005baa","#ca9a9a","#c3d746",
                                "#123e90","#aaaaaa","#000000","#e85726"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d[d$Date!=election,])+
  theme_minimal()+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(2.5, 'lines'),
        # legend.position = "none",
        legend.text = element_text(face="bold.italic"),
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold.italic"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  xlim(min(d$Date), election)+
  geom_point(data=d[d$Date==election,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==election,],size=5.25, shape=5, alpha=1)+
  scale_x_date(date_breaks = "1 week", date_labels =  "%d %b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2024-25 Croatian Presidential election (First Round)')
plot <- plot + guides(color = guide_legend(override.aes = list(fill = c("white", "white"), shape = c(NA, NA))))


plot

ggsave(plot=plot, file="Croatia/President/plot.png",width = 15, height = 7.5, type="cairo-png")
