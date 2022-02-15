# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 14:39:26 2022

@author: Minty_Lin
"""

import pandas as pd
import os

class SraRunTable_helper(object):
    version='beta'
    def __init__(self, path,user):
        #path is the path o SraRunTable
        self.path=path;
        if (path!='None'):
            self.data=pd.read_csv(path);
        self.user=user;              #SCC username
        self.download_list= None;
        self.download_name= None   #download_name is the keyword witout space
        self.prefetch_path='/restricted/projectnb/casa/mtLin/sratoolkit.2.11.2-centos_linux64/bin/prefetch'
        self.qsub_setting='-P casa -pe omp 8 -cwd -o log_o -e log_e'
        self.code=0;
        
        
    def env_setting(self):
        print("----------------------------------------------------------------------------")
        print("1. sratoolkit path:"+self.prefetch_path)
        print("2. qsub setting:"+self.qsub_setting)
        print("E. Back")
        print("----------------------------------------------------------------------------")
        flag=input('What you want to reset: ')
        if (flag == 'E'): return None
        if (flag == '1'):
            self.prefetch_path=input('Input the new path to prefetch: ')
        if (flag == '2'):
            self.qsub_setting=input('Input the new qsub setting: ')
            
    def start():
        print("Hi, I am SraRunTable Downloading Helper. Author: Minty")
        print("Version: "+SraRunTable_helper.version)
       
        SraRunTable_helper.func()
    
    def func(user='minty'):
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
            print("Saving to "+ write_path)
            with open(write_path,'wb') as f:
                for SRR in selected_list:
                    f.write(bytes(SRR+'\n','utf-8'))
                    
        flag='kn'
        while(not(flag=='y' or flag=='n')):
            flag=input("Do you want to save this list for later downloading? (y/n)")
        if (flag=='y'): 
            self.download_list=selected_list.copy()
            self.download_name=self.space2dash(key_value)
            
                
    def download_entry(self):
        #flag_cache=='n', using an external txt file as list, =='y',using cache as list
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
        
        #make dir
        home=os.getcwd()
        SRA_file_path='./Sample/'+self.download_name+'/SRA_files'
        os.makedirs( SRA_file_path,exist_ok=True)
        os.chdir('./'+SRA_file_path)
        
        #Write a temp qsub file
        with open('temp.qsub','wb') as f:
            f.write(bytes('#! /bin/bash -l'+'\n','utf-8'))
            f.write(bytes('#$ '+self.qsub_setting+'\n','utf-8'))
            f.write(bytes(self.prefetch_path+' ${1}'+'\n','utf-8'))
            
        #download
        for SRR in self.download_list:
            bash='eval qsub temp.qsub ' + SRR
            #print(bash)
            os.system(bash)
        
        #listen qstat
        self.qstat_listen()

        os.chdir(home)
        self.code=1;
        
    
    def download_txt(self):
        #download SRA from a txt file
        path=input("The path to SRA number file(only include SRA number): ")
        selected_list=[]
        with open(path,'rt') as f:
            for line in f.readlines():
                selected_list.append(line[:-1])
        
        print("Saving the file")
        self.download_list=selected_list.copy()
        self.download_name=self.space2dash(path[:-4])
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
            flag=input("If you wanna keep tracking Remaining Tasks, Press F. \n \
Leave Right now, Press any other keys \n \
Caution: Before starting next part of DCC, please make sure all tasks are done. \n")
            qstat=os.popen('qstat -u '+self.user).readlines()
            tasks=len(qstat)-2
            print('----------------------------------------')
            print("Tasks are running. Remaining Tasks:")
            print(tasks)
            
    def space2dash(self, string):
        return string.replace(' ','_')
    
        
if __name__=='__main__':
    SraRunTable_helper.start()

