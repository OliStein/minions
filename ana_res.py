'''
Created on Jun 1, 2015

@author: Oli
'''
import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import shutil as st
import pickle 
from time import strftime, localtime, time
import time
import glob

from csv_list_class import csv_list
from gen_class import gen
from list_class import lists
# from astropy.io.fits.header import Header

l = lists()
c = csv_list()
g = gen() 

class ana_res():
    def __init__(self):
        self.test = 0
    
    
    def rosy_dir_creator(self,cwd,pflag):
        g.tprinter('Running daq_dir_creator',pflag)
        
        
        if not os.path.exists(cwd):
            g.printer('creating daq dir',pflag)
            os.mkdir(cwd)
        else:
            pass
        
    
    def infrastruc(self,path,pflag):
        g.tprinter('Running infrastruc',pflag)
        if os.path.exists(path) is not True:
            g.printer('Creating ana_res path',pflag)
            
            os.mkdir(path)
        else:
            g.printer('Ana_res path exists',pflag)
        g.printer('ana_res_path: \n'+str(path),pflag)
#         g.printer(path,pflag)
        self.ana_res_path = path 
    
    def ana_file_check(self,forceflag,pflag):
        g.tprinter('Running ana_file_check',pflag)
        self.ana_file_name = os.path.join(self.ana_res_path,'ana_file.csv')
#         print self.ana_file_name
#         g.printer(self.ana_file_name,pflag)
        if os.path.isfile(self.ana_file_name) is True & forceflag == 0:
            g.printer('Found ana_file',pflag)
#             self.ana_file = c.csv_file_loader(self.ana_res_path,'ana_file.csv',pflag) 
        else:
            if forceflag == 1:
                g.printer('ana_file found but forceflag == 1',pflag)
            else:
                g.printer('No ana_file found',pflag)
            
            self.ana_file_creator(1,pflag)
    
    def header_set(self,header,pflag):
        g.tprinter('Running header_set',pflag)
        g.printer('Header: \n'+str(header),pflag)
        
        self.header=list(header)
#         print self.header
         
#         g.printer(self.header,pflag)
                
    def ana_file_creator(self,flag,pflag):
        g.tprinter('Running ana_file_creator',pflag)
#         header=[['time_stamp','meas_nr','daq_name','channel','t_delta','t_length','offset','offset_corr','noise','analysed','file_name','file_name_path']]
        g.printer(str(self.ana_res_path),pflag)
        g.printer(self.header,pflag)
        try:
            self.header
#             g.prinert(self.header,pflag)
            g.printer('header ok',pflag)
        except:
            g.printer('header not ok',pflag)
            sys.exit('script stop')
        
        
        c.csv_file_saver(self.ana_res_path,'ana_file.csv',self.header,flag,pflag)
              
    def ana_file_name_set(self,r_name,pflag):
        g.tprinter('Running ana_file_name',pflag)
        self.ana_file_name = r_name+'_ana_file.csv'
        
        g.printer('Name: '+str(self.ana_file_name),pflag)
        
        
    def ana_file_loader(self,pflag):
        g.tprinter('Running ana_file_loader',pflag)
        self.ana_file = c.csv_file_loader(self.ana_res_path,self.ana_file_name,pflag)
        
    def ana_file_saver(self,flag,pflag):
        g.tprinter('Running ana_file_saver',pflag)
        c.csv_file_saver(self.ana_res_path,self.ana_file_name,self.ana_file,flag,pflag)
           
    def ana_file_writer(self,dlist,pflag):
        g.tprinter('Running ana_file_writer',pflag)
        for i in dlist:
#             print i[0]
            if str(i[0]) in np.array(self.ana_file):
                g.printer(str(i[0])+' is in ana_file',pflag)
                pass
            else:
                g.printer(str(i[0])+' is not in ana_file',pflag)
                nline = [0]*len(self.ana_file[0])
                nline[l.find_val('file_name',self.ana_file[0],0)] = i[-1]
                nline[l.find_val('file_name_path',self.ana_file[0],0)] = i[-2]
                self.ana_file.append(nline)
