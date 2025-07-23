library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)
library(ggpubr)
library(zoo)
library(dplyr)
library(ggbreak)


poll98 <- read_csv("German/Federal/Historic/poll_98.csv")
poll02 <- read_csv("German/Federal/Historic/poll_02.csv")
poll05 <- read_csv("German/Federal/Historic/poll_05.csv")
poll09 <- read_csv("German/Federal/Historic/poll_09.csv")
poll13 <- read_csv("German/Federal/Historic/poll_13.csv")
poll17 <- read_csv("German/Federal/Historic/poll_17.csv")
poll21 <- read_csv("German/Federal/Historic/poll_21.csv")
poll25 <- read_csv("German/Federal/Historic/poll_25.csv")
poll29 <- read_csv("German/Federal/poll.csv")
'%!in%' <- function(x,y)!('%in%'(x,y))

poll <- dplyr::bind_rows(poll98, poll02, poll05, poll09, poll13, poll17, poll21, poll25, poll29)
polls <- c("poll98", "poll02", "poll05", "poll09", "poll13", "poll17", "poll21", "poll25", "poll29")

d <- reshape2::melt(poll, id.vars = "Date")
d$value <- as.numeric(d$value) / 100
d$value <- formattable::percent(d$value)

next_election <- as.Date("30 09 2029", "%d %m %Y")
next_election <- max(d$Date)+14
start <- min(d$Date)

election94 <- as.Date("16 10 1994", "%d %m %Y")
election98 <- as.Date("27 09 1998", "%d %m %Y")
election02 <- as.Date("22 09 2002", "%d %m %Y")
election05 <- as.Date("18 09 2005", "%d %m %Y")
election09 <- as.Date("27 09 2009", "%d %m %Y")
election13 <- as.Date("22 09 2013", "%d %m %Y")
election17 <- as.Date("24 09 2017", "%d %m %Y")
election21 <- as.Date("26 09 2021", "%d %m %Y")
election25 <- as.Date("23 02 2025", "%d %m %Y")

elections <- c(election94, election98, election02, election05, election09, election13, election17, election21, election25, election29)

for (i in 1:9){
  assign(paste0("d_", i), reshape2::melt(get(paste0(polls[i])), id.vars = "Date"))
  assign(paste0("d_", i), get(paste0("d_", i)) %>% mutate(value = as.numeric(value)/100))
  assign(paste0("d_", i), get(paste0("d_", i)) %>% mutate(value = formattable::percent(value)))
}

colss <-c("Union"  ="#005974",
          "AfD"    ="#009EE0",
          "SPD"    ="#DD1529",
          "Grüne"  ="#509A3A",
          "Linke"  ="#B43377",
          "BSW"    ="#792350",
          "FDP"    ="#FBBE00",
          "FW"     ="#f7a800",
          "Piraten"="#ff8800",
          "Others" ="#aaaaaa")

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date%!in%elections,],alpha=0.15)+
  scale_color_manual(values = colss)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.4,linewidth=0.75, data=d_1[d_1$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_2[d_2$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_3[d_3$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_4[d_4$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_5[d_5$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_6[d_6$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_7[d_7$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.1,linewidth=0.75, data=d_8[d_8$Date%!in%elections,],alpha=0.5)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=0.75, data=d_9[d_9$Date%!in%elections,],alpha=0.5)+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.7,0.05))+
  # geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=elections, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date%in%elections,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date%in%elections,],size=5.25, shape=5, alpha=1)+
  xlim(start,next_election)+
  scale_x_date(date_breaks = "1 year", date_labels =  "%Y",limits = c(start,next_election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling since the 1994 German Federal Election')
# plot1


ggsave(plot=plot1, file="German/Federal/Historic/plot.png",width = 25, height = 10, type="cairo-png",limitsize=FALSE)

