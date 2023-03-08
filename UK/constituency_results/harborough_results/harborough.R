library(readr)
library(reshape2)
library(formattable)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)

poll <- read_csv("UK/constituency_results/harborough_results/harborough.csv")
d <- reshape2::melt(poll, id.vars="year")
d$year<-as.Date(d$year, "%d/%m/%Y")
d$value<-formattable::percent(d$value)


# MAIN GRAPH

plot<-ggplot(data=d,aes(x=year,y=value, colour=variable, group=variable)) +
  geom_point(size=2)+
  scale_color_manual(values = c("#0087DC", "#E4003B", "#FAA61A", "#528D6B", "#6D3177", "#DCDCDC"))+
  geom_line(size=1)+
  scale_x_date(name="Date of Election", breaks = unique(d$year), guide = guide_axis(check.overlap = TRUE))+
  theme(axis.text.x=element_text(angle=90,vjust=0.5,hjust=1),panel.grid.minor.x = element_blank())+
  scale_y_continuous(name="Vote", labels = scales::percent_format(accuracy = 1))+
  labs(title="Election Results in Harborough Constituency Between 1885 and 2019")

ggsave(plot=plot, file="UK/constituency_results/harborough_results/plot.png",width = 15, height = 7.5, type = "cairo-png")
