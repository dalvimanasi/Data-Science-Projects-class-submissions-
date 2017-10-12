import json
import datetime
import time

import downloaderfunctions
import cleaningandmergefunctions
import logging
import os
import sys
import pandas as pd
from itertools import chain, islice
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.utils import *
from math import sqrt




NOW = datetime.datetime.now()
TODAYSDATE = str(NOW.day).zfill(2)+str(NOW.month).zfill(2)+str(NOW.year)
TODAYSDATESTRING = str(NOW.day).zfill(2)+"/"+str(NOW.month).zfill(2)+"/"+str(NOW.year)
#MAINPATH="C:/Users/Manasi/Desktop/ads/midterm/SCRIPTS"

LOGPATH = os.environ['LOGPATH']+"/"

LOGFILENAME = LOGPATH+"/"+TODAYSDATE+str(NOW.hour).zfill(2)+str(NOW.minute).zfill(2)+str(NOW.second).zfill(2)+".log"
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',filename=LOGFILENAME,datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)


DOWNPATH=os.environ['TEMPPATH']
BASEURL="https://freddiemac.embs.com/FLoan/Data/"
AUTHURL = "https://freddiemac.embs.com/FLoan/secure/auth.php"
DOWNLOADURL = "https://freddiemac.embs.com/FLoan/Data/download.php"
DATAPATH=os.environ['DATAPATH']
CONFIGFILEPATH = os.environ['CONFIGPATH']+"/"+"config.json"

FINALCSVPATH=DATAPATH+"/ClassificationMetrics.csv"
FINALCSVPREDICTION=DATAPATH+"/RegressionMetrics.csv"
       
def dummyvar(df):
    dumvar=df
    dumvar.select_dtypes(include=['object']).copy()
    #dumvar=pd.get_dummies(dumvar, columns=["PPM_FLAG"], prefix=["ppm"])
    lb_make = LabelEncoder()
    dumvar["PPM_FLAG_CODE"] = lb_make.fit_transform(dumvar["PPM_FLAG"])
    dumvar["LOAN_PURPOSE_CODE"] = lb_make.fit_transform(dumvar["LOAN_PURPOSE"])
    dumvar["OCCUPANCY_STATS_CODE"] = lb_make.fit_transform(dumvar["OCCUPANCY_STATS"])
    dumvar["PROP_TYPE_CODE"] = lb_make.fit_transform(dumvar["PROP_TYPE"])
    dumvar["FIRST_HOME_BUYER_FLAG_CODE"] = lb_make.fit_transform(dumvar["FIRST_HOME_BUYER_FLAG"])
    dumvar["PROP_STATE_CODE"] = lb_make.fit_transform(dumvar["PROP_STATE"])
    dumvar["CHANNEL_CODE"] = lb_make.fit_transform(dumvar["CHANNEL"])
    dumvar["SELLER_NAME_CODE"] = lb_make.fit_transform(dumvar["SELLER_NAME"])
    dumvar["SERVICE_NAME_CODE"] = lb_make.fit_transform(dumvar["SERVICE_NAME"])
    return dumvar
def mean_absolute_percentage_error(y_true, rf_predict): 
    return np.mean(np.abs((y_true - rf_predict) / y_true)) * 100

