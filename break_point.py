# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:44:34 2022

@author: Minty_Lin

break_point recorder
"""
from datetime import datetime
import json
import os

class break_point_recorder():
    version='beta'
    
    def generate(path_pwd, path_module, user, project_name):
        #generate a new breakpoint json file
        #nothing is returned
        with open(path_module) as json_file:
            dic = json.load(json_file)
            
        dic['step']=0
        dic['status']="finished"
        dic['date']=str(datetime.today())
        dic['user']=user;
        dic['download_name']='not defined'
        dic['project_name']=project_name
        
        os.makedirs(path_pwd+'/Cache',exist_ok=True)
        path_json=path_pwd+'/Cache/break_point.json'
        with open(path_json, "w") as outfile:
            json.dump(dic, outfile, indent=4)
    
    def read(path_pwd):
        #read the breakpoint json file, and return the key parameter, which is dic
        path_json=path_pwd+'/Cache/break_point.json'
        with open(path_json) as json_file:
            dic = json.load(json_file)
        return dic
    
    def write(path_pwd, dic):
        path_json=path_pwd+'/Cache/break_point.json'
        with open(path_json, "w") as outfile:
            json.dump(dic, outfile, indent=4)
    
    def delete(path_pwd):
        path_json=path_pwd+'/Cache/break_point.json'
        os.remove(path_json)
    
    def qsub_start(path_pwd, step):
        #anytime qsub a file, please use it to update the json
        dic=break_point_recorder.read(path_pwd)
        dic['step']=step 
        dic['status']='running'
        
        break_point_recorder.write(path_pwd, dic)
        
    def update_status(path_pwd):
        dic=break_point_recorder.read(path_pwd)
        qstat=os.popen('qstat -u '+dic['user']).readlines()
        tasks=len(qstat)-2
        #################
        if tasks<=0:
            dic['status']='finished'
            break_point_recorder.write(path_pwd, dic)
            if (dic['step']!=0):
                print('----------------------------------------')
                print("Current qsub tasks are finished. You could go to the next step.")
        else:
            print('----------------------------------------')
            print("qsub Tasks are running. Remaining Tasks:")
            print(tasks)
        
        
    
    
    
if __name__=="__main__":
    #test=break_point_recorder.generate('')
    break_point_recorder.generate('.','module_break_point.json', 'ES_cell', 'minty', 'casa')
    break_point_recorder.qsub_start('.','ES_cell', 3)
