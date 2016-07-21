#!/usr/bin/python 
#coding:utf-8 
 
import json 
import zlib,os
import urllib2 
import requests
import datetime,time
from django.db.models import Q
from django.http import HttpResponse
#import plantform.models
from so.models import groups,hosts,relation,config,files,tasktable
from so.tasks import task_run,initsalt
from celery.result import AsyncResult
from so.models import userconf

global url 
global username
global password
global token

lists = userconf.objects.all()
for i in lists:
#     user =  i.zabbix_user
#     paooword = i.zabbix_pass
    salturl = i.salt_url
    username = i.salt_user
    password = i.salt_pass
    token = i.salt_token
#token = '2db128cbe8e5935305e80bb34d38399a341d6120'
#token = user_login()

# def __init__(self):
#     self.url = 'https://59.108.38.73:9990/' 
#     self.header = {"Content-Type":"application/json"}         
          
def user_login(username,password):
	url = salturl + '/login'
	data = {
                    "username": username,
					"password": password,
					"eauth": 'pam',
					}	
	headers = {
		#'Content-Type': 'application/x-www-form-urlencoded',
		'Accept':'application/json',
	}
	r = requests.post(url,data=data,verify=False)
	a = r.json()
	token = a['return'][0]['token']
	#print token
	return token
	#print r.text
	#print r.status_code
	## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb



	
def test():
	url = 'https://59.108.38.73:9990/login'
	header = {"Content-Type":"text/html"}
	data = json.dumps({
                    # "username": 'webui',
					# "password": 'webui',
					"username": username,
					"password": password,
					"eauth": 'auto',
					})
	request = urllib2.Request(url, data)
	
	for key in header:
		request.add_header(key, header[key])  
	try:
		result = urllib2.urlopen(request) 
		#print result.read()
		response = json.loads(result.read())
		result.close() 
		token = response['token']
		return token
	except urllib2.HTTPError as http_error:
		print zlib.decompress(http_error.read(), 30)
def remote_run(request):
	r = {}
	arguments = request.POST['arguments']
	model = request.POST['model']
	h = request.POST['host_post']
	g = request.POST['group_post']
	type = request.POST['type']
	if type == 'Group':
		gname = groups.objects.get(name=g)
		hs = gname.members.all()
		#print hs
		if model == 'test.ping':
			for h in hs:
				r.update(ping(h))
			print r.items()
			return r.items()
		elif model == 'cmd.run' or 'state.sls':
			for h in hs:
				r.update(cmd(h,model,arguments))
			return r.items()
		
	else:
		if model == 'test.ping':	
			r.update(ping(h))
			return r.items()
		elif model == 'cmd.run' or 'state.sls':
			r.update(cmd(h,model,arguments))
			return r.items()
		


def ping(host):
	
	url = salturl + '/run'
	data = {
                    "client": 'local',
					"tgt": host,
					"fun": 'test.ping',
					# "username": 'webui',
					# "password": 'webui',
					"username": username,
					"password": password,
					"eauth": 'pam',
					}		
	
	r = requests.post(url,data=data,verify=False)

	#print r.text
	a = r.json()
	result = a['return'][0]
	#print result
	return result ##.items()

	#print r.text
	#print r.status_code
	## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb

def cmd(host,model,arguments):
	url = salturl + '/run'
	data = {
                    "client": 'local',
					"tgt": host,
					"fun": model,
					# "username": 'webui',
					# "password": 'webui',
					"username": username,
					"password": password,
					"eauth": 'pam',
					"arg": arguments ,
					
					}	

	r = requests.post(url,data=data,verify=False)
	#print r.text
	a = r.json()
	result = a['return'][0]
	return result.items()
	#return r.text
	#print r.status_code
	## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb

def push_list():
	# url = 'https://59.108.38.73:9990/jobs'
	# token = user_login()
	
	# headers = {
		# #'Content-Type': 'application/x-www-form-urlencoded',
		# #'Accept':'application/x-yaml',
		# "X-Auth-Token": token,
	# }	
	# r = requests.get(url,verify=False, headers=headers)
	# #print r.text
	# #print r
	# a = r.json()
	# result = a['return'][0]
	# #print token
	# return result.items()
	
	# #print r.status_code
	# ## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb
	list = task.objects.all()
	#print list
	return list
def push_minions():
	url = salturl + '/minions'
	headers = {
		#'Content-Type': 'application/x-www-form-urlencoded',
		#'Accept':'application/x-yaml',
		"X-Auth-Token": token,
	}	
	data = {
                    "client": 'local',
					"tgt": '*',
					"fun": '*',
			}	
	r = requests.get(url,verify=False,headers=headers)
	#print r.text
	#print r
	a = r.json()
	result = a['return'][0]
	# for key,value in result.items():
		# print key
		# print value
		# print "+++++++++"
	return result
	
	#print r.status_code
	## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb

