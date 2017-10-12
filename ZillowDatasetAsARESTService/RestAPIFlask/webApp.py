#from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
from flaskext.mysql import MySQL
import requests
import json


# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db = None
conn=None

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'zillowdb'
app.config['MYSQL_DATABASE_HOST'] = 'zillow.ccn3m9bbdf3i.us-east-1.rds.amazonaws.com'
mysql.init_app(app)
conn = mysql.connect()

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8080))
'''
@app.route('/')
def home():
    return render_template('index.html')
'''

def customError(code,errString):
    output = {"Status":code,"Message":errString,"results":[]}
    return jsonify(output)

@app.route('/searchclosestgeo', methods=['GET'])
def search_closest():

    try:
        lat = float(request.args.get('latitude'))
        long = float(request.args.get('longitude'))
    except:
        return customError(520,"request parameters latitude and longitude expected")
    if ((lat==None) | (long==None)):
        return customError(520,"request parameters latitude and longitude expected")
    
    if ((lat=="") | (long=="")):
        return customError(520,"request parameters latitude and longitude expected")

    cursor =conn.cursor()
    query="select parcelid,latitude,longitude,st_distance(point("+str(lat)+","+str(long)+"),point(latitude,longitude)) as distance_plane,bathroomcnt,bedroomcnt,calculatedfinishedsquarefeet from zillowdata having distance_plane < 2 ORDER BY distance_plane limit 10"
    cursor.execute(query)
    
    status=200
    errmessage="Success"
    retlist = []
    
    if cursor.rowcount==0:
        status=204
        errmessage = "No records close to the entered location"
    else:
        data = cursor.fetchall()
        retlist = []
        for row in data:
            latlong=str(row[2])+","+str(row[1])
            url = "http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?f=pjson&featureTypes=&location="+latlong
            response = requests.get(url)
            resp=json.loads(response.text)
            retlist.append({"parcelid":row[0],"Latitude":float(row[1]),"Longitude":float(row[2]),"Distance in meters":round(float(row[3])*111195,3),"Bathrooms":row[4],"Bedrooms":row[5],"Total Area":row[6],"Zipcode":resp['address']['Postal'],"City":resp['address']['City'],"Neighborhood":resp['address']['Neighborhood'],"County":resp['address']['Subregion'],"State":resp['address']['Region']})
        
                #retlist.append({"parcelid":row[0],"Latitude":float(row[1]),"Longitude":float(row[2]),"Distance in meters":float(row[3]),"Bathrooms":row[4],"Bedrooms":row[5],"Total Area":row[6]})
            
    #ret = {retlist}
    output = {"Status":status,"Message":errmessage,"results":retlist}
    #conn.close()
    return jsonify(output)

def addQueryParams(querystr,param):
    if querystr=="":
        querystr+=param
    else:
        querystr+=","+param
    return querystr

def addQuerycondition(querystr,field,param):
    if querystr=="":
        querystr+=field+"='"+param+"'"
    else:
        querystr+=" AND "+field+"='"+param+"'"
    return querystr

