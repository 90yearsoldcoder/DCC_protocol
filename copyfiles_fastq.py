# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 15:01:07 2022

@author: Minty_Lin

cp fastq files to the working directory.
copy files from a input directory to ./Sample/keyword/fastqgz/
generate a list

os.listdir(filePath)

"""
import os
import sys
from enviroment import qsub_para

class copy_fastq(object):
    version="v0.2"
    def __init__(self, project_name, origin, dest, download_name, user):
        self.download_name= download_name   #download_name is the keyword witout space
        self.code=0; #downloading has been done or not
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        self.origin=origin
        self.dest=dest 
        self.user=user;
        #read module
        #module json path
        module_json = self.pro_path+"/bash_files/module_copy.json"
        #Working place json file path
        pwd_json= self.pwd+"/Cache/module_copy.json"
        #Does working place have the json file? if not, read the module json and write a new one
        os.makedirs(self.pwd+'/Cache',exist_ok=True)
        if not(os.path.exists(pwd_json)):
            self.env=qsub_para.read_json("copyfiles", module_json)
            #reset the dest path
            #dest=self.pwd+"/Sample/"+self.download_name+"/fastqgz/"
            #print(dest)
            self.env.set_dic_p2p("dest", self.dest)
            #reset the project name
            self.env.set_dic_p2p("project_name",project_name)
            
            self.env.write2json(pwd_json)
            
        else:
            self.env=qsub_para.read_json("copyfiles", pwd_json)
        
        
    def start():
        print("--------------------------")
        origin=input("Please give me the path to Fastq files(eg home/test/samples):")
        if (origin[-1]=='/'):
            origin=origin[:-1]
        sample_name=input("Please give me the name for those samples(eg ES_cell):")
        user=input('Username:')
        print("--------------------------")
        dest=os.getcwd()+"/Sample/"+sample_name+"/fastqgz"
        print("--------------------------")
        project_name=input("Please input the project name: ")
        copy_fastq.func(project_name, origin,dest,sample_name, user)
        
    def func(project_name,origin, dest, download_name, user='minty'):
        cf=copy_fastq(project_name, origin, dest, download_name, user)
        flag=cf.read_dir()
        if (flag==0):
            print("the file list is not decided")
            return (None, 0);
        cf.copyto()
        return (cf.download_name, cf.code)
        
    def read_dir(self):
        print("--------------------------")
        print("If those samples are paired-ends, the name should be like <..>_1.fastq and <...>_2.fastq")
        print("If those samples are single-ends, the name should be like <..>_1.fastq")
        print("Example: SRR001_1.fastq, SRR001_2.fastq")
        print("--------------------------")
        temp_list=[]
        all_files=os.listdir(self.origin)
        for file in all_files:
            if (file[-8:]=="_1.fastq" or  file[-8:]=="_2.fastq"):
                temp_list.append(file)
        print("We detected those samples: ")
        print(temp_list)
        flag=input("Do you want to use those samples?(y/n):")
        if (flag=='n'):
            return 0
        self.copy_list=temp_list.copy()
        self.download_list=[]
        for file in temp_list:
            if (file[:-8] not in self.download_list):
                self.download_list.append(file[:-8])
        #save the list to Cache dir
        write_path=self.pwd+'/Cache/'+self.download_name+'.txt'
        with open(write_path,'wb') as f:
            for SRR in self.download_list:
                f.write(bytes(SRR+'\n','utf-8'))
        print("Saved to "+ write_path)
        
        return 1
    
    def copyto(self):
        #write qsub files
        qsub_path=self.pwd+"/Cache/copy.qsub"
        self.env.write2qsub(qsub_path)
        #make the directory ./Sample/<keyword>/fastq
        os.makedirs(self.dest,exist_ok=True)
        #copy them to dest
        for file in self.copy_list:
            bash="qsub "+ qsub_path+" "+ self.origin+"/"+file
            print(bash)
            os.system(bash);
            
        #listen qstat
        self.qstat_listen()
        
        self.code=1
        
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
    copy_fastq.start()
