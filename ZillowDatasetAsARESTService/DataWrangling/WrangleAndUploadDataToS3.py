import datetime
import luigi
import logging
import boto3
import json
from botocore.client import Config
from pathlib import Path
import pandas as pd
import os


NOW = datetime.datetime.now()
TODAYSDATE = str(NOW.day).zfill(2)+str(NOW.month).zfill(2)+str(NOW.year)
TODAYSDATESTRING = str(NOW.day).zfill(2)+"/"+str(NOW.month).zfill(2)+"/"+str(NOW.year)

MAINPATH = os.environ['MAINPATH']+"/"
OUTPUTPATH = os.environ['OUTPUTPATH']+"/"
INPUTFILEPATH = os.environ['DATAPATH']+"/"+"properties_2016.csv"
TEMPFILEPATH = OUTPUTPATH+"/"+"TEMP_WrangleFirst.csv"
CLEANFILEPATH = OUTPUTPATH+"/"+"zillowdata.csv"
CONFIGFILEPATH = os.environ['CONFIGPATH']+"/"+"config.json"
TEMPCONFIGFILEPATH = OUTPUTPATH+"/"+"TEMP_"+TODAYSDATE+"_config.json"

LOGPATH = os.environ['LOGPATH']+"/"

LOGFILENAME = LOGPATH+"/"+TODAYSDATE+str(NOW.hour).zfill(2)+str(NOW.minute).zfill(2)+str(NOW.second).zfill(2)+".log"
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',filename=LOGFILENAME,datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)


def validateConfigFile(config_file):
    try:
        if str(config_file['team']) == "":
            logging.error("team is not defined in the config file")
            return False
        if config_file['AWSAccess'] == "":
            logging.error("AWSAccess is not defined in the config file")
            return False
        if config_file['AWSSecret'] == "":
            logging.error("AWSSecret is not defined in the config file")
            return False
        if config_file['notificationEmail'] == "":
            logging.error("notificationEmail is not defined in the config file")
            return False
        return True
    except:
        logging.error("Config File not complete or unparseable. Check if all keys (team,AWSAccess,AWSSecret,notificationEmail) exist.")

def readConfig(path):
    fil = open(path,'r')
    conf = json.load(fil)
    fil.close()
    return conf
def getBucketName(conf):
    BUCKET_NAME = "Team" + str(conf['TEAM']) + "_" +"ZillowData"
    return BUCKET_NAME

class UploadCleanFileToS3(luigi.Task):
    uploadRawDataToS3 = "TEMP_uploadRawDataSToS3.txt"
    def requires(self):
        yield WrangleData()
        yield ValidateConfigFile()
    def run(self):
        conf = {}
        tempConfPath = ""
        dataPath = ""
        
        for p in self.input():
            if "config" in p.path:
                tempConfPath = p.path
            else:
                dataPath = p.path
        
        if tempConfPath == "":
            logging.error("Temporary Config file not written")
            raise CustomDataIngestionException("Temporary Config file not written")
        if dataPath == "":
            logging.error("Clean Data Path could not be determined")
            raise CustomDataIngestionException("Clean Data Path could not be determined")
        
        conf = readConfig(tempConfPath)       
        BUCKET_NAME = getBucketName(conf) 
        S3 = boto3.resource('s3',
            aws_access_key_id= conf['AWSACCESS'],
            aws_secret_access_key=conf['AWSSECRET'],
            config=Config(signature_version='s3v4')
            )
        try:
            S3.create_bucket(Bucket=BUCKET_NAME)
        except:
            logging.error("Error while creating / accessing new Bucket")
            raise
        logging.info("Bucket "+BUCKET_NAME+"created / already exists")

        logging.info("Reading clean zillow data file from local "+dataPath)

        data = open(dataPath,'rb')
        keyName = dataPath.split("/")[-1]
        logging.info("Uploading clean zillow data file "+keyName+" to S3 bucket " + BUCKET_NAME+ "...")
        S3.Bucket(BUCKET_NAME).put_object(Key=keyName, Body=data)
        data.close()
        
        logging.info("File "+keyName+" Uploaded successfully to S3 bucket " + BUCKET_NAME)
        
        f = self.output().open('w')
        f.write("SUCCESS")
        f.close()
    def output(self):
        return luigi.LocalTarget(OUTPUTPATH+"/"+self.uploadRawDataToS3)

