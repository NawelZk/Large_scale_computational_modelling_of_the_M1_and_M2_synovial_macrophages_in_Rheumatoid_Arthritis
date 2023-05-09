library(readxl)
library(xlsx)
setwd("a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main/In_silico_simulations")
modif <- read.csv("stable_nodes.csv")
calibrated <- read.csv("M1_calibrated_state_with_no_oscillations.csv", sep=";")
vec=calibrated$stable_nodes_name
modif=modif[modif$stable_nodes_name %in% vec,]
modif <- modif[order(modif$stable_nodes_name),]
calibrated=calibrated[order(calibrated$stable_nodes_name),]
modif=cbind(modif,calibrated$occurence)
modif=modif[modif$stable_nodes_val!=modif$`calibrated$occurence`,]

