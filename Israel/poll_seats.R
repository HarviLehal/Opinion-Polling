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

poll <- read_csv("Israel/poll.csv")
d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)

d$value <-ifelse(d$value<4,0,d$value)

d <- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 14, Date), mean, na.rm=TRUE)) %>%
  ungroup()


Date<-d$Date
Seats<-d$Moving_Average
Party<-d$variable
data <- data.frame(Date,Seats,Party)
election<-as.Date("27 10 2026", "%d %m %Y")
election<-max(d$Date)
old <-min(d$Date)






plot1<-ggplot(data, aes(x=Date, y=Seats, fill=Party)) + 
  geom_area(alpha=0.95,na.rm=TRUE,position="fill",colour="white",size=0.1)+
  scale_fill_manual(values = c("#1c5a9f","#1a3581","#ff4300",
                               "#00bce0","#0082b3","#032470",
                               "#003066","#9bc1e3","#0d7a3a",
                               "#d51f33","#ef1520","#1be263",
                               "#2d38cf","#f66004","#19a3bd"))+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        # legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Seats",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,1,0.05))+
  # geom_vline(xintercept=election, linetype="solid", color = "#000000", alpha=0.5, size=0.75)+
  geom_hline(yintercept=0.5, linetype="dashed", color = "#000000", size=0.75)+
  geom_vline(xintercept=old, linetype="solid", color = "#000000", alpha=0.5, linewidth=0.75)+
  # geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  # geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(old,election),guide = guide_axis(angle = -90))+
  ggtitle('Israeli General Election Seat Projection Since 2022') 
  plot1

ggsave(plot=plot1, file="Israel/plot_bar.png",width = 15, height = 7.5, type="cairo-png")
