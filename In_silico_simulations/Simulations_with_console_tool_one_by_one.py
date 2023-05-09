# -*- coding: utf-8 -*-
"""
Created on Tue May  2 12:07:20 2023

@author: I0471594
"""

import pandas as pd
import json
import os
import subprocess

my_path = os.path.join("a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main","In_silico_simulations","BMA")
os.chdir(my_path)

file=open("M2_macrophage_calibrated.json")
global model
model = json.load(file)
file.close()
all_ko=["JAK1","JAK1_TYK2_complex","JAK2"]
ko_id=[]
ko_name=[]

for i in model['Model']["Variables"]:
    if i['Name'] in all_ko:
        ko_id.append(i['Id'])
        ko_name.append(i["Name"])
ko_id_name= {'name':ko_name,'id':ko_id}
ko_id_name=pd.DataFrame(ko_id_name)
args='BioCheckConsole.exe -engine VMCAI -model M2_macrophage_calibrated.json -prove stability_analysis.json'
for ko in ko_id_name["id"]:
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
df_stable.to_csv('a-computational-framework-to-build-and-calibrate-large-scale-boolean-models-main\\In_silico_simulations\\stable_nodes.csv')
