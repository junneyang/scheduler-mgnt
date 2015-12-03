# This is a comment
#FROM ubuntu:14.04
#MAINTAINER JunneYang <597092663@qq.com>

#RUN apt-get update -y

#RUN apt-get install python-pip -y
#RUN pip install --upgrade pip
#RUN pip install Django==1.8.3 
#RUN apt-get install python-dev libmysqlclient-dev -y
#RUN pip install MySQL-python==1.2.5

#RUN pip install uwsgi
#RUN apt-get install nginx -y

FROM 10.5.24.46:80/django:1.0.0.0

RUN pip install celery==3.1.19
RUN pip install Mako==1.0.3

RUN mkdir -p /opt/applications
COPY ./applications/ /opt/applications/
RUN find /opt/applications/ -type d -name ".svn" | xargs rm -rf
RUN chmod 755 /opt/applications/run.sh

VOLUME ["/opt/applications/logs", "/opt/applications/template/sharedfiles"]

CMD ["/bin/bash", "-c", "env && cd /opt/applications/ && ./run.sh"]

