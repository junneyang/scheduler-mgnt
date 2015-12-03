from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from app import views as app_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

    #added by app
    #('^header/$', app_views.header),
    #('^footer/$', app_views.footer),
    ('^$', app_views.index),
    ('^gettest/$', app_views.gettest),
    ('^posttest/$', app_views.posttest),

    ###################################
    ('^get_schedulers/$', app_views.get_schedulers),
    ('^get_marathon_leader/$', app_views.get_marathon_leader),
    ('^get_mesos_info/$', app_views.get_mesos_info),
    ('^svc_create/$', app_views.svc_create),
    ('^svc_delete/$', app_views.svc_delete),
    ('^svc_update/$', app_views.svc_update),
    ('^get_svc_deploy_status/$', app_views.get_svc_deploy_status),
    ('^get_svc_apps/$', app_views.get_svc_apps),
    ('^get_app_instances/$', app_views.get_app_instances),
    ('^callback/$', app_views.callback),
)
