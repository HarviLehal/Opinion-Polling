library(readr)
library(reshape2)
library(formattable)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)

poll <- read_csv("UK/constituency_results/leicester_east_results/leicester_east.csv")
d <- reshape2::melt(poll, id.vars="year")
d$year<-as.Date(d$year, "%d/%m/%Y")
d$value<-formattable::percent(d$value)


# MAIN GRAPH

plot<-ggplot(data=d,aes(x=year,y=value, colour=variable, group=variable)) +
  # geom_rect(aes(xmin = as.Date("23 02 1950", "%d %m %Y"), xmax = as.Date("28 02 1974", "%d %m %Y"), ymin = 0, ymax = 0.8),fill = "grey", colour = NA, alpha = 0.5)+
  geom_point(size=2)+
  scale_color_manual(values = c("#0087DC", "#E4003B", "#FAA61A",'#FFF890','#000080','#7D26CD',"#528D6B",'#303c74',"#6D3177",'#12B6CF', "#8c8c8c"))+
  geom_line(size=1)+
  scale_x_date(name="Date of Election", breaks = unique(d$year), guide = guide_axis(check.overlap = TRUE))+
  theme_minimal()+
  theme(axis.title=element_blank(),
        legend.title = element_blank(),
        legend.key.size = unit(0.45,'lines'),
        legend.box.margin = margin(t = 0, r = 0, b = 0, l = -15, unit = "pt"),
        axis.text.x = element_text(angle=90,vjust=0.5,hjust=1,size=7,face="bold"),
        axis.text.y = element_text(size=7,face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        panel.grid.minor.x = element_blank(),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  labs(title="Election Results in the Leicester East Constituency for 1918-1950 and 1974-2024")
plot

ggsave(plot=plot, file="UK/constituency_results/leicester_east_results/plot.png",width = 20, height = 7.5, type = "cairo-png")
