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
library(ggbreak)

py_run_file("Bulgaria/data3.py")
poll00<-read_csv("Bulgaria/poll0.csv")
poll0 <- read_csv("Bulgaria/poll.csv")
poll1 <- read_csv("Bulgaria/poll1.csv")
poll2 <- read_csv("Bulgaria/poll2.csv")
poll3 <- read_csv("Bulgaria/poll3.csv")
poll4 <- read_csv("Bulgaria/poll4.csv")
poll5 <- read_csv("Bulgaria/poll5.csv")
poll6 <- read_csv("Bulgaria/poll6.csv")
poll<-dplyr::bind_rows(poll00,poll0,poll1,poll2,poll3,poll4,poll5,poll6)

d <- reshape2::melt(poll, id.vars="Date")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)

future_election<-max(d$Date)+60
next_election<-as.Date("27 10 2024", "%d %m %Y")
election0<-as.Date("09 06 2024", "%d %m %Y")
election1<-as.Date("02 04 2023", "%d %m %Y")
election2<-as.Date("02 10 2022", "%d %m %Y")
election3<-as.Date("14 11 2021", "%d %m %Y")
election4<-as.Date("11 07 2021", "%d %m %Y")
election5<-as.Date("04 04 2021", "%d %m %Y")
election6<-min(d$Date)

d_00 <- reshape2::melt(poll00, id.vars="Date")
d_00$value<-as.numeric(d_00$value)/100
d_00$value<-formattable::percent(d_00$value)

d_0 <- reshape2::melt(poll0, id.vars="Date")
d_0$value<-as.numeric(d_0$value)/100
d_0$value<-formattable::percent(d_0$value)

d_1 <- reshape2::melt(poll1, id.vars="Date")
d_1$value<-as.numeric(d_1$value)/100
d_1$value<-formattable::percent(d_1$value)

d_2 <- reshape2::melt(poll2, id.vars="Date")
d_2$value<-as.numeric(d_2$value)/100
d_2$value<-formattable::percent(d_2$value)

d_3 <- reshape2::melt(poll3, id.vars="Date")
d_3$value<-as.numeric(d_3$value)/100
d_3$value<-formattable::percent(d_3$value)

d_4 <- reshape2::melt(poll4, id.vars="Date")
d_4$value<-as.numeric(d_4$value)/100
d_4$value<-formattable::percent(d_4$value)

d_5 <- reshape2::melt(poll5, id.vars="Date")
d_5$value<-as.numeric(d_5$value)/100
d_5$value<-formattable::percent(d_5$value)

d_6 <- reshape2::melt(poll6, id.vars="Date")
d_6$value<-as.numeric(d_6$value)/100
d_6$value<-formattable::percent(d_6$value)
colss <-c("GERB"      ="#0054a6",
          "DPS"       ="#0066b7",
          `PP-DB`     ="#4200ff",
          "V"         ="#c09f62",
          "MECh"      ="#1a2c44",
          "BSP"       ="#db0f28",
          "ITN"       ="#4bb9de",
          "Velichie"  ="#ad1c20",
          "Other"     ="#999999",
          "APS"       ="#6147aa",
          `DPS–NN`    ="#0066b7",
          "BV"        ="#197032",
          "Levitsata" ="#ba1034",
          "PP"        ="#ffc300",
          "DB"        ="#004a80",
          "ISMV"      ="#ba1034",
          "OP"        ="#009b75")

