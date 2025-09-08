library(ggplot2)
library(readr)
library(dplyr)

read_tsv("~/SEIR_4.traj") %>%
ggplot (aes (t,value,color=population,group_by=factor(Sample))) + geom_step(alpha=0.5)

