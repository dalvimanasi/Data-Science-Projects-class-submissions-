import json
import datetime
import time

import downloaderfunctions
import cleaningandmergefunctions
import glob
import logging
import os
import sys


NOW = datetime.datetime.now()
TODAYSDATE = str(NOW.day).zfill(2)+str(NOW.month).zfill(2)+str(NOW.year)
TODAYSDATESTRING = str(NOW.day).zfill(2)+"/"+str(NOW.month).zfill(2)+"/"+str(NOW.year)

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

def main():

    args = sys.argv[1:]
    
    if len(args) != 4:
        print("Not enough arguments")
        exit(0)
        
    username=str(args[0])
    password=str(args[1])
    startyear=int(args[2])
    endyear=int(args[3])
    
    if startyear > endyear:
        logging.error("Start year has to be lesser than end year")
        exit()
    
    #config_file=loadConfig()
    #username=config_file['username']
    #password=config_file['password']
    
    if (username=="") | (password == ""):
        logging.error("Username or password not present in config file.")
        exit()
    
    opcookie=downloaderfunctions.getSession(AUTHURL,username,password)
    searchList=list(range(startyear,endyear+1))
    origcombinefilelist=[]
    perfcombinefilelist=[]
    
    '''
    for filename in glob.iglob('C:/Users/visha/Desktop/MSIS/Advanced Data Science/Assignments/MIDTERM/FM Dataset/Samples/Downloads/*.txt', recursive=True):
        if 'orig' in filename:
            origcombinefilelist.append(filename)
        elif 'svcg' in filename:
            perfcombinefilelist.append(filename)
    if len(origcombinefilelist) > 0:
        cleaningandmergefunctions.cleanAndMergeOrig(DOWNPATH+"/originationsummary.csv",origcombinefilelist)
    if len(perfcombinefilelist) > 0:
        cleaningandmergefunctions.cleanAndMergePerf(DOWNPATH+"/performancesummary.csv",perfcombinefilelist)
    exit()
    '''
    
    
    if opcookie['auth'] != 'error':
        print(opcookie)
        downlinksdict=downloaderfunctions.getDownloadLinksFrom('sample',searchList,DOWNLOADURL,username,password,opcookie)
        if len(downlinksdict.keys())==0:
            print("User ID might have been disabled")
            logging.error("User ID might have been disabled")
            exit()
        else:
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
            print("Download Start Time : "+st)
            for key, value in downlinksdict.items():
                downlist=downloaderfunctions.downloadExtractRemove(BASEURL+value,DOWNPATH,key,opcookie)
                for downfilename in downlist:
                    if 'orig' in downfilename:
                        origcombinefilelist.append(DOWNPATH+"/"+downfilename)
                    elif 'svcg' in downfilename:
                        perfcombinefilelist.append(DOWNPATH+"/"+downfilename)
            
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
            print("Download End Time : "+st)
            print("Start Performance summarization : "+st)
            if len(origcombinefilelist) > 0:
                cleaningandmergefunctions.cleanAndMergeOrig(DATAPATH+"/originationsummary.csv",origcombinefilelist)
            if len(perfcombinefilelist) > 0:
                cleaningandmergefunctions.cleanAndMergePerf(DATAPATH+"/performancesummary.csv",perfcombinefilelist)
            downloaderfunctions.logout(AUTHURL,username,password,opcookie)
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
            print("End Performance summarization : "+st)
    else:
        print("Cannot access account")
        logging.error("Cannot access account")
        exit()
if __name__ == '__main__':
    main()