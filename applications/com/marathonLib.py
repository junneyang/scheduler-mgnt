#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import traceback
import logging
import sys
import os

from celery import Celery
from com import CONF
from com.jsonLib import jsonStr,jsonResponse

pro_dir = ''  #可以自己用绝对路径定义,目的是工程目录下
pro_dir = os.getcwd()  #如果放在project目录，就不需要在配置绝对路径了
sys.path.append(pro_dir)
os.environ.update({"DJANGO_SETTINGS_MODULE": "mysite.settings"})  #项目的settings

#sys.path.append('../')
#os.environ.update({"DJANGO_SETTINGS_MODULE": "mysite.settings"})


def get_marathon_leader(scheduler_id):
    try:
        logger = logging.getLogger('django')
        MARATHON_ENDPOINTS = CONF.SCHEDULER[str(scheduler_id)]['MARATHON_ENDPOINTS']
        marathon_endpoint_list = MARATHON_ENDPOINTS.split(";")
        flag = False
        for item in marathon_endpoint_list:
            r = requests.get('http://'+item+'/v2/leader')
            logging.info(r.status_code)
            logger.info(r.json())
            if(r.status_code == requests.codes.ok):
                flag = True
                marathon_leader = r.json()
                break
            else:
                raise Exception(r.json())
    except Exception as e:
        #traceback.print_exc()
        logger.error(e, exc_info=1)
        raise Exception(e)
    else:
        return marathon_leader

def get_mesos_info(scheduler_id):
    try:
        logger = logging.getLogger('django')
        MARATHON_ENDPOINTS = CONF.SCHEDULER[str(scheduler_id)]['MARATHON_ENDPOINTS']
        marathon_endpoint_list = MARATHON_ENDPOINTS.split(";")
        flag = False
        for item in marathon_endpoint_list:
            r = requests.get('http://'+item+'/v2/info')
            logger.info(r.status_code)
            logger.info(r.json())
            if(r.status_code == requests.codes.ok):
                flag = True
                mesos_leader = r.json()['marathon_config']['mesos_leader_ui_url']
                framework_id = r.json()['frameworkId']
                msg = {}
                msg['mesos_leader'] = mesos_leader
                msg['framework_id'] = framework_id
                break
            else:
                raise Exception(r.json())
    except Exception as e:
        #traceback.print_exc()
        logger.error(e, exc_info=1)
        raise Exception(e)
    else:
        return msg

def svc_create(scheduler_id, svc_params):
    try:
        logger = logging.getLogger('django')
        marathon_leader = get_marathon_leader(scheduler_id)
        headers = {'content-type':'application/json;charset=utf-8'}
        #logger.info(marathon_leader)
        r = requests.post('http://'+marathon_leader['leader']+'/v2/groups', data=svc_params, headers=headers)
        logger.info(r.status_code)
        logger.info(r.json())
        #if(r.status_code == requests.codes.ok):
        if('deploymentId' in r.json()):
            deploy_info = r.json()
        else:
            raise Exception(r.json())
    except Exception as e:
        #traceback.print_exc()
        logger.error(e, exc_info=1)
        raise Exception(e)
    else:
        return deploy_info

def svc_delete(scheduler_id, svc_catalog, apply_id):
    try:
        logger = logging.getLogger('django')
        marathon_leader = get_marathon_leader(scheduler_id)
        headers = {'content-type':'application/json;charset=utf-8'}
        #logger.info(marathon_leader)
        r = requests.delete('http://'+marathon_leader['leader']+'/v2/groups/'+svc_catalog+"/"+str(apply_id)+"?force=true", headers=headers)
        logger.info(r.status_code)
        logger.info(r.json())
        #if(r.status_code == requests.codes.ok):
        if('deploymentId' in r.json()):
            deploy_info = r.json()
        else:
            raise Exception(r.json())
    except Exception as e:
        #traceback.print_exc()
        logger.error(e, exc_info=1)
        raise Exception(e)
    else:
        return deploy_info

