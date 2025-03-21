# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 15:22:22 2022

Merge helper, used to merge sample sheet for DCC input
@author: Minty_Lin
"""
import os

class Merge_helper(object):
    version='beta'
    def __init__(self,key_value, paired):
        self.key_value=key_value;
        self.paired=paired
        self.SRR_list=[]
        self.pwd=os.getcwd()
        self.numPerGroup = 100

    def start():
        print("This is merge_helper alone without other parts of DCC_helper. Version:", Merge_helper.version)
        print('---------------------------------------------')
        print("An SRR number list should be in Cache folder, and the name of it should be key_value")
        key_value=input("Please give me the key_value(or said cell_type): ")
        print('---------------------------------------------')
        paired='kn'
        while(not(paired=='s' or paired=='d')):
            paired=input("Please tell me it is single-paired data or double-paired data? (s/d)")
        print('---------------------------------------------')
        if (paired=='s'):
            print("Path of bam file should be ./Run/Star/<key-value>/sample_sheet/<SRR_num>_Aligned.sortedByCoord.out.bam")
            print("Path of junc file should be ./Run/Star/<key-value>/sample_sheet/<SRR_num>_Chimeric.out.junction")
        else:
            print("Path of bam file should be ./Run/Star/<key-value>/sample_sheet/<SRR_num>_Aligned.sortedByCoord.out.bam")
            print("Path of junc file for both should be ./Run/Star/<key-value>/sample_sheet/<SRR_num>_Chimeric.out.junction")
            print("Path of junc1 file should be ./Run/Star/<key-value>/mate1/<SRR_num>_1.fastq.gz_Chimeric.out.junction")
            print("Path of junc2 file should be ./Run/Star/<key-value>/mate2/<SRR_num>_2.fastq.gz_Chimeric.out.junction")
        continue_flag=input("Press any key to continue")
        print('---------------------------------------------')
        Merge_helper.func(key_value, paired)
        
    def func(key_value):
        paired='d'
        Merge=Merge_helper(key_value, paired)
        Merge.read_SRR_list()
        #print(Merge.pwd+"/Sample/"+Merge.key_value+"/fastqgz/"+Merge.SRR_list[0]+"_2.fastq.gz")
        if os.path.exists(Merge.pwd+"/Sample/"+Merge.key_value+"/fastqgz/"+Merge.SRR_list[0]+"_2.fastq.gz"):
            print("I think they are paired-end sequences.")
            paired='d';
        else:
            print("I think they are single-end sequences.")
            paired='s';
        
        Merge.paired=paired

        Merge.numPerGroup = int(input("The number of Sample per group, for qsub running only(not for phenotype): "))
        
        st_line = 0
        ed_line = min(len(Merge.SRR_list), st_line + Merge.numPerGroup) - 1
        ind = 0

        while (ed_line < len(Merge.SRR_list)):
            if (paired=='d'): 
                Merge.write_paired(ind, st_line, ed_line)
            if (paired=='s'):
                Merge.write_single(ind, st_line, ed_line)
            st_line = ed_line + 1
            ind += 1
            if ed_line == len(Merge.SRR_list) - 1:
                break
            ed_line = min(len(Merge.SRR_list), st_line + Merge.numPerGroup) - 1
            
        return ind
        
    def read_SRR_list(self):
        path='./Cache/'+self.key_value+'.txt' #path of SRR list
        with open(path,'rt') as f:
            for line in f.readlines():
                self.SRR_list.append(line[:-1])
                
    def write_paired(self, ind, st_line, ed_line):
        os.makedirs( f'./Run/DCC/'+self.key_value + f'/DCC_InputFiles_{ind}',exist_ok=True)
        
        #both junc to samplesheet
        path='./Run/DCC/'+self.key_value+ f'/DCC_InputFiles_{ind}/samplesheet'
        prefix=self.pwd+'/Run/Star/'+self.key_value+'/sample_sheet/'
        suffix='_Chimeric.out.junction'
        self.writetofile(path,prefix,suffix, st_line, ed_line)
        
        #mate1 junc to mate1
        path='./Run/DCC/'+self.key_value+f'/DCC_InputFiles_{ind}/mate1' 
        prefix=self.pwd+'/Run/Star/'+self.key_value+'/mate1/'
        suffix='_1.fastq.gz_Chimeric.out.junction'
        self.writetofile(path,prefix,suffix, st_line, ed_line)
        
        #mate2 junc to mate2
        path='./Run/DCC/'+self.key_value+f'/DCC_InputFiles_{ind}/mate2'
        prefix=self.pwd+'/Run/Star/'+self.key_value+'/mate2/'
        suffix='_2.fastq.gz_Chimeric.out.junction'
        self.writetofile(path,prefix,suffix, st_line, ed_line)
        
        #bam to bam_files
        path='./Run/DCC/'+self.key_value+f'/DCC_InputFiles_{ind}/bam_files' 
        prefix=self.pwd+'/Run/Star/'+self.key_value+'/sample_sheet/'
        suffix='_Aligned.sortedByCoord.out.bam'
        self.writetofile(path,prefix,suffix, st_line, ed_line)
        
    def write_single(self, ind, st_line, ed_line):
        os.makedirs( './Run/DCC/'+self.key_value+ f'/DCC_InputFiles_{ind}',exist_ok=True)
        
        #both junc to samplesheet
        path='./Run/DCC/'+self.key_value + f'/DCC_InputFiles_{ind}/samplesheet'
        prefix=self.pwd+'/Run/Star/'+self.key_value+'/sample_sheet/'
        suffix='_Chimeric.out.junction'
        self.writetofile(path,prefix,suffix, st_line, ed_line)
        #bam to bam_files
        path='./Run/DCC/'+self.key_value+f'/DCC_InputFiles_{ind}/bam_files' 
        prefix=self.pwd+'/Run/Star/'+self.key_value+'/sample_sheet/'
        suffix='_Aligned.sortedByCoord.out.bam'
        self.writetofile(path,prefix,suffix, st_line, ed_line)
        
    def writetofile(self, path, prefix, suffix, st_line, ed_line):
        with open(path,'wb') as f:
            for line, cellnum in enumerate(self.SRR_list):
                if line < st_line or line > ed_line:
                    continue
                f.write(bytes(prefix+cellnum+suffix+'\n','utf-8'))
        
        
        
        


if __name__=='__main__':
    print('This main')
    Merge_helper.start()