class WrangleData(luigi.Task):
    wranglefilename = CLEANFILEPATH
    def requires(self):
       return RemoveUnwantedColumns()
    def run(self):
        zillow_raw = pd.read_csv(self.input().path)
        
        #Wrangle the file
        latlong_df = pd.DataFrame({'parcelid':zillow_raw.parcelid,'latitude':zillow_raw.latitude.apply(lambda x: x/1000000),'longitude':zillow_raw.longitude.apply(lambda x: x/1000000)})
        zillow_raw=zillow_raw.drop(['latitude','longitude'],axis=1)
        zillow_raw=zillow_raw.merge(latlong_df, left_on='parcelid', right_on='parcelid')
        
        #Removing columns for which longitude or latitude data doesn't exist
        zillow_raw=zillow_raw[zillow_raw.latitude.notnull() & zillow_raw.longitude.notnull()]
       
        zillow_raw.regionidzip[(zillow_raw.regionidzip >= 99999)|(zillow_raw.regionidzip < 99999)]=96987
        
        #Cleaning strategy1
        clean_means=zillow_raw[zillow_raw.bathroomcnt.notnull()][['bathroomcnt','propertylandusetypeid','fips']].groupby(['propertylandusetypeid','fips']).mean()
    
        clean_means_bed=zillow_raw[zillow_raw.bedroomcnt.notnull()][['bedroomcnt','propertylandusetypeid','fips']].groupby(['propertylandusetypeid','fips']).mean()
        
        clean_means_room=zillow_raw[zillow_raw.roomcnt.notnull()][['roomcnt','propertylandusetypeid','fips']].groupby(['propertylandusetypeid','fips']).mean()
       
        heatgrp=zillow_raw[zillow_raw.heatingorsystemtypeid.notnull()][['heatingorsystemtypeid','propertylandusetypeid','fips']].groupby(['propertylandusetypeid','fips'])
        heatgrp = heatgrp.heatingorsystemtypeid.value_counts()
        
        buildinggrp=zillow_raw[zillow_raw.buildingqualitytypeid.notnull()][['buildingqualitytypeid','propertylandusetypeid','fips']].groupby(['propertylandusetypeid','fips'])
        buildinggrp = buildinggrp.buildingqualitytypeid.value_counts()
        
        dic={}
        dicBed={}
        dicRoom={}
        
        #print(zillow_raw.bathroomcnt.isnull().sum())
        #print(zillow_raw.bedroomcnt.isnull().sum())
        #print(zillow_raw.roomcnt.isnull().sum())
        #print(zillow_raw.heatingorsystemtypeid.isnull().sum())
        #print(zillow_raw.buildingqualitytypeid.isnull().sum())
        
        logging.info("Grouping values by propertydesctypeid and fips to derive an average of the property in that area.")
        
        for propid,fip in clean_means.index:
            dic[propid,fip] = round(clean_means.loc[propid,fip]['bathroomcnt']*2)/2
        for propid,fip in clean_means_bed.index:
            dicBed[propid,fip] = round(clean_means_bed.loc[propid,fip]['bedroomcnt']*2)/2
        for propid,fip in clean_means_room.index:
            dicRoom[propid,fip] = round(clean_means_room.loc[propid,fip]['roomcnt']*2)/2
        logging.info("Replacing missing bathroomcnt,bedroomcnt,roomcnt,heatingorsystemtypeid,buildingqualitytypeid with the average for these type of buildings in that area.")
        for propid,fip in dic.keys():
            #cleantest['bathroomcnt'] = np.where(((cleantest['bathroomcnt']==None) & (cleantest['propertylandusetypeid']==key)),dict[str(key)])
            #frames.append(cleantest.loc[((cleantest['propertylandusetypeid']==propid) & (cleantest['fips']==fip))][['bathroomcnt','roomcnt','bedroomcnt']].fillna(value=dic[propid,fip]))
            #cleantest[((cleantest['propertylandusetypeid']==propid) & (cleantest['fips']==fip))]['bathroomcnt'].replace(value=dic[propid,fip],inplace=True)
            zillow_raw.bathroomcnt[((zillow_raw['propertylandusetypeid']==propid) & (zillow_raw['fips']==fip) & (zillow_raw['bathroomcnt'].isnull()))] = dic[propid,fip]
            zillow_raw.bedroomcnt[((zillow_raw['propertylandusetypeid']==propid) & (zillow_raw['fips']==fip) & (zillow_raw['bedroomcnt'].isnull()))] = dicBed[propid,fip]
            zillow_raw.roomcnt[((zillow_raw['propertylandusetypeid']==propid) & (zillow_raw['fips']==fip) & (zillow_raw['roomcnt'].isnull()))] = dicRoom[propid,fip]
            try:
                zillow_raw.heatingorsystemtypeid[((zillow_raw['propertylandusetypeid']==propid) & (zillow_raw['fips']==fip) & (zillow_raw['heatingorsystemtypeid'].isnull()))] = heatgrp[propid,fip].index[0]
            except KeyError:
                logging.warn("Heat\t"+str(propid)+"\t"+str(fip) + " could not be determined")
            try:
                zillow_raw.buildingqualitytypeid[((zillow_raw['propertylandusetypeid']==propid) & (zillow_raw['fips']==fip) & (zillow_raw['buildingqualitytypeid'].isnull()))] = buildinggrp[propid,fip].index[0]
            except KeyError:
                logging.warn("BLDG\t"+str(propid)+"\t"+str(fip)+" could not be determined")
    
        
        logging.info("Filling missing values as 0 for \n heatingorsystemtypeid,buildingqualitytypeid,airconditioningtypeid,numberofstories,fireplacecnt,poolcnt,unitcnt")
        zillow_raw.heatingorsystemtypeid=zillow_raw.heatingorsystemtypeid.fillna(value=0)
        zillow_raw.buildingqualitytypeid=zillow_raw.buildingqualitytypeid.fillna(value=0)
        zillow_raw.airconditioningtypeid=zillow_raw.airconditioningtypeid.fillna(value=0)
        
        zillow_raw.bathroomcnt=zillow_raw.bathroomcnt.fillna(value=0)
        zillow_raw.bedroomcnt=zillow_raw.bedroomcnt.fillna(value=0)
        zillow_raw.roomcnt=zillow_raw.roomcnt.fillna(value=0)
        
        zillow_raw.unitcnt=zillow_raw.unitcnt.fillna(value=0)
        
		#zillow_raw=zillow_raw.fillna(value='NULL')
		
        #print(zillow_raw.bathroomcnt.isnull().sum())
        #print(zillow_raw.bedroomcnt.isnull().sum())
        #print(zillow_raw.roomcnt.isnull().sum())
        #print(zillow_raw.heatingorsystemtypeid.isnull().sum())
        #print(zillow_raw.buildingqualitytypeid.isnull().sum())
        
        

        #End of cleaning strategy1
        logging.info("Wrangling completed... Saving final file to : "+str(self.output().path))
        
        zillow_raw.to_csv(self.output().path,index=False)
        
    def output(self):
        return luigi.LocalTarget(self.wranglefilename)