def svc_update(scheduler_id, svc_params):
    try:
        logger = logging.getLogger('django')
        marathon_leader = get_marathon_leader(scheduler_id)
        headers = {'content-type':'application/json;charset=utf-8'}
        #logger.info(marathon_leader)
        r = requests.put('http://'+marathon_leader['leader']+'/v2/groups', data=svc_params, headers=headers)
        logger.info(r.status_code)
        logger.info(r.json())
        #if(r.status_code == requests.codes.ok):
        if('deploymentId' in r.json()):
            deploy_info = r.json()
        else:
            raise Exception(r.json())
    except Exception as e:
        #traceback.print_exc()
        logger.error(e, exc_info=1)
        raise Exception(e)
    else:
        return deploy_info

def get_svc_apps(scheduler_id, svc_catalog, apply_id):
    try:
        logger = logging.getLogger('django')
        marathon_leader = get_marathon_leader(scheduler_id)
        headers = {'content-type':'application/json;charset=utf-8'}
        r = requests.get('http://'+marathon_leader['leader']+'/v2/groups/'+svc_catalog+'/'+str(apply_id), headers=headers)
        #print r.status_code
        #print r.json()
        app_name_list = []
        app_info = []
        groups = r.json()
        if(r.status_code == 200):
            for item in groups['apps']:
                app_name_list.append(item['id'])
        else:
            raise Exception(jsonStr(groups))

        for app in app_name_list:
            r = requests.get('http://'+marathon_leader['leader']+'/v2/apps'+app, headers=headers)
            msg = r.json()['app']
            app_info_tmp = {}
            if(r.status_code == 200):
                app_info_tmp['id'] = msg['id']
                app_info_tmp['mem'] = msg['mem']
                app_info_tmp['cpus'] = msg['cpus']
                app_info_tmp['instances'] = msg['instances']
                app_info_tmp['tasksStaged'] = msg['tasksStaged']
                app_info_tmp['tasksRunning'] = msg['tasksRunning']
                app_info_tmp['tasksHealthy'] = msg['tasksHealthy']
                app_info_tmp['tasksUnhealthy'] = msg['tasksUnhealthy']
                app_info.append(app_info_tmp)
            else:
                raise Exception(jsonStr(msg))
    except Exception as e:
        #traceback.print_exc()
        logger.error(e, exc_info=1)
        raise Exception(e)
    else:
        return app_info

def get_app_instances(scheduler_id, app_id):
    try:
        logger = logging.getLogger('django')
        marathon_leader = get_marathon_leader(scheduler_id)
        mesos_info = get_mesos_info(scheduler_id)
        mesos_leader = mesos_info['mesos_leader']
        framework_id = mesos_info['framework_id']
        headers = {'content-type':'application/json;charset=utf-8'}
        r = requests.get('http://'+marathon_leader['leader']+'/v2/apps'+app_id+'/tasks', headers=headers)
        #print r.status_code
        #print r.json()
        msg = None
        if(r.status_code == 200):
            msg = r.json()['tasks']
            for msg_item in msg:
                msg_item['log'] = mesos_leader + "#/slaves/" + msg_item['slaveId'] + "/frameworks/" + framework_id + "/executors/" + msg_item['id']
        else:
            raise Exception(jsonStr(r.json()))
    except Exception as e:
        #traceback.print_exc()
        logger.error(e, exc_info=1)
        raise Exception(e)
    else:
        return msg

if __name__ == "__main__":
    #print get_marathon_leader()
    '''project_id = '1'
    user_id = '1'
    svc_id = '1'
    action_type = 'new_instance'
    svc_type = 'PAAS_RDB_MySQL_Docker'
    sub_type = 'single_instance'
    svc_label = 'test'
    svc_params = {"instance_name":"mysql01","mysql_version":"5.6"}
    task_id = task_submit(project_id, user_id, svc_id, action_type, svc_type, sub_type, svc_label, svc_params)
    print task_id'''

    print get_group_apps(1, 1, 25, 'test')

