# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 17:17:28 2022

@author: Minty_Lin

star alignment helper
convert fastq.gz to bam/bai file
"""
import os
import sys
from enviroment import qsub_para

class star_helper():
    version="beta"
    def __init__(self,project_name, download_name, user):
        self.download_name=download_name
        self.user=user;              #SCC username
        #self.download_list= None
        self.download_name= download_name   #download_name is the keyword witout space
        self.code=0; #downloading has been done or not
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        self.star_out=self.pwd+'/Run/Star'
        
        #module json path
        module_json_single = self.pro_path+"/bash_files/module_star_single.json"
        module_json_paired = self.pro_path+"/bash_files/module_star_paired.json"
        #Working place json file path
        pwd_json_single= self.pwd+"/Cache/star_single.json"
        pwd_json_paired= self.pwd+"/Cache/star_paired.json"

        os.makedirs(self.pwd+'/Cache',exist_ok=True)
        os.makedirs(self.pwd+'/Cache/tmpdir',exist_ok=True)
        #create the star working place
        os.makedirs(self.star_out+'/'+self.download_name,exist_ok=True)
        #Do working place has the json file? if not, read the module json and write a new one
        if not(os.path.exists(pwd_json_single)):
            self.env_single=qsub_para.read_json("star_single", module_json_single)
            #rewrite the output directory of star
            self.env_single.set_dic_p2p('star_out_dir', self.star_out+"/${cell_type}")
            #rewrite the cache file path for star
            self.env_single.set_dic_p2p('Tmpdir', self.pwd+'/Cache/tmpdir')
            #reset the path of startool to DCC-kit
            STARDir=self.pro_path+"/DCC-kit/STAR-2.6.1c/bin/Linux_x86_64/"
            self.env_single.set_dic_p2p('STARDir', STARDir)
            #reset the path of picard
            picard=self.pro_path+"/DCC-kit/picard.jar"
            self.env_single.set_dic_p2p('picard', picard)
            #reset project name
            self.env_single.set_dic_p2p("project_name",project_name)
            
            self.env_single.write2json(pwd_json_single)
        else:
            self.env_single=qsub_para.read_json("star_single", pwd_json_single)
            
        if not(os.path.exists(pwd_json_paired)):
            self.env_paired=qsub_para.read_json("star_paired", module_json_paired)
            #rewrite the output directory of star
            self.env_paired.set_dic_p2p('star_out_dir', self.star_out+"/${cell_type}")
            #rewrite the cache file path for star
            self.env_paired.set_dic_p2p('Tmpdir', self.pwd+'/Cache/tmpdir')
            #reset the path of startool to DCC-kit
            STARDir=self.pro_path+"/DCC-kit/STAR-2.6.1c/bin/Linux_x86_64/"
            self.env_paired.set_dic_p2p('STARDir', STARDir)
            #reset the path of picard
            picard=self.pro_path+"/DCC-kit/picard.jar"
            self.env_paired.set_dic_p2p('picard', picard)
            #reset project name
            self.env_paired.set_dic_p2p("project_name",project_name)
            
            self.env_paired.write2json(pwd_json_paired)
        else:
            self.env_paired=qsub_para.read_json("star_paired", pwd_json_paired)
        
        #reset the seq_len
        #why I choose this place to reset the length of seq? Because I could reset the length no matter whether the module is download/save
        #it would not change json file
        seq_len=input("Please give me the length of the sequence(50, 75, 100): ")
        #reset the path of genome index of GrCh38
        genomeDir=self.pro_path+"/Genome_index/GrCh38_"+str(seq_len)+"n"
        self.env_single.set_dic_p2p('genomeDir', genomeDir)
        self.env_paired.set_dic_p2p('genomeDir', genomeDir)
            
    def start():
        print('----------------------------------------------------')
        print("Hi, I am star_helper")
        print("Version: "+star_helper.version)
        print("I assume fastqgz documents are in ./Sample/<key_word>/fastqgz/ and a SRA_list is in the ./Cache ")
        download_name=input("Please input the keyword(eg. ES_cell):")
        project_name=input("Please input the project name: ")
        star_helper.func(project_name, download_name)
    def func(project_name, download_name, user='minty'):
        st=star_helper(project_name, download_name, user)
        st.readlist()
        gzpath=st.pwd+"/Sample/"+st.download_name+"/fastqgz"
        st.run(gzpath)
        
        return (download_name, st.code)
    
    def readlist(self):
        selected_list=[]
        path_list=self.pwd+"/Cache/"+self.download_name+".txt"
        with open(path_list,'rt') as f:
            for line in f.readlines():
                selected_list.append(line[:-1])
        self.download_list=selected_list
        
    def run(self, gzpath):
        #write to qsub file
        qsub_path_single=self.pwd+"/Cache/star_single.qsub"
        self.env_single.write2qsub(qsub_path_single)
        qsub_path_paired=self.pwd+"/Cache/star_paired.qsub"
        self.env_paired.write2qsub(qsub_path_paired)
        #################
        #create the star outcome:samplesheet
        os.makedirs(self.star_out+'/'+self.download_name+"/sample_sheet",exist_ok=True)
        #create the star outcome:mate1
        os.makedirs(self.star_out+'/'+self.download_name+"/mate1",exist_ok=True)
        #create the star outcome:mate2
        os.makedirs(self.star_out+'/'+self.download_name+"/mate2",exist_ok=True)
        #################
        os.chdir(self.star_out)
        for SRR in self.download_list:
            SRR_path=gzpath+"/"+SRR
            #single-end ? paired-end?
            if (os.path.exists(SRR_path+"_2.fastq.gz")):
                bash="eval qsub "+qsub_path_paired+" "+gzpath+" "+SRR+" "+self.download_name
                print("paired seq")
            else:
                bash="eval qsub "+qsub_path_single+" "+gzpath+" "+SRR+" "+self.download_name
                print("single seq")
                
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
    star_helper.start()
        
        
        
        
        
        
        
        
        
        
        
        
        
        