# MAIN GRAPH
new<-d_0[d_0$variable!='DPS–NN'&d_0$variable!='APS',]
new2<-d_0[d_0$variable=='DPS–NN'|d_0$variable=='APS',]
new2<-new2[!is.na(new2$value),]

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=1, data=d[d$Date!=election1 & d$Date!=election2 & d$Date!=election3 & d$Date!=election4 & d$Date!=election5 & d$Date!=election0,])+
  scale_color_manual(values =colss)+
  # geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=d_00)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d_00[d_00$Date!=election0&d_00$Date!=next_election,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d_0[d_0$Date!=election1&d_0$Date!=election0,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d_0[d_0$Date!=election1&d_0$Date!=election0,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=new[new$Date!=election1&new$Date!=election0,])+
  # geom_smooth(method = "lm",formula=y ~ I(x^2) ,fullrange=FALSE,se=FALSE, linewidth=0.75, data=new2[new2$Date!=next_election&new2$Date!=election0,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.7,linewidth=0.75, data=d_1[d_1$Date!=election1&d_1$Date!=election0,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d_2[d_2$Date!=election2&d_2$Date!=election1,])+
  geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=d_2[d_2$Date!=election2&d_2$Date!=election1,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d_3[d_3$Date!=election3&d_3$Date!=election2,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d_4[d_4$Date!=election4&d_4$Date!=election3,])+
  geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=d_4[d_4$Date!=election4&d_4$Date!=election3,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=1,linewidth=0.75, data=d_5[d_5$Date!=election5&d_5$Date!=election4,])+
  geom_smooth(method = "lm",formula=y ~ x + I(x^2),fullrange=FALSE,se=FALSE, linewidth=0.75, data=d_5[d_5$Date!=election5&d_5$Date!=election4,])+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.95,linewidth=0.75, data=d_6[d_6$Date!=election6&d_6$Date!=election5,])+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold", size=25),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        axis.text.x.top = element_blank(),
        axis.ticks.x.top = element_blank(),
        axis.line.x.top = element_blank())+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  xlim(min(d$Date)-30, next_election)+
  geom_vline(xintercept=election0, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election1, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election2, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election3, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election4, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election5, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election6, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=next_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_vline(xintercept=future_election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_point(data=d[d$Date==next_election|d$Date==election0|d$Date==election1|d$Date==election2|d$Date==election3|d$Date==election4|d$Date==election5|d$Date==election6,],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==next_election|d$Date==election0|d$Date==election1|d$Date==election2|d$Date==election3|d$Date==election4|d$Date==election5|d$Date==election6,],size=5.25, shape=5, alpha=1)+
  scale_x_break(c(election6+25, as.Date("01 05 2019", "%d %m %Y")))+
  scale_x_date(date_breaks = "2 month", date_labels =  "%b %Y",limits = c(election6-25,future_election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling since the Mar 2017, Apr 2021, Jul 2021, Nov 2021, Oct 2022, Apr 2023, Jun 2024, Oct 2024 until the Next Bulgarian Parliamentary Election')
  # bbc_style()
plot1

ggsave(plot=plot1, file="Bulgaria/plot.png",width = 15, height = 7.5, type="cairo-png")

# 14 day average of latest polls for d0
d000<-poll00[poll00$Date>=max(poll00$Date)-14,]
d000 <- colMeans(d000[-1],na.rm = TRUE)
d000<- as.data.frame(d000)
d000 <- t(d000)
Date<-max(poll00$Date)
d000 <- cbind(Date, d000)
d000 <- as.data.frame(d000)
d000$Date <- as.Date(d000$Date)

d00 <- poll0[poll0$Date==max(poll0$Date),]
d00 <- as.data.frame(d00)
d0 <- poll1[poll1$Date==max(poll1$Date),]
d0 <- as.data.frame(d0)
d1 <- poll1[poll1$Date==min(poll1$Date),]
d1 <- as.data.frame(d1)
d2 <- poll2[poll2$Date==min(poll2$Date),]
d2 <- as.data.frame(d2)
d3 <- poll3[poll3$Date==min(poll3$Date),]
d3 <- as.data.frame(d3)
d4 <- poll4[poll4$Date==min(poll4$Date),]
d4 <- as.data.frame(d4)
d5 <- poll5[poll5$Date==min(poll5$Date),]
d5 <- as.data.frame(d5)
d6 <- poll6[poll6$Date==min(poll6$Date),]
d6 <- as.data.frame(d6)

d7 <-dplyr::bind_rows(d000,d00,d0,d1,d2,d3,d4,d5,d6)
d7 <- reshape2::melt(d7, id.vars="Date")
d7$value<-as.numeric(d7$value)/100
# d7$value[is.na(d7$value)] <- 0
d7$value<-formattable::percent(d7$value, digits = 2)


plot2<-ggplot(data=d7, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  scale_fill_manual(values = c("#a3c2df","#99bbdb","#6698ca","#4d87c1","#3376b8","#1a65af","#0054a6","#004385","#003c78",
                               "#aa8dff","#a180ff","#8e66ff","#7b4dff","#6833ff","#551aff","#4200ff","#3500cc","#3000b8",
                               "#f2d5a4","#f0d09a","#e4c386","#dbba7d","#d2b174","#c9a86b","#c09f62","#9a7f4e","#8b7246",
                               "#000000","#000000","#000000","#000000","#000000","#000000","#000000","#0066b7","#005ca5",
                               "#ff6078","#ff4e69","#ff3954","#f92f49","#f0243e","#e61a33","#db0f28","#af0c20","#9e0b1d",
                               "#000000","#000000","#000000","#000000","#000000","#000000","#000000","#6147aa","#574099",
                               "#afe9ff","#a6e6ff","#87ddff","#78d4f9","#69cbf0","#5ac2e7","#4bb9de","#3c94b2","#3685a0",
                               "#000000","#000000","#000000","#000000","#000000","#000000","#000000","#485669","#485669",
                               "#dddddd","#d9d9d9","#c1c1c1","#b7b7b7","#adadad","#a3a3a3","#999999","#7a7a7a","#6e6e6e",
                               "#ad1c20","#ad1c20","#ad1c20","#ad1c20","#ad1c20","#ad1c20","#ad1c20","#8a161a","#7c1417",
                               "#a3acef","#99a3ed","#668adc","#4d81d2","#3378c9","#1a6fc0","#0066b7","#005292","#004a83",
                               "#8bb37f","#7eaa71","#5d9556","#4c8c4d","#3b8344","#2a7a3b","#197032","#145a28","#125124",
                               "#f27ba4","#f16c9a","#e34c78","#d93d67","#cf2e56","#c51f45","#ba1034","#950d2a","#860c26",
                               "#fff6a3","#fff599","#ffe866","#ffdf4d","#ffd533","#ffcc1a","#ffc300","#cc9c00","#b88c00",
                               "#5fa9d6","#4d9fd1","#328aba","#267aad","#1a6a9e","#0e5a8f","#004a80","#003b66","#00355c",
                               "#f27ba4","#f16c9a","#e34c78","#d93d67","#cf2e56","#c51f45","#ba1034","#950d2a","#860c26",
                               "#6ce3c7","#5ce0c1","#3cd7b1","#2dc8a2","#1eb993","#0faa84","#009b75","#007c5e","#007055"))+
  geom_text(aes(label = formattable::percent(d7$value, digits = 1),y = 0),
            hjust=0, color="#000000",position = position_dodge(0.9), size=2.5, fontface="bold")+
  geom_text(aes(label = ifelse(is.na(d7$value), "Not Contested", ""),y = 0),
            hjust=0, color="#000000",position = position_dodge(0.9), size=2.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"),
        plot.title = ggtext::element_markdown(face="bold"),
        axis.text.y = element_text(face="bold",size=10))+
  ggtitle(' Polling <br> Oct 2024 Result <br> Jun 2024 Result <br> Apr 2023 Result <br> Oct 2022 Result <br> Nov 2021 Result <br> Jul 2021 Result <br> Apr 2021 Result <br> Mar 2017 Result  ')+
  scale_x_discrete(limits = rev(levels(d7$variable)))+
  coord_flip()
plot2

plotA<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))
plotA

ggsave(plot=plotA, file="Bulgaria/plot_long.png",width = 35, height = 15, type="cairo-png")

