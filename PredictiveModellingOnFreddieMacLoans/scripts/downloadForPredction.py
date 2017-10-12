import json
import datetime
import time

import downloaderfunctions
import cleaningandmergefunctions
import glob
import logging
import os
import luigi
import pandas as pd


NOW = datetime.datetime.now()
TODAYSDATE = str(NOW.day).zfill(2)+str(NOW.month).zfill(2)+str(NOW.year)
TODAYSDATESTRING = str(NOW.day).zfill(2)+"/"+str(NOW.month).zfill(2)+"/"+str(NOW.year)
#MAINPATH="C:/Users/visha/Desktop/MSIS/Advanced Data Science/Assignments/MIDTERM/Part2"
LOGPATH = os.environ['LOGPATH']+"/"

LOGFILENAME = LOGPATH+"/"+TODAYSDATE+str(NOW.hour).zfill(2)+str(NOW.minute).zfill(2)+str(NOW.second).zfill(2)+".log"
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',filename=LOGFILENAME,datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)



DOWNPATH=os.environ['TEMPPATH']
BASEURL="https://freddiemac.embs.com/FLoan/Data/"
AUTHURL = "https://freddiemac.embs.com/FLoan/secure/auth.php"
DOWNLOADURL = "https://freddiemac.embs.com/FLoan/Data/download.php"
DATAPATH=os.environ['DATAPATH']
CONFIGFILEPATH = os.environ['CONFIGPATH']+"/"+"config.json"


   
def loadConfig():
    fil = open(CONFIGFILEPATH,'r')
    conf = json.load(fil)
    fil.close()
    return conf


class CombinerTask(luigi.Task):
   def requires(self):
       tasks = []
       for month in range(1, 5):
         tasks.append(CompanyCount(str(month)))
       return tasks
   def run(self):
       for x in self.output():
           print(x.path)

#class RegressionTask():
    
#class ClassificationTask():

class DownloadAndCleanTask(luigi.Task):
    #filename=luigi.Parameter(default='')
    filename=luigi.Parameter(default='Q22005')
    outputfilename="X"
    def run(self):
        
        self.outputfilename="downfiles_"+self.filename+".txt"
        print(self.outputfilename)
        loadConfig()
        config_file=loadConfig()
        username=config_file['username']
        password=config_file['password']
        
        opcookie=downloaderfunctions.getSession(AUTHURL,username,password)
        
        
        searchList=[]
        searchList.append(self.filename)
        
        if opcookie['auth'] != 'error':
            print(opcookie)
            downlinksdict=downloaderfunctions.getDownloadLinksFrom('historical',searchList,DOWNLOADURL,username,password,opcookie)
            if len(downlinksdict.keys())==0:
                print("User ID might have been disabled")
                logging.error("User ID might have been disabled")
                exit()
            else:
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Download Start Time : "+st)
                for key, value in downlinksdict.items():
                    #downlist=downloaderfunctions.downloadExtractRemove(BASEURL+value,DOWNPATH,key,opcookie)
                    downlist=["historical_data1_Q22005.txt","historical_data1_time_Q22005.txt"]
                    print(self.output().path)
                    with open(self.output().path,"w") as f:
                        ct=0
                        for downfilename in downlist:
                            #self.filelist.append(DOWNPATH+"/"+downfilename)
                            if 'time' in downfilename:
                                temp=pd.DataFrame()
                                temp=cleaningandmergefunctions.cleanOrigPrediction(DOWNPATH+"/"+downfilename)
                                temp.to_csv(DOWNPATH+"/"+"clean"+"_"+downfilename)
                                os.remove(DOWNPATH+"/"+downfilename)
                            else:
                                temp=pd.DataFrame()
                                temp=cleaningandmergefunctions.cleanPerfClassification(DOWNPATH+"/"+downfilename)
                                temp.to_csv(DOWNPATH+"/"+"clean"+"_"+downfilename)
                                os.remove(DOWNPATH+"/"+downfilename)
                            f.write(DOWNPATH+"/"+"clean"+"_"+downfilename)
                            ct+=1
                            if ct < len(downlist):
                                f.write(",")
                
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Download End Time : "+st)

        else:
            print("Cannot access account")
            logging.error("Cannot access account")
            exit()
        
    def output(self):
        return luigi.LocalTarget(DOWNPATH+"/"+self.outputfilename)                           
    
class CompanyCount(luigi.Task):
    month = luigi.Parameter(default='0')
    def run(self):
        print("task")
        with open(self.output().path,"w") as fil:
            fil.write("month="+str(self.month))
    def output(self):
        return luigi.LocalTarget("C:/Users/visha/Desktop/MSIS/Advanced Data Science/Assignments/TESTLUIGI/"+self.month+"fil_month.csv")                           
                           
                           
