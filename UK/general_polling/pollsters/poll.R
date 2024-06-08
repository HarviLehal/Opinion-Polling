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

py_run_file("UK/general_polling/pollsters/data2.py")
# open every csv in the folder
files <- list.files("UK/general_polling/pollsters", full.names = TRUE)
# remove non csv files
files <- files[grep(".csv", files)]
# read all csv files into separate dataframes
polls <- lapply(files, read_csv)
# rename eacc dataframe to the name of the file without the polls_ prefix
names(polls) <- gsub("UK/general_polling/pollsters/polls_", "", gsub(".csv", "", files))

# reshape each dataframe into long format
polls <- lapply(polls, function(x) {
  x$Date <- as.Date(x$Date, "%d %b %Y")
  x <- reshape2::melt(x, id.vars="Date")
})


start<-as.Date("01 05 2024", "%d %m %Y")
LE24<-as.Date("02 05 2024", "%d %m %Y")
start2<-as.Date("22 05 2024", "%d %m %Y")
old<-as.Date("12 12 2019", "%d %m %Y")
election<-as.Date("04 07 2024", "%d %m %Y")
f<-formattable::percent(0.6)

# plot each dataframe in the list with it's own line using the same color palette but a higher alpha using the above code
# create blank list to store the regression for each dataframe
plots <- list()
# loop through each dataframe in the list and create a LOESS regression line for each

# lapply(polls, function(x) {
#   print(paste("ITERATION", x))
#   # if (x == "Savanta"){
#   #   plot<-geom_line(method="loess",fullrange=FALSE,se=FALSE,span=0.75,linewidth=1, alpha=0.5, aes(x=Date, y=formattable::percent(value/100), colour=variable, group=variable), data=x)
#   # }
#   # else{
#     plot<-geom_line(method="loess",fullrange=FALSE,se=FALSE,span=0.75,linewidth=0.75, alpha=0.25, aes(x=Date, y=formattable::percent(value/100), colour=variable, group=variable), data=x)
#   # }
#     # make Savanta polls more visible
#     plots <<- c(plots, list(plot))
# })

# create function loop through each dataframe in the list and create a LOESS regression line for each without using lapply
for (i in 1:length(polls)) {
  x <- polls[[i]]
  if (names(polls)[i] == "INSERT POLLSTER NAME HERE"){
    plot<-geom_line(method="loess",fullrange=FALSE,se=FALSE,span=0.75,linewidth=1.25, linetype="dashed", alpha=1, aes(x=Date, y=formattable::percent(value/100), colour=variable, group=variable), data=x)
  }
  else{
    plot<-geom_line(method="loess",fullrange=FALSE,se=FALSE,span=0.75,linewidth=0.75, alpha=0.25, aes(x=Date, y=formattable::percent(value/100), colour=variable, group=variable), data=x)
  }
    # make Savanta polls more visible
    plots <- c(plots, list(plot))
}

# plot all regressions on the same plot

poll_total <- read_csv("UK/general_polling/poll.csv")
d <- reshape2::melt(poll_total, id.vars="Date")
d$Date<-as.Date(d$Date, "%d %b %Y")
d$value<-as.numeric(d$value)/100
# d$value[is.na(d$value)] <- 0
d$value<-formattable::percent(d$value)
start<-as.Date("01 05 2024", "%d %m %Y")
LE24<-as.Date("02 05 2024", "%d %m %Y")
start2<-as.Date("22 05 2024", "%d %m %Y")
old<-as.Date("12 12 2019", "%d %m %Y")
election<-as.Date("04 07 2024", "%d %m %Y")
f<-formattable::percent(0.6)

d<-d[d$Date>start|d$Date==old,]

