FROM centos:7

LABEL maintainer "Wes Lambert, wlambertts@gmail.com"
LABEL version="Hive2Elastic"
LABEL description="Script for automating Hive case correlation with events for Security Onion on the Elastic Stack"

RUN yum update -y && yum -y install epel-release
RUN yum -y install https://$(rpm -E '%{?centos:centos}%{!?centos:rhel}%{rhel}').iuscommunity.org/ius-release.rpm
RUN yum -y makecache && yum -y install python36u python36u-pip && pip3.6 install --upgrade pip && yum clean all
RUN mkdir -p hive2elastic
ADD ./requirements.txt hive2elastic/
ADD ./app/* hive2elastic/
WORKDIR hive2elastic
RUN pip3.6 install -r requirements.txt
ENTRYPOINT ["python3.6", "hive2elastic.py"] 
