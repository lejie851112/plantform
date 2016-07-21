#!/usr/bin/python 
#coding:utf-8 

from so.models import userconf
from zabbix_api import login
from salt_api import user_login
from django.core.urlresolvers import reverse

def showconf():
    lists = userconf.objects.all()
    print "#################"
    for i in lists:
        print i.zabbix_user
    return lists
def updateconf(request):
	# cuser = request.session['name']
	# cname = request.POST['configname']
	# ctime = datetime.datetime.now()
	# cdetail = request.POST['detail']
	# createtime = models.TimeField()
	# updatetime = models.TimeField(auto_now=True)
	# createuser = models.CharField(max_length=32)
	# detail = models.TextField()
	# print ctime
	# if not config.objects.filter(confname=cname):
	# 	c = config(confname=cname,createtime=ctime,createuser=cuser,detail=cdetail)
	# 	# print c
	# 	c.save()
	# 	with open('/srv/salt/'+ cname +'.sls', 'w') as destination:	
	# 		destination.write(cdetail)
	# 	files_sync()
	# else:
	# 	n = config.objects.filter(confname=cname)
	# 	# c = config(confname=cname,createtime=ctime,createuser=cuser,detail=cdetail)
	# 	n.update(updatetime=ctime,createuser=cuser,detail=cdetail)
	# 	with open('/srv/salt/'+ cname +'.sls', 'w') as destination:	
	# 		destination.write(cdetail)
	# 	files_sync()
	# # data = {'zauser':api.,'zapass':,'zaurl':,'salturl':,'saltuser':,'saltpass':,}
	# zabbix_url = models.CharField(max_length=128)
 #    zabbix_user = models.CharField(max_length=32)
 #    zabbix_pass = models.CharField(max_length=128)
 #    zabbix_token = models.CharField(max_length=128)
 #    salt_url = models.CharField(max_length=128)
 #    salt_user = models.CharField(max_length=32)
 #    salt_pass = models.CharField(max_length=128)
 #    salt_token = models.CharField(max_length=128)
    tzabbix_user = request.POST['zauser']
    tzabbix_pass = request.POST['zapass']
    tzabbix_url = request.POST['zaurl']
    tsalt_user = request.POST['saltuser']
    tsalt_pass = request.POST['saltpass']
    tsalt_url = request.POST['salturl']
    ttoken = login(tzabbix_user,tzabbix_pass,tzabbix_url)
    tsalt_token = user_login(tsalt_user,tsalt_pass)
    print tsalt_token
    lists = userconf.objects.all()
    for one in lists:
        one.delete()
    new = userconf(zabbix_user=tzabbix_user,zabbix_pass=tzabbix_pass,zabbix_url=tzabbix_url,salt_user=tsalt_user,salt_pass=tsalt_pass,salt_url=tsalt_url,zabbix_token=ttoken,salt_token=tsalt_token)
    new.save()
def require_role(role='user'):
    """
    decorator for require user role in ["super", "admin", "user"]
    要求用户是某种角色 ["super", "admin", "user"]的装饰器
    """

    def _deco(func):
        def __deco(request, *args, **kwargs):
            request.session['pre_url'] = request.path
            if not request.user.is_authenticated():
                return HttpResponseRedirect(reverse('/login'))
            if role == 'admin':
                # if request.session.get('role_id', 0) < 1:
                if request.user.role == 'CU':
                    return HttpResponseRedirect(reverse('index'))
            elif role == 'super':
                # if request.session.get('role_id', 0) < 2:
                if request.user.role in ['CU', 'GA']:
                    return HttpResponseRedirect(reverse('index'))
            return func(request, *args, **kwargs)

        return __deco

    return _deco
