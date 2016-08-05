from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import so.views
import dev.views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'so.views.home', name='home'),
    url(r'^user/', include('so.urls')),
    # url(r'^init/', include('so.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	 
     url(r'^$', so.views.user_login),
     url(r'^index$', so.views.index),
	 url(r'^login', so.views.user_login),
     url(r'^conf_edit/(.+)/$', so.views.conf_edit),
	 url(r'^conf_del/(.+)/$', so.views.conf_del),
	 url(r'^file_del/(.+)/$', so.views.file_del),
	 url(r'^file_list$', so.views.file_list),
	 url(r'^edit$', so.views.edit),
	 url(r'^push$', so.views.push),
	 url(r'^push_list$', so.views.push_list),
	 # url(r'^push_detail/(.+)/$', so.views.push_detail),
	 url(r'^group_edit/(.+)/$', so.views.group_edit),
	 url(r'^group_del/(.+)/$', so.views.group_del),
	 url(r'^host_del/(.+)/$', so.views.host_del),
	 url(r'^salt_group$', so.views.salt_group),
	 url(r'^salt_hosts$', so.views.salt_hosts),
	 # url(r'^users$', so.views.users),
	 url(r'^new_config$', so.views.new_config),
	 url(r'^new_task$', so.views.new_task),
	 url(r'^logout$', so.views.user_logout),
	 url(r'^zabbix_host$', so.views.zabbix_host),
	 url(r'^zabbix_alert$', so.views.zabbix_alert),
	 url(r'^zabbix_graps$', so.views.zabbix_graps),
	 url(r'^update_host$', so.views.update_host),
	 url(r'^update_device$', so.views.update_device),
	 url(r'^ganglia$', so.views.ganglia),
	 
	 url(r'^remote$', so.views.remote),
	 url(r'^uploadfile$', so.views.uploadfile),
	 #url(r'^show_images$', so.views.show_images),
	 url(r'^task_save$', so.views.task_save),
	url(r'^progress/(.+)/(.+)/(.+)/$', so.views.progress),
	url(r'^sysconf$', so.views.sysconf),
    url(r'^device$', so.views.device),
    url(r'^device_add$', so.views.device_add),
    url(r'^device_edit/(.+)/$', so.views.device_edit),
    url(r'^device_del/$', so.views.device_del),
    url(r'^device_detail/(.+)/$', so.views.device_detail),
    url(r'^info_update$', so.views.info_update),
    url(r'^device_group$', so.views.device_group),
    url(r'^idc$', so.views.idc),
    url(r'^idc_del/(.+)/$', so.views.idc_del),
    url(r'^idc_edit/(.+)/$', so.views.idc_edit),
    url(r'^grp_edit/(.+)/$', so.views.grp_edit),
    url(r'^grp_del/(.+)/$', so.views.grp_del),
    # url(r'^install_info$', so.views.install_info),
    url(r'^install_os/$', so.views.install_os),
    url(r'^install_init/$', so.views.install_init),
    # url(r'^install_jb$', so.views.install_jb),
    
]