class RemoveUnwantedColumns(luigi.Task):
    wranglefilename = TEMPFILEPATH
    def requires(self):
        return CheckIfInputExists()
    def run(self):
        logging.info("Removing Unwanted columns")
        zillow_raw = pd.read_csv(self.input().path,low_memory=False)
        zillow_raw.fireplaceflag.replace(to_replace=True,value=1,inplace=True)
        zillow_raw.fireplacecnt[((zillow_raw['fireplaceflag']==1) & (zillow_raw['fireplacecnt'].isnull()))]=1
        COLUMN_LIST_TO_KEEP=['parcelid','airconditioningtypeid','bathroomcnt','bedroomcnt','buildingqualitytypeid','calculatedfinishedsquarefeet','fips','fireplacecnt','garagecarcnt','garagetotalsqft','heatingorsystemtypeid','latitude','longitude','lotsizesquarefeet','poolcnt','propertylandusetypeid','rawcensustractandblock','regionidcity','regionidneighborhood','regionidzip','roomcnt','unitcnt','yearbuilt','numberofstories','structuretaxvaluedollarcnt','taxvaluedollarcnt','assessmentyear','landtaxvaluedollarcnt','taxamount']
        logging.info("Keeping columns \nparcelid','airconditioningtypeid','bathroomcnt','bedroomcnt','buildingqualitytypeid','calculatedfinishedsquarefeet','fips','fireplacecnt','garagecarcnt','garagetotalsqft','heatingorsystemtypeid','latitude','longitude','lotsizesquarefeet','poolcnt','propertylandusetypeid','rawcensustractandblock','regionidcity','regionidneighborhood','regionidzip','roomcnt','unitcnt','yearbuilt','numberofstories','structuretaxvaluedollarcnt','taxvaluedollarcnt','assessmentyear','landtaxvaluedollarcnt','taxamount")
        zillow_raw_reduced_columns = zillow_raw[COLUMN_LIST_TO_KEEP] 
        zillow_raw_reduced_columns.to_csv(self.output().path,index=False)
        
    def output(self):
        return luigi.LocalTarget(self.wranglefilename)

