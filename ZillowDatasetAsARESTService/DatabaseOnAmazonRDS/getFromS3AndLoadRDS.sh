filename=$LOGPATH/$(date "+%d%m%Y%H%m%s").log
echo $filename
touch $filename
echo "copying db config files data from config.txt"
echo "copying db config files data from config.txt" >> $filename
head $CONFIGPATH/config.txt --lines=4 >> /etc/mysql/my.cnf
echo "Setting AWS Access Keys from config.txt"
echo "Setting AWS Access Keys from config.txt" >> $filename
awskey=$(sed '5!d' $CONFIGPATH/config.txt)
awssecret=$(sed '6!d' $CONFIGPATH/config.txt)
export "$awskey"
export "$awssecret"

if [ -e $DATAPATH/zillowdata.csv ]
then
	echo "File Exists. Will not download"
	echo "File Exists. Will not download" >> $filename
else
	echo "Downloading from S3"
	echo "Downloading from S3" >> $filename
	aws s3 cp s3://Team1_ZillowData/zillowdata.csv $DATAPATH/
fi

echo "Splitting the large file into 10 different files"
echo "Splitting the large file into 10 different files" >> $filename
chmod 777 $DATAPATH/*
sed -i '1d' $DATAPATH/zillowdata.csv
chmod 777 $DATAPATH/*
split -300000 $DATAPATH/zillowdata.csv $DATAPATH/
chmod 777 $DATAPATH/*
echo "Dropping zillowdata if it exists. Executing script dropscript.sql"
echo "Dropping zillowdata if it exists. Executing script dropscript.sql" >> $filename
mysql zillowdb < $SCRIPTSPATH/dropscript.sql
echo "Creating and uploading supporting tables"
echo "Creating and uploading supporting tables" >> $filename
mysql zillowdb < $SCRIPTSPATH/sidetables.sql
echo "Uploading data to Amazon RDS. Executing script loadingscript.sql -- This may take some time around 10 minutes depending on your internet connection, please be patient!!"
echo "Uploading data to Amazon RDS. Executing script loadingscript.sql -- This may take some time around 10 minutes depending on your internet connection, please be patient!!" >> $filename
mysql zillowdb < $SCRIPTSPATH/loadingscript.sql
echo "All tables created"
echo "All tables created" >> $filename
echo "Removing temporary split files"
echo "Removing temporary split files" >> $filename
rm $DATAPATH/aa
rm $DATAPATH/ab
rm $DATAPATH/ac
rm $DATAPATH/ad
rm $DATAPATH/ae
rm $DATAPATH/af
rm $DATAPATH/ag
rm $DATAPATH/ah
rm $DATAPATH/ai
rm $DATAPATH/aj