plot1<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.6, data=d[d$Date!=old,],alpha=1) +
  scale_color_manual(values = c("#0077b6","#c70000","#e05e00","#f5dc00","#528D6B","#12B6CF"))+
  geom_smooth(method="loess",fullrange=FALSE,se=FALSE,span=0.5,linewidth=1.5, data=d[d$Date!=old,])+
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
  scale_y_continuous(name="Vote",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=old, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=election, linetype="solid", color = "#56595c", alpha=0.5, size=0.75)+
  geom_vline(xintercept=start2, linetype="dashed", color = "#000000", alpha=0.25, size=1)+
  geom_text(aes(start2,f,label = "Election Called", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  geom_vline(xintercept=LE24, linetype="dashed", color = "#000000", alpha=0.25, size=1)+
  geom_text(aes(LE24,f,label = "Local Elections", vjust = -1, hjust=0, angle=-90),colour="#000000")+
  geom_hline(aes(yintercept=0), alpha=0)+
  geom_point(data=d[d$Date==old,],size=5, shape=18, alpha=0.5)+
  geom_point(data=d[d$Date==old,],size=5.25, shape=5, alpha=0.5)+
  scale_x_break(c(old+0.5, start+1))+
  scale_x_date(date_breaks = "2 day", date_labels =  "%d %b %Y",limits = c(old-0.5,election),guide = guide_axis(angle = -90))+
  ggtitle('Opinion Polling for the 2024 United Kingdom General Election (Since Local Elections)')+
  plots
plot1
  



poll <- read_csv("UK/general_polling/poll.csv")
poll$Date <- as.Date(poll$Date, "%d %b %Y")
Date <- c(max(poll$Date))
poll[-1]<-data.frame(apply(poll[-1], 2, function(x) 
  as.numeric(sub("%","",as.character(x)))))
d2 <- poll[poll$Date==min(poll$Date),]
poll<-poll[poll$Date>(max(poll$Date)-3),]
d1 <- colMeans(poll[-1],na.rm = TRUE)
d1 <- as.data.frame(d1)
d1 <- t(d1)
d1 <- cbind(Date, d1)
d1 <- as.data.frame(d1)
d1$Date <- as.Date(d1$Date)
d2 <- as.data.frame(d2)

d1 <- reshape2::melt(d1, id.vars="Date")
d1$value<-as.numeric(d1$value)/100
d1$value<-formattable::percent(d1$value, digits = 1)

d2 <- reshape2::melt(d2, id.vars="Date")
d2$value<-as.numeric(d2$value)/100
d2$value<-formattable::percent(d2$value, digits = 1)

d3<-rbind(d2,d1)

plot2<-ggplot(data=d3, aes(x=variable, y=value,fill=interaction(Date,variable), group=Date )) +
  geom_bar(stat="identity",width=0.9, position=position_dodge())+
  # scale_fill_manual(values = c("#77c0ed","#0087DC","#f27999","#E4003B",
  # "#fcd38b","#FAA61A","#fcf7c5","#FDF38E",
  # "#9dc7af","#528D6B","#80dae8","#12B6CF"))+
  scale_fill_manual(values = c("#66add3","#0077b6","#dd6666","#c70000",
                               "#ec9e66","#e05e00","#f9ea66","#f5dc00",
                               # "#85c780","#33a22b","#71d8e2","#13bece"))+
                               "#9dc7af","#528D6B","#80dae8","#12B6CF"))+
  
  geom_text(aes(label = formattable::percent(ifelse(d3$Date != min(d3$Date), d3$value, ""), digits = 1),y = 0),
            hjust=-0.35, vjust = 0, color="#000000",position = position_dodge(0.7), size=3.5, fontface="bold")+
  geom_text(aes(label = ifelse(d3$Date == min(d3$Date),paste("(",d3$value,")"),""),y = 0),
            hjust=-0.1, vjust = 0, color="#404040", position = position_dodge(1.1), size=3.5, fontface="bold")+
  theme_minimal()+
  theme(legend.position = "none",axis.title=element_blank(),axis.text.x = element_blank(),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF"))+
  ggtitle(' 3 day average \n (2019 Result)')+
  scale_x_discrete(limits = rev(levels(d3$variable)))+
  coord_flip()
plot2

plot<-aplot::plot_list(plot1,plot2,ncol = 2, nrow = 1,widths=c(2,0.5))

ggsave(plot=plot, file="UK/general_polling/pollsters/plot_election.png",width = 20, height = 7.5, type = "cairo-png")