@app.route('/search', methods=['GET'])
def put_visitor():

    parcelid = request.args.get('parcelid')
    zipcode = request.args.get('zipcode')
    bathroom = request.args.get('bathroom')
    totalarea = request.args.get('totalarea')
    bedroom = request.args.get('bedroom')
    yearbuilt = request.args.get('yearbuilt')
    pool = request.args.get('pool')
    heating = request.args.get('heating')
    storeys = request.args.get('storeys')
    propertytype = request.args.get('propertytype')
    aircondition = request.args.get('aircondition')
    start = request.args.get('start')

    queryconditions=""

    if parcelid!=None:
        if parcelid!="":
            #queryParams=addQueryParams(queryParams,"regionidzipcode",zipcode)
            queryconditions=addQuerycondition(queryconditions,"parcelid",str(parcelid))
    
    if zipcode!=None:
        if zipcode!="":
            #queryParams=addQueryParams(queryParams,"regionidzipcode",zipcode)
            queryconditions=addQuerycondition(queryconditions,"regionidzip",str(zipcode))
    
    if bathroom!=None:
        if bathroom!="":
            queryconditions=addQuerycondition(queryconditions,"bathroomcnt",str(bathroom))
    
    if totalarea!=None:
        if totalarea!="":
            queryconditions=addQuerycondition(queryconditions,"calculatedfinishedsquarefeet",str(totalarea))
    
    if bedroom!=None:
        if bedroom!="":
            queryconditions=addQuerycondition(queryconditions,"bedroomcnt",str(bedroom))
    
    if yearbuilt!=None:
        if yearbuilt!="":
            queryconditions=addQuerycondition(queryconditions,"yearbuilt",str(yearbuilt))
    
    if pool!=None:
        if pool!="":
            queryconditions=addQuerycondition(queryconditions,"poolcnt",str(pool))
            
    if heating!=None:
        if heating!="":
            queryconditions=addQuerycondition(queryconditions,"A.heatingorsystemtypeid",str(heating))
    if storeys!=None:
        if storeys!="":
            queryconditions=addQuerycondition(queryconditions,"numberofstories",str(storeys))
    if propertytype!=None:
        if propertytype!="":
            queryconditions=addQuerycondition(queryconditions,"A.propertylandusetypeid",str(propertytype))
    if aircondition!=None:
        if aircondition!="":
            queryconditions=addQuerycondition(queryconditions,"A.airconditioningtypeid",str(aircondition))
    
    

    
    if queryconditions=="":
        return customError(520,"At least One search parameter expected")
    
    cursor =conn.cursor()
    query = "select taxvaluedollarcnt as TotalTaxAssessed,taxamount as TotalTaxForAssessmentYear,assessmentyear as AssessmentYear,structuretaxvaluedollarcnt as TaxAssessedOnStructure,garagecarcnt as Garage,parcelid as ParcelID,latitude as Latitude,longitude as Longitude,fips as FIPS,buildingqualitytypeid as BuildingQuality,regionidzip as ZIP,bathroomcnt as Bathrooms,calculatedfinishedsquarefeet as LivingArea,bedroomcnt as Bedrooms,yearbuilt as YearBuilt,poolcnt as Pool,A.heatingorsystemtypeid as HeatingID,numberofstories as NumberOfStories,A.propertylandusetypeid as PropertyTypeID,A.airconditioningtypeid as AirConditioningID,B.AirConditioningDesc as AirConditioning,C.HeatingOrSystemDesc as HeatingSystem,D.PropertyLandUseDesc as PropertyType from zillowdata A inner join airconditiontype B on  A.airconditioningtypeid = B.AirConditioningTypeID inner join heatingsystemtypeid C on A.heatingorsystemtypeid = C.HeatingOrSystemTypeID inner join propertydescid D on A.propertylandusetypeid=D.PropertyLandUseTypeID where "
    query+= queryconditions
    query+= " limit 100"
    if start!=None:
        if start!="":
            query+= " OFFSET "+str(start)
    cursor.execute(query)
    
    status=200
    errmessage="Success"
    result = []
    
    if cursor.rowcount==0:
        status=204
        errmessage="No Records found matching this criteria" 
    else:
        columns = tuple( [d[0] for d in cursor.description] )
        for row in cursor:
          result.append(dict(zip(columns, row)))
    
    
    output = {"Status":status,"Message":errmessage,"results":result}
    
    return jsonify(output)

@app.route('/airconditiontype', methods=['GET'])
def airconditiontypeid():
    cursor =conn.cursor()
    airid=request.args.get('airid')
    if airid!=None:
        if airid!="":
            cursor.execute("select AirConditioningTypeID,AirConditioningDesc from airconditiontype where AirConditioningTypeID ='"+str(airid)+"'")
        else:
            return customError(501,"airtypeid has to be provided")
    else:
        cursor.execute("select AirConditioningTypeID,AirConditioningDesc from airconditiontype")
   
    status=200
    errmessage="Success"
    
    
    retlist = []
    if cursor.rowcount==0:
        status=204
        errmessage = "No records found"
    else:
        data = cursor.fetchall()
        retlist = []
        for row in data:
            print(row)
            retlist.append({"AirConditioningTypeID":row[0],"AirConditioningDesc":(row[1])})
    output = {"Status":status,"Message":errmessage,"results":retlist}

    return jsonify(output)


