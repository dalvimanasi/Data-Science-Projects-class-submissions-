use zillowdb;

CREATE TABLE airconditiontype (
    `AirConditioningTypeID` INT,
    `AirConditioningDesc` VARCHAR(30) CHARACTER SET utf8
);

LOAD DATA LOCAL INFILE '/src/assignment2/data/aircondition.csv' INTO TABLE airconditiontype
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(AirConditioningTypeID,AirConditioningDesc)
;

CREATE TABLE heatingsystemtypeid (
    `HeatingOrSystemTypeID` INT,
    `HeatingOrSystemDesc` VARCHAR(30) CHARACTER SET utf8
);

LOAD DATA LOCAL INFILE '/src/assignment2/data/heatingsystemtypeid.csv' INTO TABLE heatingsystemtypeid
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(HeatingOrSystemTypeID,HeatingOrSystemDesc)
;

CREATE TABLE propertydescid (
    `PropertyLandUseTypeID` INT,
    `PropertyLandUseDesc` VARCHAR(30) CHARACTER SET utf8
);

LOAD DATA LOCAL INFILE '/src/assignment2/data/propertydescid.csv' INTO TABLE propertydescid
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(PropertyLandUseTypeID,PropertyLandUseDesc)
;
