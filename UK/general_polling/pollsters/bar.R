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

# create blank dataframe with net approval rating for each party leader

data<-data.frame(
  Leader=c("Penny Moradaunt","Angela Rayner","Stephen Flynn","Daisy Cooper","Rhun ap Iorwerth","Carla Denyer","Nigel Farage"),
  Approval = c(0.29,0.48,0.50,0.47,0.38,0.50,0.45),
  Disapproval = c(0.48,0.25,0.19,0.17,0.21,0.19,0.35))

data$Net<-data$Approval-data$Disapproval

# order the dataframe by net approval rating

data<-data[order(data$Net),]

# create a bar plot of the net approval rating for each party leader in order of net approval rating

plot <- ggplot(data, aes(x=reorder(Leader, Net), y=Net, fill=Leader)) +
  geom_bar(stat="identity") +
  scale_fill_manual(values = c("#c70000","#528D6B","#e05e00","#12B6CF","#0077b6","#1e5b53","#f5dc00"))+
  theme_minimal()+
  theme(legend.position = "none",
        axis.title = element_text(face="bold"),
        axis.text.x = element_text(face="bold"),
        axis.text.y = element_text(face="bold"),
        plot.title = element_text(face="bold"),
        # panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill="#FFFFFF",color="#FFFFFF"),
        plot.background = element_rect(fill = "#FFFFFF",color="#FFFFFF")
        )+
  labs(title="Net Approval Rating of Party Representatives Debate Performance",
       y="Net Approval Rating",
       x="Party Leader") +
  geom_text(aes(label=formattable::percent(Net,digits=0)), hjust=-0.4, size=3.5, fontface="bold") +
  scale_y_continuous(labels = scales::percent_format(scale = 100))+
  coord_flip()

plot

ggsave(plot=plot, file="UK/general_polling/pollsters/debate.png",width = 10, height = 5, type = "cairo-png")

