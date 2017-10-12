# ADS-Midterm

The assignment focusses on performing Exploratory Data Analysis, Prediction and Classification on the Freddie Mac Single Family Loans Dataset.

You can execute this project using the docker images that have been hosted on DockerHub.

You will have to create a new login with Freddie Mac Single Family Loans website ( http://www.freddiemac.com/research/datasets/sf_loanlevel_dataset.html )and enter your login credentials as shown below to use the docker image.


This is a repository the submission of Assignment 2 for Team 1

## Execution Instructions

### Pull the image

```
docker pull vishalsatam1988/midterm
```

### Part 1 - Summarization and EDA

Run the summarization script
```
docker run -it vishalsatam1988/midterm sh /src/midterm/runPart1.sh "<username>" "<password>" <startyear> <endyear>
```
```
Eg : docker run -it vishalsatam1988/midterm sh /src/midterm/runPart1.sh "satam.v@husky.neu.edu" "Eq=yF?f3" 2005 2016
```

Commit the running container
```
docker commit <containerid> vishalsatam1988/midterm
```

View results in Jupyter Notebook - Open /src/midterm/EDANotebooks/Part1EDA
```
docker run -it -d -p 8888:8888 vishalsatam1988/midterm /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
```

### Part 2
#### Prediction and Classification for a Single Quarter

Run the script to analyze (train, test) on one quarter
```
docker run -it vishalsatam1988/midterm sh /src/midterm/runPart2Single.sh "<username>" "<password>" <quarteryear>
```
```
Eg : docker run -it vishalsatam1988/midterm sh /src/midterm/runPart2Single.sh "satam.v@husky.neu.edu" "Eq=yF?f3" Q12005
```
Commit the image
```
docker commit <containerid> vishalsatam1988/midterm
```
The error metrics for the data can be found at /src/midterm/data/
View the resulting evaluation csv for prediction and classificaction using the jupyter notebook 
* Prediction - /src/midterm/EDANotebooks/EvaluationOfPredictionMatrix
* Classification - /src/midterm/EDANotebooks/EvaluationOfPredictionMatrix
Password to open the Jupyter Notebook is "keras"
```
docker run -it -d -p 8888:8888 vishalsatam1988/midterm /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
```

#### Prediction and Classification for Multiple Quarter

Run the script to analyze (train, test) on multiple quarters
```
docker run -it vishalsatam1988/midterm sh /src/midterm/runPart2Multiple.sh "<username>" "<password>" <startquarteryear> <endquarteryear>
```
```
Eg : docker run -it vishalsatam1988/midterm sh /src/midterm/runPart2Multiple.sh "satam.v@husky.neu.edu" "Eq=yF?f3" Q11999 Q12016
```

Commit the image
```
docker commit <containerid> vishalsatam1988/midterm
```
The error metrics for the data can be found at /src/midterm/data/
View the resulting evaluation csv for prediction and classificaction using the jupyter notebook 
* Prediction - /src/midterm/EDANotebooks/EvaluationOfPredictionMatrix
* Classification - /src/midterm/EDANotebooks/EvaluationOfPredictionMatrix
Password to open the Jupyter Notebook is "keras"
```
docker run -it -d -p 8888:8888 vishalsatam1988/midterm /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
```
