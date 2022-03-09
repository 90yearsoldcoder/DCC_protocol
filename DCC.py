# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 23:26:43 2022

@author: Minty_Lin

perform DCC
"""
import os
import sys
from enviroment import qsub_para

class DCC_helper(object):
    version="beta"
    def __init__(self, download_name, user):
        self.user=user;              #SCC username
        #self.download_list= None
        self.download_name= download_name   #download_name is the keyword witout space
        self.code=0; #downloading has been done or not
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        self.samplesheet_path=self.pwd+"/Run/DCC/"+self.download_name+'/DCC_InputFiles/samplesheet' 
        self.mate1_path=self.pwd+"/Run/DCC/"+self.download_name+'/DCC_InputFiles/mate1' 
        self.mate2_path=self.pwd+"/Run/DCC/"+self.download_name+'/DCC_InputFiles/mate2' 
        self.dcc_out_dir=self.pwd+"/Run/DCC/"
        
        #module json path
        module_json_single = self.pro_path+"/bash_files/module_DCC_single.json"
        module_json_paired = self.pro_path+"/bash_files/module_DCC_paired.json"
        #Working place json file path
        pwd_json_single= self.pwd+"/Cache/DCC_single.json"
        pwd_json_paired= self.pwd+"/Cache/DCC_paired.json"
        
        
        os.makedirs(self.pwd+'/Cache',exist_ok=True)
        os.makedirs(self.pwd+'/Cache/tmpdir',exist_ok=True)
        #create the star working place
        os.makedirs(self.dcc_out_dir+'/'+self.download_name,exist_ok=True)
        
        #Do working place has the json file? if not, read the module json and write a new one
        if not(os.path.exists(pwd_json_single)):
            self.env_single=qsub_para.read_json("DCC_single", module_json_single)
            #rewrite the output directory of dcc
            self.env_single.set_dic_p2p('output_dir', self.dcc_out_dir+"/${cell_type}_${p1}_${p2}_ver2")
            #rewrite the cache file path for dcc
            self.env_single.set_dic_p2p('tmp_dir', self.dcc_out_dir+"/tmp_dir/${1}_${2}_${3}_ver2")
            self.env_single.write2json(pwd_json_single)
        else:
            self.env_single=qsub_para.read_json("DCC_single", pwd_json_single)
            
        if not(os.path.exists(pwd_json_paired)):
            self.env_paired=qsub_para.read_json("DCC_paired", module_json_paired)
            #rewrite the output directory of star
            self.env_paired.set_dic_p2p('output_dir', self.dcc_out_dir+"/${cell_type}_${p1}_${p2}_ver2")
            #rewrite the cache file path for star
            self.env_paired.set_dic_p2p('tmp_dir', self.dcc_out_dir+"/tmp_dir/${1}_${2}_${3}_ver2")
            self.env_paired.write2json(pwd_json_paired)
        else:
            self.env_paired=qsub_para.read_json("DCC_paired", pwd_json_paired)
    
    def start():
        print('----------------------------------------------------')
        print("Hi, I am DCC_helper")
        print("Version: "+DCC_helper.version)
        print("I assume samplesheet is in ./Run/DCC/${key_word}/DCC_InputFiles/samplesheet")
        print("I assume mate1 is in ./Run/DCC/${key_word}/DCC_InputFiles/mate1")
        print("I assume mate2 is in ./Run/DCC/${key_word}/DCC_InputFiles/mate2")
        download_name=input("Please input the keyword(eg. ES_cell):")
        p1=input("parameter 1: ")
        p2=input("parameter 2: ")
        
        DCC_helper.func(download_name, p1 ,p2)
    
    def func(download_name, p1, p2, user='minty'):
        dc=DCC_helper(download_name, user)
        dc.readlist()
        #####paired or single?
        paired=False
        if os.path.exists(dc.pwd+"/Sample/"+dc.download_name+"/fastqgz/"+dc.download_list[0]+"_2.fastq.gz"):
            print("I think they are paired-end sequences.")
            paired=True;
        else:
            print("I think they are single-end sequences.")
            paired=False;
        
        dc.run(p1, p2, paired)
        
        return (download_name, dc.code)
    
    def readlist(self):
        selected_list=[]
        path_list=self.pwd+"/Cache/"+self.download_name+".txt"
        with open(path_list,'rt') as f:
            for line in f.readlines():
                selected_list.append(line[:-1])
        self.download_list=selected_list
        
    def run(self, p1, p2, paired):
        #write to qsub file
        qsub_path_single=self.pwd+"/Cache/DCC_single.qsub"
        self.env_single.write2qsub(qsub_path_single)
        qsub_path_paired=self.pwd+"/Cache/DCC_paired.qsub"
        self.env_paired.write2qsub(qsub_path_paired)
        ###########################
        os.makedirs(self.dcc_out_dir+'/'+self.download_name+"/"+self.download_name+"_"+p1+"_"+p2,exist_ok=True)
        ###########################
        os.chdir(self.dcc_out_dir)
        #qsub DCC2.qsub cell_type p1 p2
        if (paired):
            bash="qsub "+qsub_path_paired+ " " + self.download_name+ " "+ str(p1)+ " "+ str(p2);
        else:
            bash="qsub "+qsub_path_single+ " " + self.download_name+ " "+ str(p1)+ " "+ str(p2);
        print(bash);
        os.system(bash);
        
        #listen qstat
        self.qstat_listen()
        
        #go back
        os.chdir(self.pwd)
        self.code=1;
        
    def qstat_listen(self):
        # it is a listenning funtion. Tracking the tasks not finished.
        qstat=os.popen('qstat -u '+self.user).readlines()
        tasks=len(qstat)-2
        '''
        for item in qstat:
            print(item,end='$$$')
        '''
        flag='F';
        print('----------------------------------------')
        print("Tasks are running. Remaining Tasks:")
        print(tasks)
        while (tasks>0 and flag=='F'):
            flag=input("""If you wanna keep tracking Remaining Tasks, Press F.
Leave Right now, Press any other keys.
Caution: Before starting next part of DCC, please make sure all tasks are done. \n""")
            qstat=os.popen('qstat -u '+self.user).readlines()
            tasks=len(qstat)-2
            print('----------------------------------------')
            print("Tasks are running. Remaining Tasks:")
            print(tasks)
    
    
    
if __name__=="__main__":
        DCC_helper.start()
        