#                 print nline
                
    def check_for_ana_file(self,ana_file_path,force_flag,pflag):
        g.tprinter('Running check_for_ana_file',pflag)
        self.ana_file_dir = os.path.join(ana_file_path,self.ana_file_name)
        
        if os.path.isfile(self.ana_file_dir) == True and force_flag == 0:
            g.printer('ana_file exists',pflag)  
            g.printer('Loading ana_file',pflag)
            try:
                self.ana_file=c.csv_file_loader(ana_file_path,self.ana_file_name,pflag)
            except:
                sys.exit('script stop')
        else:
            
            if force_flag == 1:
                g.printer('force_flag',pflag)
            else:
                g.printer('ana_file does not exist',pflag)
            
            g.printer('creating ana_file',pflag)
            self.ana_file = self.header
        
        g.tprinter('saving file',pflag)
        c.csv_file_saver(ana_file_path,self.ana_file_name,self.ana_file,1,pflag)
        
    def data_path_set(self,data_path,pflag):
        g.tprinter('Running data_path_set',pflag)  
        self.data_path = data_path 
        
        
    def data_list_creator(self,ident,pflag):
        g.tprinter('Running data_list_creator',pflag)
        

        f = os.listdir(self.data_path)
      
        k = []
        
        for i in f:
            g.printer(str(i),pflag)
            if i.endswith(str(ident)):
#                 k.append([os.path.join(self.path,i),i])
                k.append([os.path.join(self.data_path,i),i])
#                 k.append(i)
#             print k
        
        g.printer('Length data_list: '+str(len(k)),pflag)
        
        self.data_list=k        
        
                
    def ana_file_updater(self,pflag):
        g.tprinter('Running list_updater',pflag)
        
        for i in self.data_list:
            if str(i[0]) in np.array(self.ana_file):
                g.printer(str(i[-1])+' is in ana_file',pflag)
                
            else:
                
                nline = [0]*len(self.ana_file[0])
                nline[l.find_val('file_name',self.ana_file[0],0)] = i[-1]
                nline[l.find_val('file_name_path',self.ana_file[0],0)] = i[-2]
                
                self.ana_file.append(nline)
                g.printer(str(i[-1])+' was added to ana_file',pflag)
                
            
            
                    
    def file_check(self,path,fname,pflag):
        g.tprinter('Running file_check',pflag)
        g.printer('Path name: \n'+str(path),pflag)
        g.printer('File name: \n'+str(fname),pflag)
        
        try:
            open(os.path.join(path,fname))
            g.printer('file exists',pflag)
            out =True
        except:
            g.printer('file does NOT exsist',pflag)
            out = False
        
        return out
            
            
    def file_setup(self,path,fname,pflag):
        g.tprinter('Running file_setup',pflag)
        g.printer('file name: '+str(fname),pflag)
        
        if self.file_check(path,fname,pflag) == True:
            print 'file exists'
#             print 'peng'
            self.data_sets=c.csv_file_loader(path,fname,pflag)
            print fname
            print 'file loaded'
            print self.data_sets
        else:
            try:
#                 print 'puff'
                self.data_sets = self.header
            except:
#                 print 'click'
                self.data_sets = []
                
        c.csv_file_saver(path, fname, self.data_sets, 1, pflag)
        return self.data_sets
    

        
        
        
        
        
        
                        
    def file_saver(self,path,fname,ilist,pflag):
        g.tprinter('Running fiel_saver',pflag)
        
        g.tprinter('saving data',pflag)
        c.csv_file_saver(path, fname,ilist, 1, pflag)
    
    
    def int_data_cond(self,line,param,limit,c,pflag):
        g.tprinter('Running int_data_cond',pflag)
        g.printer('param: '+str(param),pflag)
        g.printer('limit:'+str(limit),pflag)
        
        print line[l.find_val('sig 50 pt',self.header[0],0)]
        try:
            if line[l.find_val(str(param),self.header[0],0)] >= limit:
                self.add_to_int_data_sets(line, pflag)
            else:
                pass
        except:
            g.printer(str(param)+' not in header',pflag)
            
            
        
    def add_to_int_data_sets(self,line,pflag):
        g.tprinter('Running add_to_int_data_sets',pflag)
        
        if line not in self.int_data_sets:
            self.int_data_sets.append(line)
                   
           
