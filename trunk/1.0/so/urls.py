from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import so.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
	url(r'^$', so.views.user_glist),
	url(r'^new$', so.views.user_new),
	url(r'^edit/(.+)/$', so.views.user_edit),
	url(r'^grouplist$', so.views.user_glist),
	url(r'^userlist$', so.views.user_ulist),
	url(r'^del/(.+)/$', so.views.user_del),
	url(r'^gdel/(.+)/$', so.views.user_gdel),
	url(r'^gnew$', so.views.user_gnew),
	url(r'^gedit/(.+)/$', so.views.user_gedit),
	]