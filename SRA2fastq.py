# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 14:02:49 2022

@author: Minty_Lin

1.convert SRA to fastq

"""
import os
import sys
import re
from enviroment import qsub_para

class SRA2fastq_helper(object):
    version="beta"
    def __init__(self, download_name, user):
        self.download_name=download_name
        self.user=user;              #SCC username
        self.download_list= None
        self.download_name= download_name   #download_name is the keyword witout space
        self.code=0; #downloading has been done or not
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        
        #read module
        #module json path
        module_json = self.pro_path+"/bash_files/module_fastqdump.json"
        #Working place json file path
        pwd_json= self.pwd+"/Cache/fastqdump.json"
        #Do working place has the json file? if not, read the module json and write a new one
        os.makedirs(self.pwd+'/Cache',exist_ok=True)
        if not(os.path.exists(pwd_json)):
            self.env=qsub_para.read_json("fastqdump", module_json)
            self.env.write2json(pwd_json)
        else:
            self.env=qsub_para.read_json("fastqdump", pwd_json)
        
            
        
    def start():
        print('----------------------------------------------------')
        print("Hi, I am SRA2fastq_helper")
        print("Version: "+SRA2fastq_helper.version)
        print("I assume SRR documents are in ./Sample/<key_word>/SRA_files/<SRA files> and a SRA_list is in the ./Cache ")
        download_name=input("Please input the keyword(eg. ES_cell):")
        
        SRA2fastq_helper.func(download_name)
        
    def func(download_name, user='minty'):
        '''
        Parameters
        ----------
        download_name : string
            Key word of the sample (eg. 'ES_cell')
        user: string 
            username of SCC, to qsub missions.
        Returns
        -------
        download_name,
        code int, 0 or 1
        '''
        fastq=SRA2fastq_helper(download_name, user)
        #read the download list
        fastq.readlist()
        #define the path of fastq file
        fastqpath=fastq.pwd+"/Sample/"+fastq.download_name+"/fastqgz"
        os.makedirs(fastqpath,exist_ok=True)
        fastq.download(fastqpath)
        
        return (download_name, fastq.code)
    
    def readlist(self):
        selected_list=[]
        path_list=self.pwd+"/Cache/"+self.download_name+".txt"
        with open(path_list,'rt') as f:
            for line in f.readlines():
                selected_list.append(line[:-1])
        self.download_list=selected_list
    
    def download(self, fastqpath):
        qsub_path=self.pwd+"/Cache/fastqdump.qsub"
        self.env.write2qsub(qsub_path)
        os.chdir(fastqpath)
        for SRR in self.download_list:
            SRR_path=self.pwd+"/Sample/"+self.download_name+"/SRA_files/"+SRR+"/"+SRR+".sra"
            bash="eval qsub "+qsub_path+" "+SRR_path
            #print(bash)
            os.system(bash)
            
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
    SRA2fastq_helper.start()
        
    
        
