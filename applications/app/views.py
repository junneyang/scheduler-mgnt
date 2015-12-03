#!/usr/bin/env python
#-*- coding: utf-8 -*-
#from django.shortcuts import render

# Create your views here.
import sys
import json
import logging
import datetime
from datetime import datetime
import requests

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.utils.timezone import localtime

from app import models

from com.errocodeLib import ERRORCODE
from com.jsonLib import jsonStr,jsonResponse
from com import CONF
from com import marathonLib

################################################################################
def index(request):
    try:
        return render_to_response("index.html")
    except Exception as e:
        raise Http404(e)

def gettest(request):
    try:
        logger = logging.getLogger('django')
        a = request.GET.get("a")
        b = request.GET.get("b")
        logger.info(a)
        logger.info(b)
        cu_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = "Hello world, a = " + a + ", b = " + b + ", it's time now " + cu_time
        import codecs
        with codecs.open("./template/sharedfiles/sharedfile.txt", "a", "utf-8") as f:
            f.write(msg + "\n")
        logger.info(msg)
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def posttest(request):
    try:
        logger = logging.getLogger('django')
        requestData = json.loads(request.body)
        email = requestData['email']
        logger.info(email)
        cutime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(cutime)
        msg = cutime
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def get_schedulers(request):
    try:
        logger = logging.getLogger('django')
        msg = CONF.SCHEDULER
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def get_marathon_leader(request):
    try:
        logger = logging.getLogger('django')
        scheduler_id = request.GET.get("scheduler_id")
        marathon_leader = marathonLib.get_marathon_leader(scheduler_id)
        msg = marathon_leader
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def get_mesos_info(request):
    try:
        logger = logging.getLogger('django')
        scheduler_id = request.GET.get("scheduler_id")
        mesos_info = marathonLib.get_mesos_info(scheduler_id)
        msg = mesos_info
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def svc_create(request):
    try:
        logger = logging.getLogger('django')
        requestData = json.loads(request.body)
        scheduler_id = requestData['scheduler_id']
        svc_params = requestData['svc_params']
        logger.info("scheduler_id: ")
        logger.info(scheduler_id)
        logger.info("svc_params: ")
        logger.info(jsonStr(svc_params))

        svc_catalog = svc_params['id'].split("/")[1]
        logger.info("svc_catalog: ")
        logger.info(svc_catalog)
        apply_id = svc_params['id'].split("/")[2]
        logger.info("apply_id: ")
        logger.info(apply_id)

        action=models.SVC_DEPLOY_ACTION_CHOICES[0][1]
        svc_deploy = models.SVC_Deploy(action=action,
                             svc_catalog=svc_catalog, apply_id=apply_id,
                             status=models.SVC_DEPLOY_STATUS_CHOICES[0][0],
                             description=models.SVC_DEPLOY_STATUS_CHOICES[0][1])
        svc_deploy.save()
        svc_deploy_id = svc_deploy.id
        logger.info("##########" + action + " " + svc_params['id'] + " SUBMITTED" + "##########")

        deploy_info = marathonLib.svc_create(scheduler_id, jsonStr(svc_params))
        svc_deploy.deploy_id = deploy_info['deploymentId']
        svc_deploy.status = models.SVC_DEPLOY_STATUS_CHOICES[1][0]
        svc_deploy.description = models.SVC_DEPLOY_STATUS_CHOICES[1][1]
        svc_deploy.save()
        logger.info("##########" + action + " " + svc_params['id'] + " DEPLOYING" + "##########")

        msg = {"deploy_id": svc_deploy_id}
    except Exception as e:
        logger.error(e, exc_info=1)
        svc_deploy.status = models.SVC_DEPLOY_STATUS_CHOICES[2][0]
        svc_deploy.description = models.SVC_DEPLOY_STATUS_CHOICES[2][1]
        svc_deploy.info = str(e)
        svc_deploy.save()
        logger.info("##########" + action + " " + svc_params['id'] + " EXCEPTION" + "##########")
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def svc_delete(request):
    try:
        logger = logging.getLogger('django')
        requestData = json.loads(request.body)
        scheduler_id = requestData['scheduler_id']
        svc_catalog = requestData['svc_catalog']
        apply_id = requestData['apply_id']

        logger.info("scheduler_id: ")
        logger.info(scheduler_id)
        logger.info("svc_catalog: ")
        logger.info(svc_catalog)
        logger.info("apply_id: ")
        logger.info(apply_id)

        action=models.SVC_DEPLOY_ACTION_CHOICES[2][1]
        svc_deploy = models.SVC_Deploy(action=action,
                             svc_catalog=svc_catalog, apply_id=apply_id,
                             status=models.SVC_DEPLOY_STATUS_CHOICES[0][0],
                             description=models.SVC_DEPLOY_STATUS_CHOICES[0][1])
        svc_deploy.save()
        svc_deploy_id = svc_deploy.id
        logger.info("##########" + action + " " + svc_catalog + "/" + apply_id + " SUBMITTED" + "##########")

        deploy_info = marathonLib.svc_delete(scheduler_id, svc_catalog, apply_id)
        svc_deploy.deploy_id = deploy_info['deploymentId']
        svc_deploy.status = models.SVC_DEPLOY_STATUS_CHOICES[1][0]
        svc_deploy.description = models.SVC_DEPLOY_STATUS_CHOICES[1][1]
        svc_deploy.save()
        logger.info("##########" + action + " " + svc_catalog + "/" + apply_id + " DEPLOYING" + "##########")

        msg = {"deploy_id": svc_deploy_id}
    except Exception as e:
        logger.error(e, exc_info=1)
        svc_deploy.status = models.SVC_DEPLOY_STATUS_CHOICES[2][0]
        svc_deploy.description = models.SVC_DEPLOY_STATUS_CHOICES[2][1]
        svc_deploy.info = str(e)
        svc_deploy.save()
        logger.info("##########" + action + " " + svc_catalog + "/" + apply_id + " EXCEPTION" + "##########")
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def svc_update(request):
    try:
        logger = logging.getLogger('django')
        requestData = json.loads(request.body)
        scheduler_id = requestData['scheduler_id']
        svc_params = requestData['svc_params']
        logger.info("scheduler_id: ")
        logger.info(scheduler_id)
        logger.info("svc_params: ")
        logger.info(jsonStr(svc_params))

        svc_catalog = svc_params['id'].split("/")[1]
        logger.info("svc_catalog: ")
        logger.info(svc_catalog)
        apply_id = svc_params['id'].split("/")[2]
        logger.info("apply_id: ")
        logger.info(apply_id)

        action=models.SVC_DEPLOY_ACTION_CHOICES[1][1]
        svc_deploy = models.SVC_Deploy(action=action,
                             svc_catalog=svc_catalog, apply_id=apply_id,
                             status=models.SVC_DEPLOY_STATUS_CHOICES[0][0],
                             description=models.SVC_DEPLOY_STATUS_CHOICES[0][1])
        svc_deploy.save()
        svc_deploy_id = svc_deploy.id
        logger.info("##########" + action + " " + svc_params['id'] + " SUBMITTED" + "##########")

        deploy_info = marathonLib.svc_update(scheduler_id, jsonStr(svc_params))
        svc_deploy.deploy_id = deploy_info['deploymentId']
        svc_deploy.status = models.SVC_DEPLOY_STATUS_CHOICES[1][0]
        svc_deploy.description = models.SVC_DEPLOY_STATUS_CHOICES[1][1]
        svc_deploy.save()
        logger.info("##########" + action + " " + svc_params['id'] + " DEPLOYING" + "##########")

        msg = {"deploy_id": svc_deploy_id}
    except Exception as e:
        logger.error(e, exc_info=1)
        svc_deploy.status = models.SVC_DEPLOY_STATUS_CHOICES[2][0]
        svc_deploy.description = models.SVC_DEPLOY_STATUS_CHOICES[2][1]
        svc_deploy.info = str(e)
        svc_deploy.save()
        logger.info("##########" + action + " " + svc_params['id'] + " EXCEPTION" + "##########")
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def get_svc_deploy_status(request):
    try:
        logger = logging.getLogger('django')
        deploy_id = request.GET.get("deploy_id")
        item = models.SVC_Deploy.objects.get(id=deploy_id)
        msg = {}
        msg['deploy_id'] = item.id
        msg['action'] = item.action
        msg['apply_id'] = item.apply_id
        msg['start_time'] = str(localtime(item.start_time))
        if(item.end_time == None):
            msg['end_time'] = '-'
        else:
            msg['end_time'] = str(localtime(item.end_time))
        msg['status'] = item.status
        msg['description'] = item.description
        if(item.info == None):
            msg['info'] = '-'
        else:
            msg['info'] = item.info
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def get_svc_apps(request):
    try:
        logger = logging.getLogger('django')
        scheduler_id = request.GET.get("scheduler_id")
        svc_catalog = request.GET.get("svc_catalog")
        apply_id = request.GET.get("apply_id")
        msg = marathonLib.get_svc_apps(scheduler_id, svc_catalog, apply_id)
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def get_app_instances(request):
    try:
        logger = logging.getLogger('django')
        scheduler_id = request.GET.get("scheduler_id")
        app_id = request.GET.get("app_id")
        msg = marathonLib.get_app_instances(scheduler_id, app_id)
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def callback(request):
    try:
        logger = logging.getLogger('django')
        requestData = json.loads(request.body)
        #logger.info(jsonStr(requestData))
        msg = requestData
        #####Deployments
        if(msg['eventType'] == 'deployment_success' or msg['eventType'] == 'deployment_failed'):
            tmp = msg['plan']['steps'][0]['actions'][0]['app'].split("/")
            deploy_id = msg['id']
            svc_catalog = tmp[1]
            apply_id = tmp[2]
            logger.info(msg['eventType'] + ' ' + deploy_id + ' ' + svc_catalog + ' ' + apply_id)
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if(msg['eventType'] == 'deployment_success'):
                status = models.SVC_DEPLOY_STATUS_CHOICES[3][0]
                description = models.SVC_DEPLOY_STATUS_CHOICES[3][1]
                logger.info("##########" + svc_catalog + "/" + apply_id + " SUCCESS" + "##########")
            else:
                status = models.SVC_DEPLOY_STATUS_CHOICES[2][0]
                description = models.SVC_DEPLOY_STATUS_CHOICES[2][1]
                logger.info("##########" + svc_catalog + "/" + apply_id + " EXCEPTION" + "##########")
            update_svc_deploy_status(svc_catalog, apply_id, deploy_id, end_time, status, description)
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        #logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def update_svc_deploy_status(svc_catalog, apply_id, deploy_id, end_time, status, description, info=None):
    try:
        logger = logging.getLogger('django')
        svc_deploy = models.SVC_Deploy.objects.get(svc_catalog=svc_catalog, apply_id=apply_id, deploy_id=deploy_id)
        svc_deploy.end_time = end_time
        svc_deploy.status = status
        svc_deploy.description = description
        svc_deploy.info = info
        svc_deploy.save()
        logger.info("##########" + svc_catalog + " " + apply_id + " "+ deploy_id + " UPDATE SUCCESS" +"##########")
    except Exception as e:
        logger.error(e, exc_info=1)
        raise Exception(e)