def push_detail(request,jobid):
	
	url = salturl + '/jobs/' + jobid
	token = user_login()
	headers = {
		#'Content-Type': 'application/x-www-form-urlencoded',
		'Accept':'application/x-yaml',
		"X-Auth-Token": token,
	}	
	r = requests.get(url,verify=False, headers=headers)
	return r.text
	#print "=========================" + url
	#a = r.json()
	#result = a['return'][0]
	#print a['info'][0]
	#print result
	#return result.items()
	
	#print r.status_code
	## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb
			

def hostinfo():
	list = hosts.objects.values_list('name','cpu','mem','ip','os','virt')
	return list
def device_group():
	list = hosts.objects.values_list('name','cpu','mem','ip','os','virt')
	return list
def addgroup(request):
		groupname = request.POST['groupname']
		addone = groups(name = groupname)
		addone.save()
def salt_hosts(request):
	data = []
	list = hosts.objects.all()
	for host in list:
		gname = []
		gname_tmp = []
		if host.relation_set.all():
			for h in host.relation_set.all():
				gname_tmp = h.groupname
				gname.append(gname_tmp)
		data_tmp = {'name':host.name,'ip':host.ip,'group':gname}
		data.append(data_tmp)
	return data
def salt_group(request):
	data = []
	list = groups.objects.values_list('name',flat=True)
	for gname in list:			
		ghost = groups.objects.get(name=gname)
		data_tmp = {'gname': gname,'hosts': ghost.members.all()}
		data.append(data_tmp)
	return data
def show_group():
	list = groups.objects.values_list('name',flat=True)
	return list

def group_del(groupname):
	gname = groups.objects.get(name=groupname)	
	gname.members.clear()
	gname.delete()
def host_del(hostname):
	rname = relation.objects.filter(hostname__name=hostname)
	hname = hosts.objects.get(name=hostname)
	#删除关系
	rname.delete()
	#删除host
	hname.delete()
	
def hosts_selected(groupname):
	selected_list = hosts.objects.filter(groups__name=groupname)
	#print list
	return selected_list
def hosts_unselected(groupname):
	unselected_list = hosts.objects.exclude(groups__name=groupname)
	#print list
	return unselected_list
def save_relation(request,gname):
	hosts_list = request.POST.getlist('host_selected')
	print "==========="
	print hosts_list
	print "==========="
	
	##清空group中的hosts
	gname = groups.objects.get(name=gname)
	gname.members.clear()
	for host in hosts_list:
		hname =  hosts.objects.get(name=host)
		r = relation(groupname=gname,hostname=hname)
		r.save()
	
def update_host(request):
	##从salt 获取hostname 和 ip 存入mysql，通过tet.ping 获取信息	
	arguments = ['cpu_model', 'mem_total', 'os', 'osrelease', 'osarch', 'virtual','ipv4']
	url = salturl + '/run'
	data = {
                    "client": 'local',
					"tgt": '*',
					"fun": 'grains.item',
					# "username": 'webui',
					# "password": 'webui',
					"username": username,
					"password": password,
					"eauth": 'pam',
					"arg": arguments ,
					
					}	

	r = requests.post(url,data=data,verify=False)
	#print r.text
	a = r.json()
	result = a['return'][0]
	#print result
	for key in result:
		name = key
		values = result[key]
		cpu = values['cpu_model']
		mem = values['mem_total']
		os = values['os'] + values['osrelease'] + '-' + values['osarch'] 
		virt = values['virtual']
		ip = ''
		for ips in values['ipv4']:
			if ips != '127.0.0.1':
				ip = ips + ' ' + ip
		ip = ip.strip()
		#print name +'####'+ ip
	###update to mysql
		try:
			oldone = hosts.objects.get(name=name)
			#print oldone.name
			if oldone.name == name:
				addone = hosts.objects.filter(name=name)
				addone.update(cpu=cpu,mem=mem,os=os,virt=virt,ip=ip)
		except:
			#print cpu
			addone = hosts(name=name,cpu=cpu,mem=mem,os=os,virt=virt,ip=ip)
			addone.save()
	#return result.items()
def files_sync():
	cmd = '/usr/bin/rsync -acv --port=9999 --password-file=/etc/rsyncd.pass --delete /srv/salt/ root@59.108.38.73::www '
	os.system(cmd)
	print "Rsync is OK!!"
def get_configs(name):
	if name == 'NULL':
		list = config.objects.all()
		#print list
		return list
	else:
		list = config.objects.get(confname=name)
		return list
def conf_del(name):
	try:
		fname = '/srv/salt/'+ name +'.sls'
		os.remove(fname)
		n = config.objects.get(confname=name)
		n.delete()
	except:
		n = config.objects.get(confname=name)
		n.delete()
