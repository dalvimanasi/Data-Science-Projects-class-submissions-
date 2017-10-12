# ADSAssignment1
This repository is for the submission of ADS Assignment1

## The execution instructions are given in the report as well.

### Data Ingestion

Step 1 : Pull the image
```
docker pull vishalsatam1988/assign1dataingestion
```

Step 2 : Create the container using 
```
docker create --name="testname" vishalsatam1988/assign1dataingestion
```

Step 3 :  copy your config.json and the configIntial.json file to update the links and your AWS credentials. Please do not change the name of these files.
```
docker cp <local file path> <containername>:/src/assignment1/
docker cp config.json testname:/src/assignment1/
```

Step 4  : Start the container
```
docker start <containername>
docker start -i testname
```

Step 5 : Commit the container to persist the changes
```
docker commit <containername> <new image name>
docker commit testname vishalsatam1988/assign1dataingestion
```

Step 6 : Run the jupyter notebook on the committed image in detached mode
```
docker run -it -d --name “dataingestion” -p 8888:8888 vishalsatam1988/assign1dataingestion /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
```

Step 7 :  Connect to this running container via browser by entering
```
http://<docker machine ip address>:8888
Password for the jupyter notebook is keras
```

Step 8 : Execute the bin/bash command to enter the running container to check output and logs
```
docker exec -it dataingestion /bin/bash
```


### Data Wrangling

Step 1 : Pull the image
The docker image is present on the docker hub and is available to pull using the following command
```
docker pull vishalsatam1988/assign1datawrangling
```

Step 2 : Create the container using the below command 
```
docker create --name="datawrangling" vishalsatam1988/assign1datawrangling
```

Step 3 :  copy your configWrangle.json file to update the link. Please do not change the name of the config file.
```
docker cp <local file path> <containername>:/src/assignment1/
docker cp configWrangle.json datawrangling:/src/assignment1/
```

Step 4  : Start the container
```
docker start <containername>
docker start -i datawrangling
```

Step 5 : Commit the container to persist the changes
```
docker commit <containername> <new image name>
docker commit datawrangling vishalsatam1988/assign1datawrangling
```

Step 6 : Run the jupyter notebook on the committed image in detached mode
```
docker run -it -d --name “datawranglingjupyter” -p 8888:8888 vishalsatam1988/assign1datawrangling /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
```

Step 7 :  Connect to this running container via browser by entering
```
http://<docker machine ip address>:8888
Password for the jupyter notebook is keras
```

Step 8 : Execute the bin/bash command to enter the running container to check output and logs
```
docker exec -it datawranglingjupyter /bin/bash
```
