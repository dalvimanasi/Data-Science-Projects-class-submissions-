FROM ubuntu:latest

USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    python-pip --upgrade python-pip

RUN pip install --upgrade pip

# install py3
RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    # install python 3
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
	python-matplotlib \
	python-mpltoolkits.basemap \
    pkg-config \
	wget \
	vim &&\
	echo "luigi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    apt-get clean && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# install additional python packages
RUN pip3 install pyproj
RUN pip3 install pyshp
RUN pip3 install ipython
RUN pip install jupyter
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scikit-learn
RUN pip3 install missingno
RUN pip3 install scipy
RUN pip3 install seaborn
#RUN pip install nltk
RUN pip3 install boto3
RUN pip3 install requests
RUN pip3 install plotly
RUN pip3 install beautifulsoup4
RUN pip3 install matplotlib

RUN pip3 install luigi

RUN pip3 install jupyter
RUN pip install --upgrade awscli

# configure console
RUN echo 'alias ll="ls --color=auto -lA"' >> /root/.bashrc \
 && echo '"\e[5~": history-search-backward' >> /root/.inputrc \
 && echo '"\e[6~": history-search-forward' >> /root/.inputrc
# default password: keras
ENV PASSWD='sha1:98b767162d34:8da1bc3c75a0f29145769edc977375a373407824'

# dump package lists
RUN dpkg-query -l > /dpkg-query-l.txt \
 && pip2 freeze > /pip2-freeze.txt \
 && pip3 freeze > /pip3-freeze.txt

RUN wget http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz
RUN tar -zxvf basemap-1.0.7.tar.gz
RUN cd basemap-1.0.7

RUN wget http://download.osgeo.org/geos/geos-3.5.0.tar.bz2
RUN tar xvjf geos-3.5.0.tar.bz2
RUN cd geos-3.5.0
RUN geos-3.5.0/configure
RUN make
RUN make install
 
RUN pip3 install https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz

# for jupyter
EXPOSE 8888

WORKDIR /src/

RUN mkdir /src/midterm
RUN mkdir /src/midterm/EDANotebooks
RUN mkdir /src/midterm/temp
RUN mkdir /src/midterm/logs
RUN mkdir /src/midterm/data
RUN mkdir /src/midterm/config
RUN mkdir /src/midterm/scripts
ENV MAINPATH=/src/midterm

ENV TEMPPATH=/src/midterm/temp
ENV LOGPATH=/src/midterm/logs
ENV CONFIGPATH=/src/midterm/config
ENV DATAPATH=/src/midterm/data
ENV SCRIPTSPATH=/src/midterm/scripts

ENV PYTHONPATH=$SCRIPTSPATH:$PYTHONPATH

ADD runPart1.sh /src/midterm/
ADD runPart2Single.sh /src/midterm/
ADD runPart2Multiple.sh /src/midterm/
ADD scripts/* $SCRIPTSPATH/
ADD config/* $CONFIGPATH/
ADD EDAJupyterNotebooks/* /src/midterm/EDANotebooks/

#testing
#ADD MA_21062017_WBAN_14702.csv /src/assignment1/output/
#RUN chmod 777 /src/assignment1/output/MA_21062017_WBAN_14702.csv

RUN chmod 777 /src/midterm/runPart1.sh
RUN chmod 777 /src/midterm/runPart2Single.sh
RUN chmod 777 /src/midterm/runPart2Multiple.sh
RUN chmod 777 $SCRIPTSPATH/*
RUN chmod 777 $CONFIGPATH/*

WORKDIR /src/midterm/

#CMD /src/midterm/runPart1.sh

#RUN mkdir /srv/nb1/

#CMD /bin/bash -c 'jupyter notebook --no-browser --allow-root --ip=* --NotebookApp.password="$PASSWD" "$@"'
CMD /bin/bash -c 'jupyter notebook --no-browser --ip=* --NotebookApp.password="$PASSWD" "$@"'
#CMD /bin/bash -c 'jupyter notebook --no-browser --ip=* --NotebookApp.password="keras" "$@"'