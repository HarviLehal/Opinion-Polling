library(reticulate)
library(ggplot2)
library(bbplot)
library(tidyquant)
library(scales)
library(Cairo)
library(reshape2)
library(readr)
library(formattable)

py_run_file("French_Elections/Approval_Ratings/data.py")
macron <- read_csv("French_Elections/Approval_Ratings/macron.csv")
borne <- read_csv("French_Elections/Approval_Ratings/borne.csv")
castex <- read_csv("French_Elections/Approval_Ratings/castex.csv")
philippe <- read_csv("French_Elections/Approval_Ratings/philippe.csv")

d1 <- melt(macron, id.vars="Date")
d2 <- melt(borne, id.vars="Date")
d3 <- melt(castex, id.vars="Date")
d4 <- melt(philippe, id.vars="Date")

d <- rbind(d1,d2,d3,d4)
d.list<-lapply(1:4,function(x) eval(parse(text=paste0("d",x))))
names(d.list)<-lapply(1:4, function(x) paste0("d", x))


for (i in 1:length(d.list)){ 
  d.list[[i]]$value<-formattable::percent(d.list[[i]]$value)
}
list2env(d.list,.GlobalEnv)

# SANS BORNE

d1 <- melt(macron, id.vars="Date")
d2 <- melt(castex, id.vars="Date")
d3 <- melt(philippe, id.vars="Date")

d <- rbind(d1,d2,d3)
d.list<-lapply(1:3,function(x) eval(parse(text=paste0("d",x))))
names(d.list)<-lapply(1:3, function(x) paste0("d", x))


for (i in 1:length(d.list)){ 
  d.list[[i]]$value<-formattable::percent(d.list[[i]]$value)
}
list2env(d.list,.GlobalEnv)





castex<-as.Date("03 07 2020", "%d %m %Y")
borne<-as.Date("16 05 2022", "%d %m %Y")
foot<-as.Date("15 06 2018", "%d %m %Y")
ukr<-as.Date("24 02 2022", "%d %m %Y")
# ORDER OF VALUES:
    # Macron Approve      Macron Disapprove     Macron Unsure
    # Borne Approve       Borne Disapprove      Borne Unsure      # IGNORE THIS IF USING SANS BORNE SECTION (RECOMMENDED!!!!!!)
    # Castex Approve      Castex Disapprove     Castex Unsure
    # Philippe Approve    Philippe Disapprove   Philippe Unsure

# MAIN GRAPH


# LOESS GRAPH

plot<-ggplot(data=d,aes(x=Date,y=value, colour=variable, group=variable)) +
  geom_point(size=0.5,alpha=0.5) +
  geom_smooth(method="loess",fullrange=TRUE,se=FALSE,span=0.25,linewidth=0.75,aes(linetype=variable))+
  bbplot::bbc_style()+
  scale_y_continuous(name="Percentage",labels = scales::percent_format(accuracy = 5L),breaks=seq(0,0.6,0.05))+
  geom_vline(xintercept=castex, linetype="dashed", color = "#385ffa", alpha=0.5, size=1.5)+
  geom_vline(xintercept=borne, linetype="dashed", color = "#ed6161", alpha=0.5, size=1.5)+
  geom_vline(xintercept=foot, linetype="dashed", color = "#FFBF00", alpha=0.5, size=1.5)+
  geom_vline(xintercept=ukr, linetype="dashed", color = "#0e80eb", alpha=0.5, size=1.5)+

  scale_color_manual(values = c("#006000","#600000","#424242",
                                "#009000","#990000","#6e6e6e",
                                "#009000","#990000","#6e6e6e"))+
  scale_linetype_manual(values=c("solid", "longdash", "twodash",
                                 "solid", "longdash", "twodash",
                                 "solid", "longdash", "twodash"))


ggsave(plot=plot, file="French_Elections/Approval_Ratings/plot.png",width = 15, height = 7.5, type = "cairo-png")

# EXPERIMENTAL THINGS
