luigi --module WrangleAndUploadDataToS3 UploadCleanFileToS3 --local-scheduler
echo "Luigi Tasks completed"
rm -f $OUTPUTPATH/TEMP*
