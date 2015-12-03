from django.db import models

# Create your models here.
SVC_DEPLOY_STATUS_CHOICES = (
    (u'0', u'SUBMITTED'),
    (u'1', u'DEPLOYING'),
    (u'2', u'EXCEPTION'),
    (u'3', u'SUCCESS'),
)

SVC_DEPLOY_ACTION_CHOICES = (
    (u'0', u'CREATE'),
    (u'1', u'UPDATE'),
    (u'2', u'DELETE'),
)

class SVC_Deploy(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=128)
    apply_id = models.IntegerField()
    svc_catalog = models.CharField(max_length=128)
    deploy_id = models.CharField(max_length=128)
    start_time = models.DateTimeField(auto_now_add=True, null=False)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=SVC_DEPLOY_STATUS_CHOICES)
    description = models.CharField(max_length=128)
    info = models.TextField(blank=True, null=True)

