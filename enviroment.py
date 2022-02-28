# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:11:24 2022

@author: Minty_Lin

Enviroment Setting for DCCprotocol
"""
import json

class qsub_para(object):
    def __init__(self, name ,dic):
        self.name=name
        self.dic=dic
    def init_dic():
        #it is a json generate function. only used for initiate
        #Please don't use it, if you are not familiar with the program. 
        print("--------------------------------------------")
        print("Please dont use it if you are not familiar with this program, since it might damage the whole program.")
        print("I am initiating tool for DCCprotocol, which is used for generating new json for the program")
        name=input("The new file name: ")
        dic={}
        while(1):
            print("--------------------------------------------")
            p_name=input("The name of new parameter('E to Exit'): ")
            if (p_name=='E'):
                break
            p_setting=input("Setting of "+p_name+" : ")
            p_hiden=input("Setting of hiden(y/n): ")
            p_withslash=input("With slash(y/n):")
            dic[p_name]={'Setting':p_setting, 'Hidden':p_hiden, 'withslash': p_withslash, 'silent':False}
        print("________________________________________")
        flag=input("Save them to ./bashfiles/"+name+".json ? (y/n): ")
        if (flag=='y'):
            new=qsub_para(name,dic)
            new.view_dic()
            new.write2json("./bashfiles/"+new.name+".json")
        else:
            print("Not save")
            
    def read_json(name, path):
        '''
        Parameters
        ----------
        name : str
            name of the json file.
        path : TYPE
            the path to json file
        Returns
        -------
        A qsub_para class containing the dic in the json file.

        '''
        # Opening JSON file
        with open(path) as json_file:
            dic = json.load(json_file)
        return qsub_para(name,dic)
        
        
    def view_dic(self):
        print("-------------------------------------------")
        for key in self.dic.keys():
            if (self.dic[key]['Hidden'] != 'y'):
                print(key+": "+ self.dic[key]['Setting'])
        print("------------------------------------------")
    def set_dic(self, path):
        while(1):
            self.view_dic()
            key_i=input("Enter the parameter you wantna modify(full name, E for Exit): ")
            if (key_i=='E'):
                break
            if (key_i in self.dic.keys()):
                item_i=input("Change it to: ")
                self.dic[key_i]['Setting']=item_i
            else:
                print("No such parameter exists")
        
        print("--------------------------------------------")
        flag=input("Save the new setting to "+path+" (y/n): ")
        if (flag=='y'):
            self.write2json(path)
    
    def silent(self, key, path):
        self.dic[key]['silent']=True
        self.write2json(path)
            
    def write2qsub(self, path):
        with open(path,'wb') as f:
            for key in self.dic.keys():
                if (self.dic[key]['silent']==False):
                    if (self.dic[key]['withslash']=='y'):
                        f.write(bytes(self.dic[key]['Setting']+'  ','utf-8'))
                    else:
                        f.write(bytes(self.dic[key]['Setting']+'\n','utf-8'))
                
    def write2json(self, path):
        with open(path, "w") as outfile:
            json.dump(self.dic, outfile, indent=4)
    
if __name__=='__main__':
    qsub_para.init_dic()