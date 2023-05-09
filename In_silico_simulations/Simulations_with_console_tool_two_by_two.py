# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:52:29 2023

@author: I0471594
"""


import pandas as pd
import json
import os
import subprocess
import itertools
from itertools import combinations
import numpy as np

my_path = os.path.join("a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main","In_silico_simulations","BMA")
os.chdir(my_path)
file=open("M2_macrophage_calibrated.json")
global model
model = json.load(file)
file.close()

df = pd.read_csv('a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main\\In_silico_simulations\\Two_by_two_drug_combinations.csv',sep=';', header=0)
ko=df['Corresponding_nodes_M2_macrophage']
ko=ko.dropna()
ko_sep=ko.str.split(',', expand=True)
all_ko=ko_sep.values.tolist()
all_ko=list(itertools.chain.from_iterable(all_ko))
all_ko=list(filter(None,all_ko))
ko_id=[]
ko_name=[]

for i in model['Model']["Variables"]:
    if i['Name'] in all_ko:
        ko_id.append(i['Id'])
        ko_name.append(i["Name"])
ko_id_name= {'name':ko_name,'id':ko_id}
ko_id_name=pd.DataFrame(ko_id_name)


for col in ko_sep.columns:
    for i in ko_sep.index:
        if str(ko_sep[col][i]) in set(ko_id_name["name"]):
            index=list(np.where(ko_id_name["name"]==ko_sep[col][i]))
            index=index[0]
            ko_sep[col] = ko_sep[col].replace([ko_sep[col][i]],ko_id_name['id'][index].astype(int))
            
            
M1_targets=df[['Targets','Corresponding_nodes_M2_macrophage']]
M1_targets = M1_targets[M1_targets['Corresponding_nodes_M2_macrophage'].notna()]

ko_sep_with_targets=pd.concat([M1_targets,ko_sep],axis=1)
combi=[",".join(map(str, comb)) for comb in combinations(ko_sep_with_targets['Targets'],2)]

def drug_combination(pair,co):
    args='BioCheckConsole.exe -engine VMCAI -model M2_macrophage_calibrated.json -prove stability_analysis.json'
    pair=pair.split(',')
    data=ko_sep_with_targets[ko_sep_with_targets['Targets'].isin(pair)]
    data=data.drop(data.columns[[0,1]],axis=1)
    ko_list=[]
    for col in data.columns:
       ko_list.append(data[col].values.tolist())
    ko_list=list(itertools.chain.from_iterable(ko_list))
    ko_list=[x for x in ko_list if str(x) != 'nan']
    ko_list=[x for x in ko_list if str(x) != ' ']
    ko_list=list(filter(None,ko_list))
    ko_list=[int(item) for item in ko_list]
    
    for ko in ko_list:
      args=args +' '+ '-ko '+ str(ko) +' '+ str(0)

    subprocess.run(args,shell=True)



    stable_nodes_id=[]
    stable_nodes_val=[]
    stable_nodes_name=[]
      
    
    file=open('stability_analysis.json')
    result=json.load(file)
    file.close()
      
    for i in result['Ticks'][0]['Variables']:
        if i["Lo"]==i["Hi"]:
            stable_nodes_id.append(i['Id'])
            stable_nodes_val.append(i['Lo'])
    
    
    for i in stable_nodes_id:
        for k in model['Model']["Variables"]:
            if i == k['Id']:
                stable_nodes_name.append(k['Name'])
                
    
   
        
    df_stable={'stable_nodes_id':stable_nodes_id,'stable_nodes_val':stable_nodes_val,'stable_nodes_name':stable_nodes_name}
    df_stable=pd.DataFrame(df_stable)
    df_stable.to_csv('a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main\\In_silico_simulations\\'+'_'+str(co)+'.csv')
    

co=0
for pair in combi:
    drug_combination(pair,co)
    co=co+1
combi={'drug_pairs':combi}
combi=pd.DataFrame(combi)
combi.to_csv('a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main\\In_silico_simulations\\two_by_two_combination_KO_M2.csv')
  
   