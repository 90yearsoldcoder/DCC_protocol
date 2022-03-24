# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 14:39:26 2022

@author: Minty_Lin
"""

import pandas as pd
import os
import sys
import shutil
import re
from enviroment import qsub_para

class SraRunTable_helper(object):
    version='beta'
    def __init__(self, path,user):
        #path is the path to SraRunTable
        self.path=path;
        if (path!='None'):
            self.data=pd.read_csv(path);
        self.user=user;              #SCC username
        self.download_list= None;
        self.download_name= None   #download_name is the keyword witout space
        self.code=0; #downloading has been done or not
        self.pro_path=sys.path[0]
        self.pwd=os.getcwd()
        
        #read module
        #module json path
        module_json = self.pro_path+"/bash_files/module_SRA_download.json"
        #Working place json file path
        pwd_json= self.pwd+"/Cache/SRA_download.json"
        #Do working place has the json file? if not, read the module json and write a new one
        os.makedirs(self.pwd+'/Cache',exist_ok=True)
        if not(os.path.exists(pwd_json)):
            self.env=qsub_para.read_json("SRA_download", module_json)
            self.env.write2json(pwd_json)
        else:
            self.env=qsub_para.read_json("SRA_download", pwd_json)
        
    
    def env_setting(self):
        pwd_json= self.pwd+"/Cache/SRA_download.json"
        self.env.set_dic(pwd_json)
            
    def start():
        print('----------------------------------------------------')
        print("Hi, I am SraRunTable Downloading Helper.")
        print("Version: "+SraRunTable_helper.version)
       
        SraRunTable_helper.func()
    
    def func(user='minty'):
        '''
        This is the entry function for SRAdownload
        Parameters
        ----------
        user : string, optional
            DESCRIPTION. The default is 'minty'.
        Returns a tuple
        -------
        download_name: string
            the name of cell_type(or other key word) 
        int 0 or 1
            Download or not

        '''
        #print the working directory
        os.system('echo Working directory: ')
        os.system('pwd')
        
        #enter the path of SraRunTable.txt
        path = input("The path To the SraRunTable.txt(If you already have a SRR_numbertxt, enter'None'): ")
        Sra = SraRunTable_helper(path,user)
        
        ###################################
        in_flag=True
        while(in_flag):
            print("----------------------------------------------------------------------------")
            print("--------------SraRunTable Downloading Helper--------------------------------")
            print("Function I have:")
            print("1. Have a brief look at all data")
            print("2. Have a look at the columns' names")
            print("3. Have a look at the values in a specific column")
            print("4. Acquire SRA numbers for the row having a specific value in a specific colunm")
            print("5. Download SRR documents according to the SRA number in txt file")
            print("S. Enviorment_Setting")
            print("E. Exit()")
            print("----------------------------------------------------------------------------")
            func_num=input("Input the number before the function you need: ")
            print("----------------------------------------------------------------------------")
            if (func_num=='E'): break;
            if (func_num=='S'): Sra.env_setting();
            if (func_num=='1'): Sra.check_all();
            if (func_num=='2'): Sra.check_column();
            if (func_num=='3'): Sra.check_value();
            if (func_num=='4'): Sra.select();
            if (func_num=='5'): Sra.download_entry();
        
        return (Sra.download_name, Sra.code)
        
    def check_all(self):
        print("Brief Look: ")
        print(self.data)
    def check_column(self):
        print("Columns' names: ")
        print(self.data.columns)
    def check_value(self):
        column_name=input("Please input the name of key column: ")
        if (column_name in self.data.columns):
            value=[]
            for item in self.data[column_name]:
                if item not in value:
                    value.append(item)
            print(value)
        else:
            print("The key column does not exist.")
    
    def select(self):
        '''
        Parameters
        ----------
        Returns LIST  The list of SRA number selected
        -------
        key_name : STRING   The name of key column
        key_value : STRING  The value selected.
        '''
        key_name=input("please input the column name: ")
        key_value=input("please input the value: ")
        ################################################
        temp_data=list(self.data[key_name])
        temp_Run=list(self.data['Run'])
        selected_list=[]
        for i in range(len(temp_data)):
            if (temp_data[i]==key_value):
                selected_list.append(temp_Run[i])
        print(selected_list)
        
        flag='kn'
        while(not(flag=='y' or flag=='n')):
            flag=input("Do you want to save the list as a txt document? (y/n)")
            
        if (flag=='y'):
            os.makedirs( './Cache',exist_ok=True)
            write_path='Cache/'+self.space2dash(key_value)+'.txt'
            with open(write_path,'wb') as f:
                for SRR in selected_list:
                    f.write(bytes(SRR+'\n','utf-8'))
            print("Saved to "+ write_path)
                    
        flag='kn'
        while(not(flag=='y' or flag=='n')):
            flag=input("Do you want to save this list for later downloading? (y/n)")
        if (flag=='y'): 
            self.download_list=selected_list.copy()
            self.download_name=self.space2dash(key_value)
            
                
    def download_entry(self):
        #flag_cache=='n', using an external txt file as list, =='y',using cache as the list
        flag_cache='n'
        if (self.download_list != None):
            flag='kn'
            while(not(flag=='y' or flag=='n')):
                flag=input("Do you want to use the list saved in step 4 ? (y/n)")
            flag_cache=flag
        
        if (flag_cache=='y'):
            self.download_cache()
        elif (flag_cache=='n'):
            self.download_txt()
        
    def download_cache(self):
        #download SRA from cache
        
        #write qsub file to Cache according to json file
        pwd_json= self.pwd+"/Cache/SRA_download.qsub"
        self.env.write2qsub(pwd_json)
        #print(os.getcwd())
        SRA_file_path='./Sample/'+self.download_name+'/SRA_files'
        #print(SRA_file_path)
        os.makedirs( SRA_file_path, exist_ok=True)
        os.chdir(SRA_file_path)
        #print(os.getcwd())
        
        #prepare temp.qsub
        #SraRunTable_helper.module_copy(self.pwd+"/Cache/SRA_download.qsub", os.getcwd()+"/temp.qsub")
        
        #download
        for SRR in self.download_list:
            bash="eval qsub "+self.pwd+ "/Cache/SRA_download.qsub " + SRR
            print(bash)
            os.system(bash)
        
        #listen qstat
        self.qstat_listen()

        os.chdir(self.pwd)
        self.code=1;
        
    
    def download_txt(self):
        #download SRA according to the txt file
        path=input("The path to SRA number file(which only includes SRA number): ")
        selected_list=[]
        with open(path,'rt') as f:
            for line in f.readlines():
                selected_list.append(line[:-1])
        
        print("Read the file")
        self.download_list=selected_list.copy()
        #using Regexp to gain the name of txt
        t=re.compile(r"[^\/]+\.txt")
        full_name=re.search(t,path)
        name=full_name.group(0)
        self.download_name=self.space2dash(name[0:-4])
        #print(self.download_list)
        #print(self.download_name)
        self.download_cache()
        
    
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
            
    def space2dash(self, string):
        return string.replace(' ','_')
    
        
if __name__=='__main__':
    SraRunTable_helper.start()