@app.route('/heatingsystemtype', methods=['GET'])
def heatingsystemtypeid():
    cursor =conn.cursor()
    heattype=request.args.get('heattype')
    if heattype!=None:
        if heattype!="":
            cursor.execute("select HeatingOrSystemTypeID,HeatingOrSystemDesc from heatingsystemtypeid where HeatingOrSystemTypeID ='"+str(heattype)+"'")
        else:
            return customError(501,"heating system id has to be provided")
    else:
        cursor.execute("select HeatingOrSystemTypeID,HeatingOrSystemDesc from heatingsystemtypeid")
   
    status=200
    errmessage="Success"
    
    
    retlist = []
    if cursor.rowcount==0:
        status=204
        errmessage = "No records found"
    else:
        data = cursor.fetchall()
        retlist = []
        for row in data:
            print(row)
            retlist.append({"HeatingOrSystemTypeID":row[0],"HeatingOrSystemDesc":(row[1])})
    output = {"Status":status,"Message":errmessage,"results":retlist}

    return jsonify(output)

@app.route('/propertydesc', methods=['GET'])
def propertydescid():
    cursor =conn.cursor()
    proptype=request.args.get('proptype')
    if proptype!=None:
        if proptype!="":
            cursor.execute("select PropertyLandUseTypeID,PropertyLandUseDesc from propertydescid where PropertyLandUseTypeID ='"+str(proptype)+"'")
        else:
            return customError(501,"property id has to be provided")
    else:
        cursor.execute("select PropertyLandUseTypeID,PropertyLandUseDesc from propertydescid")
   
    status=200
    errmessage="Success"
   
    retlist = []
    if cursor.rowcount==0:
        status=204
        errmessage = "No records found"
    else:
        data = cursor.fetchall()
        retlist = []
        for row in data:
            print(row)
            retlist.append({"PropertyLandUseTypeID":row[0],"PropertyLandUseDesc":(row[1])})
    output = {"Status":status,"Message":errmessage,"results":retlist}

    return jsonify(output)

## count of properties by year
@app.route('/propertybyyear', methods=['GET'])
def propertybyyear():
    cursor =conn.cursor()
    propyear=request.args.get('propyear')
    if propyear!=None:
        if propyear!="":
            cursor.execute("select count(parcelid) as numberofhomes,yearbuilt from zillowdata where yearbuilt='"+str(propyear)+"' group by yearbuilt")
        else:
           return customError(501,"yearbuilt has to be provided") 
    else:
        cursor.execute("select count(parcelid),yearbuilt from zillowdata group by yearbuilt")
        
    status=200
    errmessage="Success"
   
    retlist = []
    if cursor.rowcount==0:
        status=204
        errmessage = "No records found"
    else:
        data = cursor.fetchall()
        retlist = []
        for row in data:
            print(row)
            retlist.append({"numberofhomes":row[0],"yearbuilt":(row[1])})
    output = {"Status":status,"Message":errmessage,"results":retlist}
        
    return jsonify(output)

@app.route('/propertytax', methods=['GET'])
def propertytypetax():
    cursor =conn.cursor()
   
    cursor.execute("select z.propertylandusetypeid,min(z.taxvaluedollarcnt) as mintaxvalue,max(z.taxvaluedollarcnt) as maxtaxvalue,avg(z.taxvaluedollarcnt) as avgtaxvalue,p.PropertyLandUseDesc from zillowdata z inner join propertydescid p on z.propertylandusetypeid = p.PropertyLandUseTypeID group by z.propertylandusetypeid")    
    status=200
    errmessage="Success"
   
    retlist = []
    if cursor.rowcount==0:
        status=204
        errmessage = "No records found"
    else:
        data = cursor.fetchall()
        '''
        retlist = []
        for row in data:
            print(row)
            retlist.append({"propertylandusetypeid":row[0],"mintaxvalue":(row[1]),"maxtaxvalue":(row[2]),"avgtaxvalue":(row[3])})
        '''
        retlist=[]
        columns = tuple( [d[0] for d in cursor.description] )
        for row in data:
          retlist.append(dict(zip(columns, row)))
    output = {"Status":status,"Message":errmessage,"results":retlist}
        
    return jsonify(output)


@atexit.register
def shutdown():
    if conn:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

