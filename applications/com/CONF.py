#!/usr/bin/env python
#-*- coding: utf-8 -*-

BROKER='amqp://guest@10.5.24.66//'
#BACKEND='redis://10.5.24.66:6379/0'
BACKEND=None

SCHEDULER={
    "1":{
        "MARATHON_ENDPOINTS":"10.5.24.20:8080;10.5.24.21:8080;10.5.24.23:8080"
    }
}
#"MESOS_ENDPOINTS":"10.5.24.20:5050;10.5.24.21:5050;10.5.24.23:5050"


