#!/usr/bin/python2.7 
#coding:utf-8 

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
import json,time,datetime
import urllib2,cookielib,urllib
import requests,datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import zabbix_api	
import ganglia_api
import salt_api
import api,device_api
from so.forms import file_form,LoginForm
import user_manage

def user_login(request):
		# try:
		# 		if request.POST['username'] and request.POST['password']:				
		# 			result = zabbix_api.login(request)				
		# 			if result == 'Failed':
		# 				return render_to_response('login.html',{'status':'用户名或密码错误'},context_instance=RequestContext(request))
		# 			else:
		# 				request.session['name'] = request.POST['username']
		# 				request.session['login'] = 'True'
		# 				request.session['token'] = result
		# 				#print result
		# 				return HttpResponseRedirect('/index')				
		# 		else:
		# 			return render_to_response('login.html',{'status':'用户名或密码不能为空'},context_instance=RequestContext(request))
		# except:
		# 	return render_to_response('login.html',context_instance=RequestContext(request))	  
    error = ''
    if request.user.is_authenticated():
    	# return HttpResponseRedirect(request.session.get('pre_url', '/'))
    	# zabbix_api.user_login()
        return HttpResponseRedirect('/index')
    if request.method == 'GET':
    	# print "login****get"
        return render_to_response('login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['name'] = username
                    # print request.session['name']
                    # return HttpResponseRedirect('/index')
                    # c = {}
                    # c.update(csrf(request))
                    # request.session['csrf_token'] = str(c.get('csrf_token'))
        # user_filter = User.objects.filter(username=username)
        # if user_filter:
        #     user = user_filter[0]
        #     if PyCrypt.md5_crypt(password) == user.password:
                    # request.session['name'] = username
        #         user_filter.update(last_login=datetime.datetime.now())
                    # if user.role == 'SU':
                    #     request.session['role_id'] = 2
                    # elif user.role == 'GA':
                    #     request.session['role_id'] = 1
                    # else:
                    #     request.session['role_id'] = 0
                    # return HttpResponseRedirect(request.session.get('pre_url', '/'))
                    zabbix_api.user_login()
                    return HttpResponseRedirect('/')
                # response.set_cookie('username', username, expires=604800)
                # response.set_cookie('seed', PyCrypt.md5_crypt(password), expires=604800)
                # return response
                else:
                    error = '用户未激活'
            else:
                error = '用户名或密码错误'
        else:
            error = '用户名或密码错误'
    	return render_to_response('login.html', {'error': error})

def session_check(request,html,data):
	# try:
			uname = request.session['name']
		# status = request.session['login']
		# token = request.session['token']
		# #print name  + token
		# #print RequestContext(request)
		# if status == 'True' and token != '' :
			data['name'] = uname	
			data['suser'] = user_manage.userrole(uname)	
			# print data
			#print html
			# return render_to_response(html,data,context_instance=RequestContext(request))
			return render_to_response(html,data,context_instance=RequestContext(request))
			#return render_to_response(html,data)
		# else:
			#print "11111" 
			# return HttpResponseRedirect('/login')
			
	# except:
		# print "2222222"
		# return HttpResponseRedirect('/login')
		
def user_logout(request):
	logout(request)
	# try:
	# 	del request.session['name']
	# 	return HttpResponseRedirect('/login')
	# except:
	return HttpResponseRedirect('/login')

@login_required(login_url='/login/')
def index(request):

	host_vm = []
	host_py = []
	alert3 = []
	task3 = []
	vm3 = []
	py3 = []
	zabbix_alert = zabbix_api.get_trigger()
	tasks_run = salt_api.task_running(request)
	device_all = salt_api.hostinfo()
	for host in device_all:
		if 'VMware' in host:
			host_vm.append(host)
		elif 'physical' in host:
			host_py.append(host)
	data = {'alert_total': len(zabbix_alert),
			'task_run_total': len(tasks_run),
			'vm_total': len(host_vm),
			'py_total': len(host_py),
			'zabbix_alert': zabbix_alert[0:3],
			'tasks_run': tasks_run[0:3],
			'host_vm': host_vm[0:3],
			'host_py': host_py[0:3],
			'times': datetime.datetime.now(),
			# 'name': request.session['name'],
			}
	html = 'index.html'	
	return session_check(request,html,data)

def zabbix_host(request):
	# hostdata = []
	# HostGroup = 'Linux servers'  ###Just List the group
	data_tmp = zabbix_api.get_hosts()
	# print data_tmp
	# for hostlist in  data_tmp:
	# 	for groupslist in hostlist['groups']:
	# 		if groupslist['name'] == HostGroup:
	# 			hostdata.append(hostlist)
	data = {'zabbix_host': data_tmp}
	html = 'zabbix_host.html'
	return session_check(request,html,data)
	#return render_to_response('zabbix_host.html',{'zabbix_host': zabbix_api.get_hosts()})
@login_required(login_url='/login/')	
def ganglia(request):
	return render_to_response('ganglia.html',{'ganglia_graps': ganglia_api.get_graps()})

@login_required(login_url='/login/')	
def device(request):
	data = {'device': zabbix_api.get_hosts()}
	html = 'device.html'
	return session_check(request,html,data)
	#return render_to_response('device.html',{'device': zabbix_api.get_hosts()})

@login_required(login_url='/login/')	
def zabbix_alert(request):
	data = {'zabbix_alert': zabbix_api.get_trigger()}
	html = 'zabbix_alert.html'
	return session_check(request,html,data)

@login_required(login_url='/login/')	
def zabbix_graps(request):
	# try:
		# G_group = request.POST['G_groups']
		# G_hosts = request.POST['G_hosts']
		# G_graphs = request.POST['G_graphs']
		# G_time = request.POST['G_time']
		# G_start = request.POST['G_start']
		# G_end = request.POST['G_end']
	# except:
	if request.method == 'POST':
		G_groups = request.POST['G_groups']
		G_hosts = request.POST['G_hosts']
		G_graphs = request.POST['G_graphs']
		G_time = request.POST['G_time']
		G_start = request.POST['G_start']
		G_end = request.POST['G_end']
		day = 3600 * 24
		T_now = datetime.datetime.now()
		#print T_now
		curtime = int(time.mktime(T_now.timetuple()))
		if G_time == 'T_today':
			period = day #1 day
			T_today = datetime.date.today()
			T_start = T_today.strftime('%Y%m%d%H%M%S') 
			G_start = ''
			G_end = ''			
			#T_end = T_now.strftime('%Y%m%d%H%M%S')
			#print '日期时间%%c: %s ' % T_today.strftime('%Y%m%d%H%M%S') 
			#print period
			#print '日期时间%%c: %s ' % T_now.strftime('%Y%m%d%H%M%S') 
		if G_time == 'T_yestoday':
			period = day #1 day
			T_yestoday = datetime.date.today() - datetime.timedelta(days=1) 
			T_start = T_yestoday.strftime('%Y%m%d%H%M%S') 
			G_start = ''
			G_end = ''			
		if G_time == 'T_week':
			period = day*7 
			T_week = datetime.date.today() - datetime.timedelta(days=7) 
			T_start = T_week.strftime('%Y%m%d%H%M%S') 
			G_start = ''
			G_end = ''
		if G_time == 'T_month':
			period = day*30
			T_month = datetime.date.today() - datetime.timedelta(days=30) 
			T_start = T_month.strftime('%Y%m%d%H%M%S') 
			G_start = ''
			G_end = ''
		if G_time == 'T_diy' :
			if  G_start and G_end:
				T_start1 = time.strptime(G_start,"%Y-%m-%d %H:%M")
				T_end1 = time.strptime(G_end,"%Y-%m-%d %H:%M")
				T_start = datetime.datetime(* T_start1[:6])
				T_end = datetime.datetime(* T_end1[:6])
				# print T_start1
				# print T_end1
				# print T_start
				# print T_end
				period_H = (T_end - T_start).days
				period_S = (T_end - T_start).seconds
				period = period_H * day + period_S
				# print period_H
				# print period
			else:
				G_start = ''
				G_end = ''
				T_start = ''
				period = day
		
		if G_groups != 'None' and G_hosts == 'None' and G_graphs == 'None': 
			#print " G_groups != 'None': "
			data = {'get_groups': zabbix_api.get_groups(request),
			'get_hosts': zabbix_api.get_allhosts(request,G_groups),
			'get_grapslist': '',
			'G_groups': G_groups,
			'G_hosts': G_hosts,
			'G_graphs': G_graphs,
			'G_time': G_time,
			'G_start': G_start,
			'G_end': G_end,
			'count': '1',
			'show_images': '', 
			}
		elif G_groups != 'None' and G_hosts != 'None' and G_graphs == 'None' or (G_groups == 'None' and G_hosts != 'None' and G_graphs == 'None'): 
			img_urls = []
			#print "G_hosts != 'None' and G_graphs == 'None':"
			#print "######" +G_groups
			get_grapslist = zabbix_api.get_grapslist(request,G_hosts)
			#print get_grapslist
			for graps in get_grapslist:
				id = graps['graphid']
				name = graps['name']
				url = zabbix_api.show_images(request,graphsid=id,stime=T_start,curtime=curtime,width='800',period=period)
				img_urls.append(url)
			#print "img_urls" 
			#print img_urls
			data = {'get_groups': zabbix_api.get_groups(request),
			'get_hosts': zabbix_api.get_allhosts(request,G_groups),
			'get_grapslist': get_grapslist,
			'G_groups': G_groups,
			'G_hosts': G_hosts,
			'G_graphs': G_graphs,
			'G_time': G_time,
			'G_start': G_start,
			'G_end': G_end,
			'count': '2',
			'show_images': img_urls, 
			}
		elif G_groups != 'None' and G_hosts != 'None' and G_graphs != 'None' or (G_groups == 'None' and G_hosts != 'None' and G_graphs != 'None'): 
			#print "G_hosts != 'None' and G_graphs != 'None': ## or G_graphs != 'None':"
			data = {'get_groups': zabbix_api.get_groups(request),
			'get_hosts': zabbix_api.get_allhosts(request,G_groups),
			'get_grapslist': zabbix_api.get_grapslist(request,G_hosts),
			'G_groups': G_groups,
			'G_hosts': G_hosts,
			'G_graphs': G_graphs,
			'G_time': G_time,
			'G_start': G_start,
			'G_end': G_end,
			'count': '1',
			'show_images': zabbix_api.show_images(request,graphsid=G_graphs,stime=T_start,curtime=curtime,width='1000',period=period),
			
			}
		else:
			data = {'get_groups': zabbix_api.get_groups(request),
			'get_hosts': zabbix_api.get_allhosts(request,G_groups),
			'get_grapslist': '' ,##zabbix_api.get_grapslist(request),
			'G_groups': G_groups,
			'G_hosts': G_hosts,
			'G_graphs': G_graphs,
			'G_time': G_time,
			'G_start': G_start,
			'G_end': G_end,
			'count': '1',
			'show_images': '', ## zabbix_api.show_images(request),
			}
		
		html = 'zabbix_graps.html'
		return session_check(request,html,data)
		
		##render_to_response('zabbix_graps.html',{'zabbix_graps': zabbix_api.get_graps()})
	else:
		
		data = {
			'get_groups': zabbix_api.get_groups(request),
			'get_hosts': zabbix_api.get_allhosts(request,''),
			#'get_grapslist': zabbix_api.get_grapslist,
			}
		html = 'zabbix_graps.html'
		return session_check(request,html,data)
		#return render_to_response('zabbix_graps.html',context_instance=RequestContext(request))

#def show_images(request):
#	data = {'show_images': zabbix_api.show_images(request)}
#	html = 'show_images.html'
	#return session_check(request,html,data)
#	return render_to_response(html,data)
	
@login_required(login_url='/login/')	
def edit(request):
	data = {'configs':salt_api.get_configs('NULL')}
	html = 'edit.html'
	return session_check(request,html,data)
	#return render_to_response('edit.html')

@login_required(login_url='/login/')
def salt_group(request):
	if request.method == 'POST':
		
		salt_api.addgroup(request)
		return HttpResponseRedirect('/salt_group')
	else:
		data = {'groupname': salt_api.salt_group(request)}
		html = 'salt_group.html'
		return session_check(request,html,data)
	#return render_to_response('salt_group.html')

@login_required(login_url='/login/')
def salt_hosts(request):
	data = {'salt_hosts': salt_api.salt_hosts(request)}
	#print data
	html = 'salt_hosts.html'
	return session_check(request,html,data)
	#return render_to_response('salt_hosts.html',{'salt_hosts': salt_api.get_event(request)})
	#return render_to_response('salt_hosts.html',{'salt_hosts': salt_api.get_event(request)})

@login_required(login_url='/login/')
def group_edit(request,name):
	if request.method == 'POST':
		salt_api.save_relation(request,name)
		return HttpResponseRedirect('/salt_group')
	else:
		groupname = name
		hosts_selected = salt_api.hosts_selected(groupname)
		hosts_unselected = salt_api.hosts_unselected(groupname)
		data = {'groupname': groupname,'hosts_selected':hosts_selected,'hosts_unselected': hosts_unselected}
		html = 'group_edit.html'
		return session_check(request,html,data)
	
@login_required(login_url='/login/')		
def group_del(request,name):
	salt_api.group_del(name)
	return HttpResponseRedirect('/salt_group')	

@login_required(login_url='/login/')
def host_del(request,name):
	salt_api.host_del(name)
	return HttpResponseRedirect('/salt_hosts')	

@login_required(login_url='/login/')
def users(request):
	data = {}
	html = 'users.html'
	return session_check(request,html,data)
	#return render_to_response('user.html')
@login_required(login_url='/login/')
def new_config(request):
	if request.method == 'POST':
		salt_api.save_conf(request)
		return HttpResponseRedirect('/edit')
	else:
		data = {'file_input': file_form()}
		html = 'new_config.html'
		return session_check(request,html,data)
		#return render_to_response('new_config.html')
@login_required(login_url='/login/')		
def conf_edit(request,name):
	# if request.method == 'POST':
		data = {'conf':salt_api.get_configs(name)}
		html = 'conf_edit.html'
		return session_check(request,html,data)
	# else:
		# return HttpResponseRedirect('/edit')
@login_required(login_url='/login/')
def conf_del(request,name):
	salt_api.conf_del(name)
	return HttpResponseRedirect('/edit')
@login_required(login_url='/login/')		
def new_task(request):
	if request.method == 'POST':
		salt_api.save_conf(request)
		return HttpResponseRedirect('/edit')
	else:
		data = {}
		html = 'new_task.html'
		return session_check(request,html,data)
		#return render_to_response('new_task.html')


@login_required(login_url='/login/')
def remote(request):
	if request.method == 'POST':
		data = {'remote_run': salt_api.remote_run(request),'groups': salt_api.show_group()}
		html = 'remote.html'
		return session_check(request,html,data)
	else:
		data = {'groups': salt_api.show_group()}
		html = 'remote.html'
		return session_check(request,html,data)
	#return render_to_response('remote.html',{'remote_run': salt_api.remote_run(request)})

@login_required(login_url='/login/')		
def push(request):
	data = {'tasks': salt_api.task_running(request),'groups': salt_api.show_group()}
	html = 'push.html'
	return session_check(request,html,data)
def task_save(request):
	if request.method == 'POST':
		salt_api.task_save(request)
	return HttpResponseRedirect('/push')

@login_required(login_url='/login/')
def push_list(request):
	data = {'tasks': salt_api.task_list()}
	html = 'push_list.html'
	return session_check(request,html,data)
	#return render_to_response('push_list.html',{'push_list': salt_api.push_list(request)})
def push_detail(request,jobid):
	data = {'push_detail': salt_api.push_detail(request,jobid)}
	html = 'push_detail.html'
	return session_check(request,html,data)
	#return render_to_response('push_detail.html',{'push_detail': salt_api.push_detail(request,jobid)})
@login_required(login_url='/login/')	
def hostinfo(request):
	data = {'device': salt_api.hostinfo()}
	html = 'device.html'
	return session_check(request,html,data)

	#return render_to_response('push_detail.html',{'push_detail': salt_api.push_detail(request,jobid)})
def update_host(request):
	salt_api.update_host(request)
	return HttpResponseRedirect('/salt_hosts')
def update_device(request):
	salt_api.update_host(request)
	return HttpResponseRedirect('/device')
def file_list(request):
	data = {'file_list': salt_api.file_list(),'file_input': file_form()}
	html = 'file_list.html'
	return session_check(request,html,data)

@login_required(login_url='/login/')
def file_del(request,name):
	salt_api.file_del(name)
	return HttpResponseRedirect('/file_list')

@login_required(login_url='/login/')
def uploadfile(request):
	if request.method == 'POST':
			form = file_form(request.POST, request.FILES)
		
			print '1111111'
			print request.FILES['file'].name
			salt_api.save_file(request,request.FILES['file'])
			return HttpResponseRedirect('/file_list')
		
	else:
		return HttpResponseRedirect('/file_list')
@login_required(login_url='/login/')
def progress(request,id,width=0,st='PENDING'):
	# if request.method == 'get':
		# t_id = request.POST['id']
		# print "####view#####"+id
		if width == 100:
			del request.session['width_'+id]
		else:
			request.session['width_'+id] = width
		
			# print "#######--width--#######"+width
			# print request.session['width_'+id]
		# data = {'status':salt_api.progress(id),'pwidth': request.session['width_'+id]}
		data = salt_api.progress(id,st)
		return HttpResponse(json.dumps(data))

@login_required(login_url='/login/')
def sysconf(request):
    if request.method == 'POST':
    	# print "######post#####"
        api.updateconf(request)
        return HttpResponseRedirect('/sysconf')
    else:
    	# data = {'conf':api.showconf()}
        # html = 'sysconf.html'
        # print "######get#####"
        # data = {'zauser':api.,'zapass':,'zaurl':,'salturl':,'saltuser':,'saltpass':,}
        data = {'config':api.showconf()}
        html = 'sysconf.html'
        print data 
        return session_check(request,html,data)

def user_new(request):
    if request.method == 'POST':
    	username = request.POST['username'] 
    	password = request.POST['password'] 
    	user_manage.createuser(username,password)
        return HttpResponseRedirect('/user/userlist')
    else:
        data = {}
        html = 'user_new.html'
        print data 
        return session_check(request,html,data)
@login_required(login_url='/login/')
def user_ulist(request):
    # if request.method == 'POST':
    # 	# print "######post#####"
    # 	data = {'ulist':user_manage.userlist()}
    #     return HttpResponseRedirect('/user/userlist')
    # else:
        data = {'ulist':user_manage.userlist()}
        html = 'users.html'
        # print data 
        return session_check(request,html,data) 
def user_edit(request,uid):
    if request.method == 'POST':
    	# username = request.POST['username'] 
    	password = request.POST['password']
    	user_manage.useredit(password,uid)
        return HttpResponseRedirect('/user/userlist')
    else:
        data = {'udetail':user_manage.userdetail(uid)}
        html = 'user_edit.html'
        return session_check(request,html,data) 
@login_required(login_url='/login/')
def user_glist(request):
    # if request.method == 'POST':
    #     return HttpResponseRedirect('/user/grouplist')
    # else:
        # data = {}
        data = {'glist':user_manage.grouplist()}
        html = 'user_group.html'
        # print data 
        return session_check(request,html,data)  
def user_del(request,uname):
	user_manage.userdel(uname)
	return HttpResponseRedirect('/user/userlist')
def user_gnew(request):
    if request.method == 'POST':
    	gname = request.POST['name'] 
    	user_manage.creategroup(gname)
        return HttpResponseRedirect('/user/grouplist')
    else:
        data = {}
        html = 'user_gnew.html'
        print data 
        return session_check(request,html,data) 
def user_gdel(request,gname):
	user_manage.groupdel(gname)
	return HttpResponseRedirect('/user/grouplist')
def user_gedit(request,id):
    # data = {'gdetail':user_manage.groupedit()}
    # html = 'user_group.html'
    # # print data 
    # return session_check(request,html,data)
    if request.method == 'POST':
    	gname = request.POST['gname'] 
    	user_manage.groupedit(id,gname)
        return HttpResponseRedirect('/user/grouplist')
    else:
        data = {'gdetail':user_manage.groupdetail(id)}
        html = 'user_gedit.html'
        # print data 
        return session_check(request,html,data)
	
@login_required(login_url='/login/')		
def idc(request):
	if request.method == 'POST':
		#保存IDC
		device_api.saveidc(request)
		return HttpResponseRedirect('/idc')
	else:
		data = {'idcs':device_api.showidc()}
		html = 'idc.html'
		return session_check(request,html,data)
def device_group(request):
	if request.method == 'POST':
		#保存新建IDC
		iname = request.POST['iname'] 
		device_api.saveidc(iname)
		return HttpResponseRedirect('/idc')
	else:
		data = {'idcs':device_api.showidc()}
		html = 'idc.html'
		return session_check(request,html,data)