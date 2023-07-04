library(readxl)
library(xlsx)
library(sys)
library(plyr)
library(stringi)
setwd("a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main//In_silico_simulations")calibrated <- read.csv("M1_calibrated_state_with_no_oscillations.csv", sep=";")
calibrated <- read.csv("M1_calibrated_state_with_no_oscillations.csv", sep=";")
vec=calibrated$stable_nodes_name
vec=calibrated$stable_nodes_name
drug_combi<- read.csv("two_by_two_combination_KO_M1.csv")

files <- list.files(pattern = "Simulation*")
interesting=c()
for (i in files){
  modif=read.csv(i)
  modif=modif[modif$stable_nodes_name %in% vec,]
  modif <- modif[order(modif$stable_nodes_name),]
  calibrated=calibrated[order(calibrated$stable_nodes_name),]
  modif=cbind(modif,calibrated$occurence)
  modif=modif[modif$stable_nodes_val!=modif$`calibrated$occurence`,]
  if ("proliferation_survival_M1_macrophage_phenotype" %in% modif$stable_nodes_name &
      ("apoptosis_M1_macrophage_phenotype" %in% modif$stable_nodes_name)){ 
  res=stri_replace_all_regex(i,pattern=c('Simulation_', '.csv'),replacement=c('', ''),vectorize=FALSE)
  interesting=append(strtoi(res),interesting)}
}

drug_combi_interesting=subset(drug_combi, X %in% interesting)
write.csv(drug_combi_interesting,"drug_combination_M1_proliferation_and_apoptosis.csv")


