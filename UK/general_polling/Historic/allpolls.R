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

poll45 <- read_csv("UK/general_polling/Historic/poll45.csv")
poll50 <- read_csv("UK/general_polling/Historic/poll50.csv")
poll51 <- read_csv("UK/general_polling/Historic/poll51.csv")
poll55 <- read_csv("UK/general_polling/Historic/poll55.csv")
poll59 <- read_csv("UK/general_polling/Historic/poll59.csv")
poll64 <- read_csv("UK/general_polling/Historic/poll64.csv")
poll66 <- read_csv("UK/general_polling/Historic/poll66.csv")
poll70 <- read_csv("UK/general_polling/Historic/poll70.csv")
poll74 <- read_csv("UK/general_polling/Historic/poll74.csv")
poll74_2 <- read_csv("UK/general_polling/Historic/poll74_2.csv")
poll79 <- read_csv("UK/general_polling/Historic/poll79.csv")
poll83 <- read_csv("UK/general_polling/Historic/poll83.csv")
poll87 <- read_csv("UK/general_polling/Historic/poll87.csv")
poll92 <- read_csv("UK/general_polling/Historic/poll92.csv")
poll97 <- read_csv("UK/general_polling/Historic/poll97.csv")
poll01 <- read_csv("UK/general_polling/Historic/poll01.csv")
poll05 <- read_csv("UK/general_polling/Historic/poll05.csv")
poll10 <- read_csv("UK/general_polling/Historic/poll10.csv")
poll15 <- read_csv("UK/general_polling/Historic/poll15.csv")
poll17 <- read_csv("UK/general_polling/Historic/poll17.csv")
poll19 <- read_csv("UK/general_polling/Historic/poll19.csv")
poll24 <- read.csv("UK/general_polling/poll.csv")
# convert poll24 to a tibble
poll24 <- as_tibble(poll24)
poll24$Date <- as.Date(poll24$Date, "%Y-%m-%d")
# correct poll24 column name for Lib Dem which is currently "Lib.Dem"
names(poll24)[names(poll24) == "Lib.Dem"] <- "Lib Dem"

poll<-dplyr::bind_rows(poll45,poll50,poll51,poll55,poll59,poll64,poll66,poll70,poll74,poll74_2,poll79,poll83,poll87,poll92,poll97,poll01,poll05,poll10,poll15,poll17,poll19,poll24)

# create list of all polls
polls<-c("poll45","poll50","poll51","poll55","poll59","poll64","poll66","poll70","poll74","poll74_2","poll79","poll83","poll87","poll92","poll97","poll01","poll05","poll10","poll15","poll17","poll19","poll24")

d <- reshape2::melt(poll, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
d$value<-formattable::percent(d$value)
election<-as.Date("04 07 2024", "%d %m %Y")
mindate<-min(d$Date)
old<-c(as.Date("12 12 2019", "%d %m %Y"),
       as.Date("08 06 2017", "%d %m %Y"),
       as.Date("07 05 2015", "%d %m %Y"),
       as.Date("06 05 2010", "%d %m %Y"),
       as.Date("05 05 2005", "%d %m %Y"),
       as.Date("07 06 2001", "%d %m %Y"),
       as.Date("01 05 1997", "%d %m %Y"),
       as.Date("09 04 1992", "%d %m %Y"),
       as.Date("11 06 1987", "%d %m %Y"),
       as.Date("09 06 1983", "%d %m %Y"),
       as.Date("03 05 1979", "%d %m %Y"),
       as.Date("10 10 1974", "%d %m %Y"),
       as.Date("28 02 1974", "%d %m %Y"),
       as.Date("18 06 1970", "%d %m %Y"),
       as.Date("31 03 1966", "%d %m %Y"),
       as.Date("15 10 1964", "%d %m %Y"),
       as.Date("08 10 1959", "%d %m %Y"),
       as.Date("26 05 1955", "%d %m %Y"),
       as.Date("25 10 1951", "%d %m %Y"),
       as.Date("23 02 1950", "%d %m %Y"),
       as.Date("05 07 1945", "%d %m %Y"))

h<-melt(poll50[1,],id.vars="Date")
h$value<-as.numeric(h$value)/100
h$value<-formattable::percent(h$value)

h2<-melt(poll74_2[1,],id.vars="Date")
h2$value<-as.numeric(h2$value)/100
h2$value<-formattable::percent(h2$value)

h3<-melt(poll15[1,],id.vars="Date")
h3$value<-as.numeric(h3$value)/100
h3$value<-formattable::percent(h3$value)

h4<-melt(poll19[1,],id.vars="Date")
h4$value<-as.numeric(h4$value)/100
h4$value<-formattable::percent(h4$value)

h5<-melt(poll45[1,],id.vars="Date")
h5$value<-as.numeric(h5$value)/100
h5$value<-formattable::percent(h5$value)
# GRAPH

#Reshape every poll individually using a for loop
for (i in 1:22){
  assign(paste0("d_",i),reshape2::melt(get(paste0(polls[i])), id.vars="Date"))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=as.numeric(value)/100))
  assign(paste0("d_",i),get(paste0("d_",i)) %>% mutate(value=formattable::percent(value)))
}

