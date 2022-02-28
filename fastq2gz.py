# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 14:44:09 2022

@author: Minty_Lin

2. convert SRA to fastq.gz
"""
import os
import sys
from enviroment import qsub_para

class fastq2gz_helper(object):
    version="beta"
    def __init__(self, download_name, user):
        self.download_name=download_name
        self.user=user;              #SCC username
        #self.download_list= None
        self.download_name= download_name   #download_name is the keyword witout space
        self.code=0; #downloading has been done or not
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        
        #module json path
        module_json_single = self.pro_path+"/bash_files/module_gzip_single.json"
        module_json_paired = self.pro_path+"/bash_files/module_gzip_paired.json"
        #Working place json file path
        pwd_json_single= self.pwd+"/Cache/gzip_single.json"
        pwd_json_paired= self.pwd+"/Cache/gzip_paired.json"
        #Do working place has the json file? if not, read the module json and write a new one
        os.makedirs(self.pwd+'/Cache',exist_ok=True)
        if not(os.path.exists(pwd_json_single)):
            self.env_single=qsub_para.read_json("gzip_single", module_json_single)
            self.env_single.write2json(pwd_json_single)
        else:
            self.env_single=qsub_para.read_json("gzip_single", pwd_json_single)
            
        if not(os.path.exists(pwd_json_paired)):
            self.env_paired=qsub_para.read_json("gzip_single", module_json_paired)
            self.env_paired.write2json(pwd_json_paired)
        else:
            self.env_paired=qsub_para.read_json("gzip_single", pwd_json_paired)
        
        
    def start():
        print('----------------------------------------------------')
        print("Hi, I am fastq2gz_helper")
        print("Version: "+fastq2gz_helper.version)
        print("I assume fastq documents are in ./Sample/<key_word>/fastqgz/ and a SRA_list is in the ./Cache ")
        download_name=input("Please input the keyword(eg. ES_cell):")
        
        fastq2gz_helper.func(download_name)
        
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
        gz=fastq2gz_helper(download_name, user)
        gz.readlist()
        gzpath=gz.pwd+"/Sample/"+gz.download_name+"/fastqgz"
        gz.convert(gzpath)
        
        return (download_name, gz.code)
    
    def readlist(self):
        selected_list=[]
        path_list=self.pwd+"/Cache/"+self.download_name+".txt"
        with open(path_list,'rt') as f:
            for line in f.readlines():
                selected_list.append(line[:-1])
        self.download_list=selected_list
    
    def convert(self, gzpath):
        qsub_path_single=self.pwd+"/Cache/gzip_single.qsub"
        self.env_single.write2qsub(qsub_path_single)
        qsub_path_paired=self.pwd+"/Cache/gzip_paired.qsub"
        self.env_paired.write2qsub(qsub_path_paired)
        ####################################################
        os.chdir(gzpath)
        for SRR in self.download_list:
            SRR_path=gzpath+"/"+SRR
            #single-end ? paired-end?
            if (os.path.exists(SRR_path+"_2.fastq")):
                bash="eval qsub "+qsub_path_paired+" "+SRR_path
            else:
                bash="eval qsub "+qsub_path_single+" "+SRR_path
                
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
        
if __name__=='__main__':
    fastq2gz_helper.start()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

