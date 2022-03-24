# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:28:49 2022

@author: Minty_Lin

start_part of DCC pipeline
"""
from SRAdownload import SraRunTable_helper
from SRA2fastq import SRA2fastq_helper
from fastq2gz import fastq2gz_helper
from star import star_helper
from merge_helper import Merge_helper
from DCC import DCC_helper
from break_point import break_point_recorder
import os
import sys


class DCC_pipeline():
    version='beta'
    def __init__(self):
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        self.breakpoint=self.pwd+'/Cache/break_point.json'
    
    def start(self):
        print("Hi, I am the DCC_pipeline helper")
        print("Version: "+DCC_pipeline.version)
        print("Hope you have already read the manual.")
        if (os.path.exists(self.breakpoint)):
            print('----------------------')
            print('Recovering the previous running DCC-pipeline.')
            break_point_recorder.update_status(self.pwd)
            dic=break_point_recorder.read(self.pwd)
            print(dic)
        else:
            print('----------------------')
            print('Starting a new DCC-pipeline.')
            username=input("Please give me your SCC username(for submitting qsub tasks): ")
            break_point_recorder.generate(self.pwd, self.pro_path+"/bash_files/module_break_point.json",username)
        
        self.do_steps()
        
    def do_steps(self):
        
        while(1):
            break_point_recorder.update_status(self.pwd)
            dic=break_point_recorder.read(self.pwd)
            
            if (dic['step']==5):
                print('------------------------------------')
                print("What can I do for you:")
                print("1. Have other parameters for DCC")
                print("2. Delete records")
                print("3. Enviorment Setting (Not full developed)")
                print("4. Quit the program")
                print('------------------------------------')
                func_num=int(input("Input the number before the function you need: "))
                if (func_num==4):
                    break;
                if (func_num==2):
                    break_point_recorder.delete(self.pwd)
                if (func_num==1):
                    self. do_step(5)
            
            else:
                if (dic['status']=='running'):
                    print('------------------------------------')
                    print('''Please wait for the SCC right now. All qsub tasks should be done before starting next step. 
You could quit the program and come back later. 
Also, when you are not in the program you could use 'qstat -u username to check the qsub tasks' ''')
                    temp=input("Press q to quit the program. Press any other key to continue.")
                    if (temp=='q'):
                        break
                else:
                    print('------------------------------------')
                    print("You have finished: ", self.step_name(dic['step']) )
                    print('------------------------------------')
                    print("What can I do for you:")
                    print("1. Go to the next step")
                    print("2. Delete records")
                    print("3. Enviorment Setting (Not full developed)")
                    print("4. Quit the program")
                    print('------------------------------------')
                    func_num=int(input("Input the number before the function you need: "))
                    if (func_num==4):
                        break;
                    if (func_num==2):
                        break_point_recorder.delete(self.pwd)
                    if (func_num==1):
                        self. do_step(dic['step'])
                    
    
    def do_step(self,last_step):
        break_point_recorder.update_status(self.pwd)
        dic=break_point_recorder.read(self.pwd)
        
        if (last_step==0):
            (download_name, success)=SraRunTable_helper.func(user=dic['user'])
            if (success==1):
                dic['status']='running'
                dic['download_name']=download_name
                dic['step']=1;
                break_point_recorder.write(self.pwd,dic)
            else:
                print("You did not download anything.")
            
        if (last_step==1):
            (download_name, success)=SRA2fastq_helper.func(dic['download_name'], user=dic['user'])
            if (success==1):
                break_point_recorder.qsub_start(self.pwd,2)
            else:
                print("You did not convert it")
                
        if (last_step==2):
            (download_name, success)=star_helper.func(dic['download_name'], user=dic['user'])
            if (success==1):
                break_point_recorder.qsub_start(self.pwd,3)
            else:
                print("You did not start the STAR alignment")
                
        if (last_step==3):
            Merge_helper.func(dic['download_name'])
            break_point_recorder.qsub_start(self.pwd,4)
                
        if (last_step==4 or last_step==5):
            p1=input("DCC parameter 1: ")
            p2=input("DCC parameter 2: ")
            (download_name, success)=DCC_helper.func(dic['download_name'], p1 , p2 ,user=dic['user'])
            if (success==1):
                break_point_recorder.qsub_start(self.pwd,5)
                print("-----------------------------")
                print("DCC is submitted. You could find DCC result in ./Run/DCC/<cell_name>_<p1>_<p2>")
            else:
                print("You did not start the DCC")
                
            
        
    def step_name(self,step):
        if (step==0):
            return "Step 0: begin"
        if (step==1):
            return "Step 1: Download SRA files"
        if (step==2):
            return "Step 2: Convert SRA files to fastqgz files"
        if (step==3):
            return "Step 3: STAR alignment"
        if (step==4):
            return "Step 4: merge STAR bam files"
        if (step==5):
            return "Step 5: DCC"
        if (step==6):
            return "All finished. You could find DCC result in ./Run/DCC/<cell_name>_<p1>_<p2>"
        
            


if __name__=="__main__":
    DCC=DCC_pipeline()
    DCC.start()