def save_conf(request):
	cuser = request.session['name']
	cname = request.POST['configname']
	ctime = datetime.datetime.now()
	cdetail = request.POST['detail']
	# createtime = models.TimeField()
	# updatetime = models.TimeField(auto_now=True)
	# createuser = models.CharField(max_length=32)
	# detail = models.TextField()
	# print ctime
	if not config.objects.filter(confname=cname):
		c = config(confname=cname,createtime=ctime,createuser=cuser,detail=cdetail)
		# print c
		c.save()
		with open('/srv/salt/'+ cname +'.sls', 'w') as destination:	
			destination.write(cdetail)
		files_sync()
	else:
		n = config.objects.filter(confname=cname)
		# c = config(confname=cname,createtime=ctime,createuser=cuser,detail=cdetail)
		n.update(updatetime=ctime,createuser=cuser,detail=cdetail)
		with open('/srv/salt/'+ cname +'.sls', 'w') as destination:	
			destination.write(cdetail)
		files_sync()
		
def file_list():
	list = files.objects.all()
	#print list
	return list
def file_del(name):
	try:
		fname = '/srv/salt/files/'+ name
		os.remove(fname)
		n = files.objects.get(name=name)
		n.delete()
		files_sync()
	except:
		n = files.objects.get(name=name)
		n.delete()
		files_sync()
def save_file(request,f):
	fname = f.name
	cuser = request.session['name']
	ctime = datetime.datetime.now()
	#print files.objects.filter(name=fname).name
	if not files.objects.filter(name=fname):
		# print '22222'
		c = files(name=fname,createtime=ctime,createuser=cuser)
		# print c
		c.save()
		with open('/srv/salt/files/'+ f.name, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		files_sync()
	# else:
		# print '33333'

def task_list():
	# d = {}
	list = tasktable.objects.filter(Q(status='2') | Q(status='3'))
	# d.append(list['detail'])
	return list
def task_running(request):
	# d = {}
	list = tasktable.objects.exclude(Q(status='2') | Q(status='3'))
	for i in list:
		# print "88888888888888888888888"
		# print i.id
		id = str(i.id)
		i.status=request.session['width_'+ id]
		# print i.status
	# d.append(list['detail'])
	return list
def update_task1(taskid,t_detail):
	# tuser = request.session['name']
	# ttime = datetime.datetime.now()
	# ttype = request.POST['type']
	# tmodel = request.POST['model']
	# if request.POST['host_post'] != '':
		# thosts = request.POST['host_post']
	# else:
		# print "##########api task_save############"
		# tgroup = request.POST['group_post']
		# thosts = tgroup + '_G'
		# print thosts
	# targs = request.POST['arguments']
	# new = task(hosts=thosts,model=tmodel,status=0,result=0,args=targs,createtime=ttime,createuser=tuser)
	# new.save()
	# print "&&&&$$&$&$&$&$&$"
	# print t_detail
	one = tasktable.objects.filter(id=taskid)
	one.update(detail=t_detail)
  
def task_save(request):
	
	# hosts = models.CharField(max_length=32)
	# model = models.CharField(max_length=32)
	# args = models.CharField(max_length=128)
	# result = models.BooleanField()
	# detail = models.TextField()
	# createtime = models.DateTimeField()
	# createuser = models.CharField(max_length=32)
	tuser = request.session['name']
	ttime = datetime.datetime.now()
	ttype = request.POST['type']
	tmodel = request.POST['model']
	tgroup = request.POST['group_post']
	thosts = request.POST['host_post']
	targs = request.POST['arguments']
	if targs == "":
		targs = request.POST['passwd']
	if thosts == '':
		h = tgroup + '_G'
	else:
		h = thosts
#	print "**##**##***##*#*#*"
#	print h
	new = tasktable(hosts=h,model=tmodel,status=0,args=targs,createtime=ttime,createuser=tuser)
	new.save()
	##run task
	taskid = str(new.id)
	res = task_run.delay(targs,tmodel,thosts,tgroup,ttype,taskid)
	# res.delay(debug=True)
	uuid = res.id 
	one = tasktable.objects.filter(id=taskid)
	one.update(cuuid=uuid)
	##save session
	request.session['width_'+taskid] = '0'
	# print initsalt(h,targs)
	# print initsalt(h, targs)
	# print "#####task_save api##############"
	# print request.session['width_'+taskid]
		
def progress(taskid,st):
	one = tasktable.objects.get(id=taskid)
	if one.cuuid:
		job_id = str(one.cuuid)
		job_result = AsyncResult(job_id)
		print 'job_resultjob_resultjob_resultjob_result'
		print job_result
		job_data = job_result.state
		print "####api progress ####"
		# print job_id + 'idididididididi'
		print job_data
		one1 = tasktable.objects.filter(id=taskid)
		if job_data != st:
			if job_data == 'FAILURE': #PENDING SUCCESS STARTED
				one1.update(status=3)
			elif job_data == 'SUCCESS':
				one1.update(status=2)
			elif job_data == 'STARTED':
				one1.update(status=1)
			elif job_data == 'PENDING':
				one1.update(status=0)
	# print request.session['sp_'+taskid]
		return job_data
	else:
		return 'Faild'
		
# def user_new():
	