'''def svc_update_status(svc_id, status, info):
    try:
        logger = logging.getLogger('django')
        svc = models.SVC.objects.get(id=svc_id)
        svc.status = status
        svc.info = info
        svc.save()
        svc_id = svc.id
        logger.info("svc id: " + str(svc_id) + " update success")
    except Exception as e:
        logger.error(e, exc_info=1)
        raise Exception(e)

def deploy_update_status(svc_id, deploy_id, status, info):
    try:
        logger = logging.getLogger('django')
        deploy = models.Deploy.objects.get(svc_id=svc_id, deploy_id=deploy_id)
        deploy.status = status
        deploy.info = info
        deploy.save()
        deploy_id = deploy.id
        logger.info("deploy id: " + str(deploy_id) + " update success")
    except Exception as e:
        logger.error(e, exc_info=1)
        raise Exception(e)

def svc_apply(request):
    try:
        logger = logging.getLogger('django')
        requestData = json.loads(request.body)
        logger.info(jsonStr(requestData))

        project_id = requestData['project_id']
        user_id = requestData['user_id']
        #svc_id = requestData['svc_id']
        #action_type = requestData['action_type']
        action_type = 'new_instance'
        apply_time_limit = requestData['apply_time_limit']
        svc_type = requestData['svc_type']
        sub_type = requestData['sub_type']
        svc_label = requestData['svc_label']
        svc_params = requestData['svc_params']

        svc = models.SVC(project_id=project_id, user_id=user_id, svc_label=svc_label,
                             svc_type=svc_type, sub_type=sub_type,
                             apply_time_limit=apply_time_limit,
                             svc_params=jsonStr(svc_params),
                             status=models.SVC_STATUS_CHOICES[0][0], info=models.SVC_STATUS_CHOICES[0][1])
        svc.save()
        svc_id = svc.id
        logger.info("svc id: " + str(svc_id) + " saved success")

        task_id = marathonLib.task_submit(project_id, user_id, svc_id, action_type, svc_type, sub_type, svc_label, svc_params)
        logger.info('task '+str(task_id)+' submit success')
        msg = {'svc_id':task_id}
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])

def get_svcs(request):
    try:
        limit = 5
        offset = 0
        sort = "id"
        order = "desc"
        ret = {}
        logger = logging.getLogger('django')
        if(request.GET.has_key('offset') and request.GET.has_key('limit')):
            offset = int(request.GET.get('offset'))
            limit = int(request.GET.get('limit'))
            sort = request.GET.get('sort')
            order = request.GET.get('order')
            #print offset,limit,sort,order
            if(order == "desc" or order == "DESC"):
                order_by = "-" + sort
            else:
                order_by = sort
            svc_set = models.SVC.objects.all().order_by(order_by)[offset:offset+limit]
            total = models.SVC.objects.count()
            svcs = []
            for item in svc_set:
                msg = {}
                msg['id'] = item.id
                msg['project_id'] = item.project_id
                msg['user_id'] = item.user_id
                msg['svc_label'] = item.svc_label
                msg['svc_type'] = item.svc_type
                msg['sub_type'] = item.sub_type
                msg['apply_time'] = str(localtime(item.apply_time))
                msg['apply_time_limit'] = item.apply_time_limit
                msg['status'] = item.status
                msg['operation'] = {"id":item.id,"project_id":item.project_id,"user_id":item.user_id,"svc_label":item.svc_label}
                svcs.append(msg)
            ret['rows'] = svcs
            ret['total'] = total
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    logger.info(json.dumps(ret))
    return jsonResponse(ret)

def get_deploys(request):
    try:
        limit = 5
        offset = 0
        sort = "id"
        order = "desc"
        ret = {}
        logger = logging.getLogger('django')
        if(request.GET.has_key('offset') and request.GET.has_key('limit')):
            offset = int(request.GET.get('offset'))
            limit = int(request.GET.get('limit'))
            sort = request.GET.get('sort')
            order = request.GET.get('order')
            #print offset,limit,sort,order
            if(order == "desc" or order == "DESC"):
                order_by = "-" + sort
            else:
                order_by = sort
            svc_id = request.GET.get('svc_id')
            #deploy_set = models.Deploy.objects.filter(svc_id=svc_id).order_by(order_by)[offset:offset+limit]
            deploy_set = models.Deploy.objects.all().order_by(order_by)[offset:offset+limit]
            total = models.Deploy.objects.count()
            deploys = []
            for item in deploy_set:
                msg = {}
                msg['id'] = item.id
                msg['svc_id'] = item.svc_id
                msg['deploy_id'] = item.deploy_id
                msg['action_type'] = item.action_type
                msg['status'] = item.status
                msg['start_time'] = str(localtime(item.start_time))
                if(item.end_time == None):
                    msg['end_time'] = '-'
                else:
                    msg['end_time'] = str(localtime(item.end_time))
                msg['operation'] = {"id":item.id}
                deploys.append(msg)
            ret['rows'] = deploys
            ret['total'] = total
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    logger.info(json.dumps(ret))
    return jsonResponse(ret)

def get_svc_apps(request):
    try:
        ret = {}
        logger = logging.getLogger('django')
        project_id = request.GET.get('project_id')
        user_id = request.GET.get('user_id')
        svc_id = request.GET.get('svc_id')
        svc_label = request.GET.get('svc_label')

        group_apps = marathonLib.get_group_apps(project_id, user_id, svc_id, svc_label)
        ret['rows'] = group_apps
        ret['total'] = len(group_apps)
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    logger.info(json.dumps(ret))
    return jsonResponse(ret)

def app_list(request):
    try:
        logger = logging.getLogger('django')
        params = {}
        params['project_id'] = request.GET.get('project_id')
        params['user_id'] = request.GET.get('user_id')
        params['svc_id'] = request.GET.get('svc_id')
        params['svc_label'] = request.GET.get('svc_label')

        return render_to_response("./product/app_list_test.html", params)
    except Exception as e:
        raise Http404(e)

def app_tasks(request):
    try:
        logger = logging.getLogger('django')
        params = {}
        params['project_id'] = request.GET.get('project_id')
        params['user_id'] = request.GET.get('user_id')
        params['app_id'] = request.GET.get('app_id')

        return render_to_response("./product/app_task_list_test.html", params)
    except Exception as e:
        raise Http404(e)

def get_app_tasks(request):
    try:
        ret = {}
        logger = logging.getLogger('django')
        project_id = request.GET.get('project_id')
        user_id = request.GET.get('user_id')
        app_id = request.GET.get('app_id')

        app_tasks = marathonLib.get_app_tasks(project_id, user_id, app_id)
        ret['rows'] = app_tasks
        ret['total'] = len(app_tasks)
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    logger.info(json.dumps(ret))
    return jsonResponse(ret)

def svc_delete(request):
    try:
        logger = logging.getLogger('django')
        requestData = json.loads(request.body)
        logger.info(jsonStr(requestData))

        project_id = requestData['project_id']
        user_id = requestData['user_id']
        svc_id = requestData['svc_id']
        #action_type = requestData['action_type']
        action_type = 'delete_instance'
        svc_type = None
        sub_type = None
        svc_label = requestData['svc_label']
        svc_params = None

        task_id = marathonLib.task_submit(project_id, user_id, svc_id, action_type, svc_type, sub_type, svc_label, svc_params)
        logger.info('task '+str(task_id)+' submit success')
        #status = models.SVC_STATUS_CHOICES[7][0]
        #info = models.SVC_STATUS_CHOICES[7][1]
        #svc_update_status(svc_id, status, info)
        msg = {'svc_id':task_id}
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return jsonResponse(ERRORCODE['INTERNAL_ERROR'])
    else:
        ERRORCODE['SUCCESS']['msg'] = msg
        logger.info(jsonStr(ERRORCODE['SUCCESS']))
        return jsonResponse(ERRORCODE['SUCCESS'])
'''


