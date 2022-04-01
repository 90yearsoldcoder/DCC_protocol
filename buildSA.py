# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:07:31 2022

@author: Minty_Lin
"""
import os
import sys
from enviroment import qsub_para


class build_index(object):
    version="v0.2"
    def __init__(self,user):
        self.user=user;
        self.code=0; #downloading has been done or not
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        
        os.makedirs(self.pro_path+'/Genome_index/GrCh38_100n',exist_ok=True)
        module_json=self.pro_path+"/bash_files/create_index.json"
        self.env=qsub_para.read_json("create_index", module_json)
        #reset STAR dir
        STARDir=self.pro_path+"/DCC-kit/STAR-2.6.1c/bin/Linux_x86_64/"
        self.env.set_dic_p2p("STARDir", STARDir)
        #reset genome directory
        SA_file_path=self.pro_path+'/Genome_index/GrCh38_100n'
        self.env.set_dic_p2p("SA_file_path", SA_file_path)
        #reset reference_path
        reference_path=self.pro_path+"/DCC-kit/GRCh38.primary_assembly.genome.fa"
        self.env.set_dic_p2p("reference_path", reference_path)
        #reset annotation_path
        annotation_path=self.pro_path+"/DCC-kit/ref/gencode.v26.primary_assembly.annotation.gtf"
        self.env.set_dic_p2p("annotation_path", annotation_path)
        
    def func(user="minty"):
        print("-------------------------------------")
        print("We are going to build the suffix array for alignments")
        print("Please make sure you have download DCC-kit to the program_path")
        print("-------------------------------------")
        bi=build_index(user);
        bi.build()
        
    def build(self):
        qsub_path=self.pro_path+"/Genome_index/create_index.qsub"
        self.env.write2qsub(qsub_path)
        SA_path=self.pro_path+"/Genome_index"
        os.chdir(SA_path)
        bash="qsub "+qsub_path
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
    user=input("Please give me your user name for qsub tasks: ")
    build_index.func(user);
        
        
        
        
        
        
        