def prediction(trainpath,testpath,trainquarter,testquarter):
    #perform regression
    print(trainpath+"\t"+testpath+"\t"+trainquarter+"\t"+testquarter)
    Train_DF = pd.read_csv(trainpath,index_col=None)
    Test_DF=pd.read_csv(testpath,index_col=None)
    
    a= dummyvar(Train_DF)
    b= dummyvar(Test_DF)
    
    a1 =a.select_dtypes(include=['number'])
    b1 =b.select_dtypes(include=['number'])
    
    a1=a1[['CREDIT_SCORE','OG_UPB','OG_DTI','CHANNEL_CODE','OG_LOANTERM','OG_LTV','MI_PERCENT','PPM_FLAG_CODE','NUM_BORROWERS','OG_CLTV','NUM_UNITS','PROP_STATE_CODE','FIRST_HOME_BUYER_FLAG_CODE','PROP_TYPE_CODE','OCCUPANCY_STATS_CODE','LOAN_PURPOSE_CODE','OG_INTERESTRATE']]
    b1=b1[['CREDIT_SCORE','OG_UPB','OG_DTI','CHANNEL_CODE','OG_LOANTERM','OG_LTV','MI_PERCENT','PPM_FLAG_CODE','NUM_BORROWERS','OG_CLTV','NUM_UNITS','PROP_STATE_CODE','FIRST_HOME_BUYER_FLAG_CODE','PROP_TYPE_CODE','OCCUPANCY_STATS_CODE','LOAN_PURPOSE_CODE','OG_INTERESTRATE']]
    
    X_train=a1.drop('OG_INTERESTRATE',axis=1)
    Y_train=a1.OG_INTERESTRATE
    X_test=b1.drop('OG_INTERESTRATE',axis=1)
    Y_test=b1.OG_INTERESTRATE
    
    regressor = RandomForestRegressor(n_estimators=100,n_jobs=10)
    regressor.fit(X_train, Y_train)
    
    rf_predict=regressor.predict(X_test)
    
    rf_r2 = r2_score(Y_test, rf_predict)
    rf_mse = mean_squared_error(Y_test, rf_predict)
    rf_rmse = sqrt(mean_squared_error(Y_test, rf_predict))
    rf_mae = mean_absolute_error(Y_test, rf_predict)
    rf_mape = mean_absolute_percentage_error(Y_test, rf_predict)

    record = str(trainquarter)+","+str(testquarter)+","+str(rf_r2)+","+str(rf_mse)+","+str(rf_rmse)+","+str(rf_mae)+","+str(rf_mape)

    checkFile = Path(FINALCSVPREDICTION)
    if checkFile.is_file():
        with open(FINALCSVPREDICTION,"a") as fil:
            fil.write(record)
            fil.write("\n")
    else:
        with open(FINALCSVPREDICTION,"a") as fil:
            fil.write("TrainQuarter,TestQuarter,R-squared,MSE,RMSE,MAE,MAPE")
            fil.write("\n")
            fil.write(record)
            fil.write("\n") 

def classification(trainpath,testpath,trainquarter,testquarter):
    #perform regression
    print(trainpath+"\t"+testpath+"\t"+trainquarter+"\t"+testquarter)
    
    Train_DF = pd.read_csv(trainpath,index_col=None)
    traincols=['MONTHLY_REPORT_PERIOD','CUR_ACT_UPB','LOAN_AGE','MONTHS_LEGAL_MATURITY','CURR_INTERESTRATE','CURR_DEF_UPB']
    
    y_train=Train_DF['DELINQUENT']
    Train_DF=Train_DF[traincols]
    
    Test_DF=pd.read_csv(testpath,index_col=None)
    
    testcols=['MONTHLY_REPORT_PERIOD','CUR_ACT_UPB','CUR_LOAN_DELQ_STAT','LOAN_AGE','MONTHS_LEGAL_MATURITY','CURR_INTERESTRATE','CURR_DEF_UPB','DELINQUENT']
    testcols=['MONTHLY_REPORT_PERIOD','CUR_ACT_UPB','LOAN_AGE','MONTHS_LEGAL_MATURITY','CURR_INTERESTRATE','CURR_DEF_UPB']

    y_test=Test_DF['DELINQUENT']
    Test_DF=Test_DF[testcols]
    
    clf = RandomForestClassifier(n_estimators=20,verbose =1,min_samples_split=10)
    clf = clf.fit(Train_DF, y_train)

    pred = clf.predict(Test_DF) 
    
    cf=confusion_matrix(y_test, pred, labels=None, sample_weight=None)
    
    numDelinqProper=cf[1][1]
    numnondelinqimproper=cf[0][1]
    numRecordsInDataset=y_test.count()
    numPredictedDelinq=cf[1][0]+cf[1][1]
    numActualDelinq=y_test[y_test==1].count()
    
    record=str(testquarter)+","+str(numActualDelinq)+","+str(numPredictedDelinq)+","+str(numRecordsInDataset)+","+str(numDelinqProper)+","+str(numnondelinqimproper)
    checkFile = Path(FINALCSVPATH)
    if checkFile.is_file():
        with open(FINALCSVPATH,"a") as fil:
            fil.write(record)
            fil.write("\n")
    else:
        with open(FINALCSVPATH,"a") as fil:
            fil.write("Quarter,NumActualDelinquents,NumOfPredictedDelinquents,NumRecordsInDataset,NumDelinquentsProperlyClassified,NumNonDelinquentsImproperlyClassified")
            fil.write("\n")
            fil.write(record)
            fil.write("\n")
                           
def loadConfig():
    fil = open(CONFIGFILEPATH,'r')
    conf = json.load(fil)
    fil.close()
    return conf

def chunks(iterable, n):
    "chunks(ABCDE,2) => AB CD E"
    iterable = iter(iterable)
    while True:
        yield chain([next(iterable)], islice(iterable, n-1))


