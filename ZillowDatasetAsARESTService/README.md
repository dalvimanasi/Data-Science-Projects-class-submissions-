# ADSAssignment2
This is a repository the submission of Assignment 2 for Team 1

## The execution instructions are given in the report as well.

### 1.	Step 1 : Pull the image

```
docker pull vishalsatam1988/wrangleanduploadassignment2
```

### 2.	Step 2 : Create the container
```
docker create --name="assignment2EDA" vishalsatam1988/wrangleanduploadassignment2
```

### 3.	Copy your config file. (The name of the file has to be config.json)
```
docker cp <local file path> <containername>:/src/assignment2/config/
docker cp <path>/config.json assignment2EDA:/src/assignment2/config/
```

### 4.	Start the container 
```
docker start <containername>
docker start -i assignment2EDA
```

### 5.Commit the container if you want to see logs otherwise invoke the following command to check the jupyter notebooks.
### Command to commit - docker commit assignment2EDA vishalsatam1988/wrangleanduploadassignment2
```
docker run -it -d --name “assignment2EDAjupyter” -p 8888:8888 vishalsatam1988/wrangleanduploadassignment2 /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
```

Password to open jupyter notebook :  keras

## Docker image - vishalsatam1988/createdbanduseapi

### 1.	Step 1 : Pull the image
The docker image is present on the docker hub and is available to pull using the following command
```
docker pull vishalsatam1988/createdbanduseapi
```

### 2.	Step 2 : Create the container
```
docker create --name="assignment2RDS" vishalsatam1988/createdbanduseapi
```

### 3.	Copy your config file. (The name of the file has to be config.txt)
```
docker cp <local file path> <containername>:/src/assignment2/config/
docker cp <path>/config.txt assignment2RDS:/src/assignment2/config/
```

### 4.	Start the container
```
docker start <containername>
docker start -i assignment2RDS
```

### 5.	Commit the container if you want to see logs otherwise invoke the following command to check the jupyter notebooks.
###     Command to commit - docker commit assignment2RDS vishalsatam1988/createdbanduseapi
```

docker run -it -d --name “assignment2RDS” -p 8888:8888 vishalsatam1988/createdbanduseapi /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
```

Password to open jupyter notebook :  keras