#set span for each poll based on range of dates

spans <- c()
  
for (i in 1:22){
  spans[i]<-min(1,1000/as.numeric(max(get(paste0("d_",i))$Date)-min(get(paste0("d_",i))$Date)))
  if (spans[i]<1){
    spans[i]<-spans[i]/2
  }
}
spans[21]<-0.3
spans[22]<-0.05
d<- d %>%
  group_by(variable) %>%
  arrange(Date) %>%
  mutate(Moving_Average = rollapplyr(value, seq_along(Date) - findInterval(Date - 7, Date), mean,na.rm=TRUE))

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#0077b6","#c70000","#e05e00","#6D3177",
                                "#528D6B","#f5dc00","#12B6CF","#222221"))+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.075,linewidth=0.75, data=d[d$Date!=old|d$Date!=election,])+
  # geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.6,linewidth=0.75, data=d_1[d_1$Date!=old,],alpha=0.75)+
  # geom_smooth(method = "lm",formula=y ~ poly(x, 5, raw = TRUE),fullrange=TRUE,se=FALSE, linewidth=0.75, data=d_1[d_1$Date!=old,],alpha=0.75)+
  geom_smooth(method = "lm",formula=y ~ x,fullrange=FALSE,se=FALSE, linewidth=0.75, data=d_1[d_1$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[2],linewidth=0.75, data=d_2[d_2$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[3],linewidth=0.75, data=d_3[d_3$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[4],linewidth=0.75, data=d_4[d_4$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[5],linewidth=0.75, data=d_5[d_5$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[6],linewidth=0.75, data=d_6[d_6$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[7],linewidth=0.75, data=d_7[d_7$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[8],linewidth=0.75, data=d_8[d_8$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[9],linewidth=0.75, data=d_9[d_9$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[10],linewidth=0.75, data=d_10[d_10$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[11],linewidth=0.75, data=d_11[d_11$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[12],linewidth=0.75, data=d_12[d_12$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[13],linewidth=0.75, data=d_13[d_13$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[14],linewidth=0.75, data=d_14[d_14$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[15],linewidth=0.75, data=d_15[d_15$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[16],linewidth=0.75, data=d_16[d_16$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[17],linewidth=0.75, data=d_17[d_17$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[18],linewidth=0.75, data=d_18[d_18$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[19],linewidth=0.75, data=d_19[d_19$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[20],linewidth=0.75, data=d_20[d_20$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[21],linewidth=0.75, data=d_21[d_21$Date!=old,],alpha=0.75)+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=spans[22],linewidth=0.75, data=d_22[d_22$Date!=old,],alpha=0.75)+
# plot1
  # geom_line(aes(y = Moving_Average), size=0.75, alpha=1)+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_point(data=d[d$Date==old[1],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[1],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h4,size=5, shape=18, alpha=1)+
  geom_point(data=h4,size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[2],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[2],],size=5.25, shape=5, alpha=1)+
  # geom_point(data=d[d$Date==old[3],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[3],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h3,size=5, shape=18, alpha=1)+
  geom_point(data=h3,size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[4],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[4],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[5],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[5],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[6],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[6],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[7],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[7],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[8],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[8],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[9],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[9],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[10],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[10],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[11],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[11],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[12],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[12],],size=5.25, shape=5, alpha=1)+
  # geom_point(data=d[d$Date==old[13],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[13],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h2,size=5, shape=18, alpha=1)+
  geom_point(data=h2,size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[14],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[14],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[15],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[15],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[16],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[16],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[17],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[17],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[18],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[18],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[19],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[19],],size=5.25, shape=5, alpha=1)+
  # geom_point(data=d[d$Date==old[20],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[20],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h,size=5, shape=18, alpha=1)+
  geom_point(data=h,size=5.25, shape=5, alpha=1)+
  # geom_point(data=d[d$Date==old[21],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[21],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h5,size=5, shape=18, alpha=1)+
  geom_point(data=h5,size=5.25, shape=5, alpha=1)+
  # geom_line(aes(y = Moving_Average), size=0.75, alpha=0.5)+
  scale_x_date(date_breaks = "2 year", date_labels =  "%Y",limits = c(mindate,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for Every United Kingdom General Election since 1943')


plot1


ggsave(plot=plot1, file="UK/general_polling/Historic/PLOT.png",width = 50, height = 10, type = "cairo-png",limitsize=FALSE)
state<-tail(d,8)
plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_hline(yintercept=state$Moving_Average, linetype="solid",
             color = c("#0077b6","#c70000","#e05e00","#6D3177",
                       "#528D6B","#f5dc00","#12B6CF","#222221"), alpha=1,linetype="dashed", size=1)+
  geom_point(size=0.5, data=d[d$Date!=old&d$Date!=election,],alpha=0.5) +
  scale_color_manual(values = c("#0077b6","#c70000","#e05e00","#6D3177",
                                "#528D6B","#f5dc00","#12B6CF","#222221"))+
  theme_minimal()+
  theme(axis.title=element_blank(),legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  # geom_point(data=d[d$Date==old[1],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[1],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h4,size=5, shape=18, alpha=1)+
  geom_point(data=h4,size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[2],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[2],],size=5.25, shape=5, alpha=1)+
  # geom_point(data=d[d$Date==old[3],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[3],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h3,size=5, shape=18, alpha=1)+
  geom_point(data=h3,size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[4],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[4],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[5],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[5],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[6],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[6],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[7],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[7],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[8],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[8],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[9],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[9],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[10],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[10],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[11],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[11],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[12],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[12],],size=5.25, shape=5, alpha=1)+
  # geom_point(data=d[d$Date==old[13],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[13],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h2,size=5, shape=18, alpha=1)+
  geom_point(data=h2,size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[14],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[14],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[15],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[15],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[16],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[16],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[17],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[17],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[18],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[18],],size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[19],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[19],],size=5.25, shape=5, alpha=1)+
  # geom_point(data=d[d$Date==old[20],],size=5, shape=18, alpha=1)+
  # geom_point(data=d[d$Date==old[20],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h,size=5, shape=18, alpha=1)+
  geom_point(data=h,size=5.25, shape=5, alpha=1)+
  geom_point(data=d[d$Date==old[21],],size=5, shape=18, alpha=1)+
  geom_point(data=d[d$Date==old[21],],size=5.25, shape=5, alpha=1)+
  geom_point(data=h5,size=5, shape=18, alpha=1)+
  geom_point(data=h5,size=5.25, shape=5, alpha=1)+
  geom_line(aes(y = Moving_Average), size=0.75, alpha=0.5)+
  scale_x_date(date_breaks = "2 year", date_labels =  "%Y",limits = c(mindate,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for Every United Kingdom General Election since 1943')


plot1

ggsave(plot=plot1, file="UK/general_polling/Historic/PLOT_MA.png",width = 50, height = 10, type = "cairo-png",limitsize=FALSE)




histplot<-ggplot(poll, aes(x=Date))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_histogram(color="#887cac", fill="#ffac94",binwidth=60)+
  theme_minimal()+
  theme(legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position = "none",
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  scale_x_date(date_breaks = "2 year", date_labels =  "%Y",limits = c(mindate,election),guide = guide_axis(angle = -90))+
  ggtitle('Number of Polls Conducted Every 60 Days Since June 1943')

histplot
ggsave(plot=histplot, file="UK/general_polling/Historic/Hist_Plot.png",width = 50, height = 10, type = "cairo-png",limitsize=FALSE)