def performregressionandclassification(username,password,trainquarter):
    
    #config_file=loadConfig()
    #username=config_file['username']
    #password=config_file['password']
    
    #args = sys.argv[1:]
    
    #if len(args) != 3:
        #print("Not enough arguments")
        #exit(0)
        
    #username=str(args[0])
    #password=str(args[1])
    #trainquarter=str(args[2])
    print(username)
    print(password)
    print(trainquarter)
    trainlist=[]
    trainlist.append(trainquarter)
    testquarter=downloaderfunctions.downloadCurrentAndNext(trainlist)
    
    if (username=="") | (password == ""):
        logging.error("Username or password not present in config file.")
        exit()
    
    opcookie=downloaderfunctions.getSession(AUTHURL,username,password)

    searchList=[trainquarter,testquarter[0]]
    
    origtrainlist=[]
    origtestlist=[]
    perftrainlist=[]
    perftestlist=[]
    
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
            downlinksdict=downloaderfunctions.getDownloadLinksFrom('historical',searchList,DOWNLOADURL,username,password,opcookie)
            if len(downlinksdict.keys())==0:
                print("User ID might have been disabled")
                logging.error("User ID might have been disabled")
                exit()
            else:
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                logging.info("Download Start Time : "+st)
                print("Download Start Time : "+st)
                for key, value in downlinksdict.items():
                    downlist=downloaderfunctions.downloadExtractRemove(BASEURL+value,DOWNPATH,key,opcookie)
                    #downlist=['historical_data1_Q12005.txt','historical_data1_time_Q12005.txt']
                    for downfilename in downlist:
                        #self.filelist.append(DOWNPATH+"/"+downfilename)
                        oldfile=downfilename
                        newfile=""
                        if 'time' in downfilename:
                            l = 7000000
                            size=os.path.getsize(DOWNPATH+"/"+downfilename)
                            numchunks=round(size/400000000)
                            if numchunks>=2:
                                with open(DOWNPATH+"/"+downfilename) as bigfile:
                                    cnt=0
                                    for i, lines in enumerate(chunks(bigfile, l)):
                                        cnt+=1
                                        if cnt<=1:
                                            file_split = '{}.{}'.format(DOWNPATH+"/"+downfilename, i)
                                            with open(file_split, 'w') as f:
                                                f.writelines(lines)
                                newfile=downfilename+".0"
                            if newfile!="":
                                downfilename=newfile
                            temp=pd.DataFrame()
                            temp=cleaningandmergefunctions.cleanPerfClassification(DOWNPATH+"/"+downfilename)
                            temp.to_csv(DOWNPATH+"/"+"clean"+"_"+downfilename,index=False)
                            if trainquarter in downfilename:                 
                                perftrainlist.append(DOWNPATH+"/"+"clean"+"_"+downfilename)
                            elif testquarter[0] in downfilename:
                                perftestlist.append(DOWNPATH+"/"+"clean"+"_"+downfilename)
                            if newfile!="":
                                os.remove(DOWNPATH+"/"+oldfile)   
                            os.remove(DOWNPATH+"/"+downfilename)
                        else:
                            temp=pd.DataFrame()
                            temp=cleaningandmergefunctions.cleanOrigPrediction(DOWNPATH+"/"+downfilename)
                            temp.to_csv(DOWNPATH+"/"+"clean"+"_"+downfilename,index=False)
                            if trainquarter in downfilename:                 
                                origtrainlist.append(DOWNPATH+"/"+"clean"+"_"+downfilename)
                            elif testquarter[0] in downfilename:
                                origtestlist.append(DOWNPATH+"/"+"clean"+"_"+downfilename)
                            
                            os.remove(DOWNPATH+"/"+downfilename)

                
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Download End Time : "+st)
                logging.info("Download End Time : "+st)
                
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Prediction Starts: "+st)
                
                prediction(origtrainlist[0],origtestlist[0],trainquarter,testquarter[0])
                
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Prediction Ends: "+st)
                
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Classification Starts: "+st)
                
                classification(perftrainlist[0],perftestlist[0],trainquarter,testquarter[0])
                
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Classification Ends: "+st)
                
                os.remove(origtrainlist[0])
                os.remove(origtestlist[0])
                os.remove(perftrainlist[0])
                os.remove(perftestlist[0])
                

    else:
        print("Cannot access account")
        logging.error("Cannot access account")


def main():
    
    #config_file=loadConfig()
    #username=config_file['username']
    #password=config_file['password']
    
    args = sys.argv[1:]
    
    if len(args) != 3:
        print("Not enough arguments")
        exit(0)
        
    username=str(args[0])
    password=str(args[1])
    trainquarter=str(args[2])

    
    performregressionandclassification(username,password,trainquarter)

if __name__ == '__main__':
    main()