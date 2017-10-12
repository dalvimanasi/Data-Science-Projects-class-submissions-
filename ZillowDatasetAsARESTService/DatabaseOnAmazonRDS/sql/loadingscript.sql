USE zillowdb;

drop table if exists zillowdata;

CREATE TABLE zillowdata (
    parcelid INT NOT NULL,
    airconditioningtypeid INT,
    bathroomcnt DOUBLE,
    bedroomcnt DOUBLE,
    buildingqualitytypeid INT,
    calculatedfinishedsquarefeet DOUBLE,
    fips INT,
    fireplacecnt INT,
    garagecarcnt DOUBLE DEFAULT NULL,
    garagetotalsqft DOUBLE,
    heatingorsystemtypeid INT,
    lotsizesquarefeet DOUBLE,
    poolcnt INT,
    propertylandusetypeid INT,
    rawcensustractandblock DOUBLE ,
    regionidcity INT,
    regionidcounty INT,
    regionidneighborhood INT,
    regionidzip INT,
    roomcnt DOUBLE,
    unitcnt INT,
    yearbuilt INT,
    numberofstories INT,
    structuretaxvaluedollarcnt DOUBLE,
    taxvaluedollarcnt DOUBLE,
    assessmentyear INT,
    landtaxvaluedollarcnt DOUBLE,
    taxamount DOUBLE,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL
);

LOAD DATA LOCAL INFILE '/src/assignment2/data/aa' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;

LOAD DATA LOCAL INFILE '/src/assignment2/data/ab' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;

LOAD DATA LOCAL INFILE '/src/assignment2/data/ac' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;

LOAD DATA LOCAL INFILE '/src/assignment2/data/ad' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;

LOAD DATA LOCAL INFILE '/src/assignment2/data/ae' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;

LOAD DATA LOCAL INFILE '/src/assignment2/data/af' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;

LOAD DATA LOCAL INFILE '/src/assignment2/data/ag' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;


LOAD DATA LOCAL INFILE '/src/assignment2/data/ah' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;

LOAD DATA LOCAL INFILE '/src/assignment2/data/ai' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;


LOAD DATA LOCAL INFILE '/src/assignment2/data/aj' INTO TABLE zillowdata
FIELDS TERMINATED BY ',' 
(parcelid,@airconditioningtypeid,@bathroomcnt,@bedroomcnt,@buildingqualitytypeid,@calculatedfinishedsquarefeet,@fips,@fireplacecnt,@garagecarcnt,@garagetotalsqft,@heatingorsystemtypeid,@lotsizesquarefeet,@poolcnt,@propertylandusetypeid,@rawcensustractandblock,@regionidcity,@regionidneighborhood,@regionidzip,@roomcnt,@unitcnt,@yearbuilt,@numberofstories,@structuretaxvaluedollarcnt,@taxvaluedollarcnt,@assessmentyear,@landtaxvaluedollarcnt,@taxamount,@latitude,@longitude)
SET
airconditioningtypeid=nullif(@airconditioningtypeid,''),
bathroomcnt=nullif(@bathroomcnt,''),
bedroomcnt=nullif(@bedroomcnt,''),
buildingqualitytypeid=nullif(@buildingqualitytypeid,''),
calculatedfinishedsquarefeet=nullif(@calculatedfinishedsquarefeet,''),
fips=nullif(@fips,''),
fireplacecnt=nullif(@fireplacecnt,''),
garagecarcnt=nullif(@garagecarcnt,''),
garagetotalsqft=nullif(@garagetotalsqft,''),
heatingorsystemtypeid=nullif(@heatingorsystemtypeid,''),
lotsizesquarefeet=nullif(@lotsizesquarefeet,''),
poolcnt=nullif(@poolcnt,''),
propertylandusetypeid=nullif(@propertylandusetypeid,''),
rawcensustractandblock=nullif(@rawcensustractandblock,''),
regionidcity=nullif(@regionidcity,''),
regionidneighborhood=nullif(@regionidneighborhood,''),
regionidzip=nullif(@regionidzip,''),
roomcnt=nullif(@roomcnt,''),
unitcnt=nullif(@unitcnt,''),
yearbuilt=nullif(@yearbuilt,''),
numberofstories=nullif(@numberofstories,''),
structuretaxvaluedollarcnt=nullif(@structuretaxvaluedollarcnt,''),
taxvaluedollarcnt=nullif(@taxvaluedollarcnt,''),
assessmentyear=nullif(@assessmentyear,''),
landtaxvaluedollarcnt=nullif(@landtaxvaluedollarcnt,''),
taxamount=nullif(@taxamount,''),
latitude=nullif(@latitude,''),
longitude=nullif(@longitude,'')
;
