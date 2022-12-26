library(readr)
<<<<<<< HEAD
poll <- read_csv("harborough results/harborough.csv")
=======
poll <- read_csv("harborough.csv")
>>>>>>> 6edf762f7db247814e386accb8c0204e9728c104
library(reshape2)
d <- melt(poll, id.vars="year")
d$year<-as.Date(d$year, "%d/%m/%Y")
library(formattable)
d$value<-formattable::percent(d$value)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)

# MAIN GRAPH

ggplot(data=d,aes(x=year,y=value, colour=variable, group=variable)) +
  geom_point(size=2)+
  scale_color_manual(values = c("#0087DC", "#E4003B", "#FAA61A", "#528D6B", "#6D3177", "#DCDCDC"))+
  geom_line(size=1)+
  scale_x_date(name="Date of Election", breaks = unique(d$year), guide = guide_axis(check.overlap = TRUE))+
  theme(axis.text.x=element_text(angle=90,vjust=0.5,hjust=1),panel.grid.minor.x = element_blank())+
  scale_y_continuous(name="Vote", labels = scales::percent_format(accuracy = 1))+
  labs(title="Election Results in Harborough Constituency Between 1885 and 2019")