class ValidateConfigFile(luigi.Task):
    configFilePath = TEMPCONFIGFILEPATH
    def run(self):
        logging.info("Reading from Config File "+CONFIGFILEPATH)
        GLOBALPARAMS = {}
        try:
            config_file_raw = open(CONFIGFILEPATH)
            config_file = json.load(config_file_raw)
            if not validateConfigFile(config_file):
                raise
            #Set parameters derived from file
            GLOBALPARAMS['AWSACCESS'] = config_file['AWSAccess']
            GLOBALPARAMS['AWSSECRET'] = config_file['AWSSecret']
            GLOBALPARAMS['TEAM'] = config_file['team']
            GLOBALPARAMS['NOTIFICATIONEMAIL'] = config_file['notificationEmail']

        except:
            logging.error("Error opening /parsing the config file "+CONFIGFILEPATH + "\nCheck if the file" +CONFIGFILEPATH+ " is well formed")
            config_file_raw.close()
            raise CustomDataIngestionException("Error opening /parsing the config file "+CONFIGFILEPATH + "\nCheck if the file" +CONFIGFILEPATH+ " is well formed")
        finally:
            config_file_raw.close()
        config_file_raw.close()
        logging.info("Config File "+CONFIGFILEPATH+" valid.")
        
        with self.output().open("w") as fp:
            json.dump(GLOBALPARAMS, fp)
        
    def output(self):
        return luigi.LocalTarget(self.configFilePath)



class CheckIfInputExists(luigi.Task):
    inputFilePath = "DUMMY"
    def run(self):
        #Check if input file exists.
        logging.info("Checking for Input Data File at : "+INPUTFILEPATH)
        checkFile = Path(INPUTFILEPATH)
        if not checkFile.is_file():
            raise CustomDataIngestionException("INPUT file not found at "+self.inputFilePath)
        else:
            self.inputFilePath = INPUTFILEPATH
        logging.info("Config file found at : "+INPUTFILEPATH)
    def output(self):
        return luigi.LocalTarget(self.inputFilePath)
        
class CustomDataIngestionException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)