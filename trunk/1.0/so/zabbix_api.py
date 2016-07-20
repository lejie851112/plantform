#!/usr/bin/python 
#coding:utf-8 
 
import json 
import urllib, urllib2, cookielib
import HTMLParser  
import urlparse   
import string  
import re  
from so.models import userconf

 
global url
global token

lists = userconf.objects.all()
for i in lists:
#     user =  i.zabbix_user
#     paooword = i.zabbix_pass
    url = i.zabbix_url
    token = i.zabbix_token
# def __init__(self):
#     self.url = 'http://59.108.38.73:9988/zabbix/api_jsonrpc.php' 
#     self.header = {"Content-Type":"application/json"}         

def tttt():
	print "aaaaaoooooa"

def login(name,password,url):
	# url = 'http://59.108.38.73:9988/zabbix/api_jsonrpc.php' 
	header = {"Content-Type":"application/json"} 
	data = json.dumps({
                    "jsonrpc": "2.0", 
                    "method": "user.login", 
                    "params": { 
                              # "user": request.POST['username'], 
                              # "password": request.POST['password'],
                              "user": name,
                              "password": password
                              }, 
                    "id": 1
					})
	# print data
	#cookie = cookielib.CookieJar() 
	#handler=urllib2.HTTPCookieProcessor(cookie)
	#opener = urllib2.build_opener(handler)
	
	#request = opener.open("http://www.baidu.com")
	#request = opener.open(url, data)
	request = urllib2.Request(url, data)
	for key in header:
		request.add_header(key, header[key])   
	#result = opener.open(request)
	#for item in cookie:
	#	print 'Name = '+item.name
	#	print 'Value = '+item.value
	#print result.header["Set-cookie"]
	result = urllib2.urlopen(request) 
	response = json.loads(result.read())	
	#print cookie
	#print request.read()	
	if 'error' in response:
		print response['error']['data']
		return "Failed"
	else:	
		token = response['result']
		return token	
		
def user_login():
	hosturl = 'http://59.108.38.73:9988/zabbix/index.php'
	posturl = 'http://59.108.38.73:9988/zabbix/index.php'
	###
	filename = '/tmp/cookie.txt'
	#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
	cj = cookielib.MozillaCookieJar(filename)
	#cj = cookielib.LWPCookieJar()  
	cookie_support = urllib2.HTTPCookieProcessor(cj)  
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)
	#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  	
	#opener.open(hosturl)  
	#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
	headers = {'Host':"59.108.38.73:9988",
				'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0",  
           		'Referer': "http://59.108.38.73:9988/zabbix/index.php",
           		'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           		'Accept-Language':"en-US,en;q=0.5",
           		'Accept-Encoding':"gzip, deflate",
           		'Connection':"keep-alive",
           		}  
	#构造Post数据，他也是从抓大的包里分析得出的。 
	postData = { 
            'name' : 'Admin', #//你的用户名  
            'password' : 'Sino2016#', #//你的密码，密码可能是明文传输也可能是密文，如果是密文需要调用相应的加密算法加密  
          	'autologin' : "1",
          	'enter' : "Sign+in",
          	'request':""
            }  
    #需要给Post数据编码  
	postData = urllib.urlencode(postData)  
	# print postData
  	#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
	request = urllib2.Request(posturl, postData, headers)  
	print "#####################"
	# print request  
	response = opener.open(request)
	cj.save(ignore_discard=True, ignore_expires=True)
	print "************************"  
	text = response.read()
	print text  
  	print "************************"
  	operate = opener.open('http://59.108.38.73:9988/zabbix/tr_status.php?ddreset=1')
  	print operate.read()
def get_hosts():
	#result2 = []
	#groups_name = 'Linux servers'
	# print "###get_host###"
	# url = "http://59.108.38.73:9988/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	data = json.dumps(
		{"jsonrpc": "2.0",
		"method": "host.get",
		
		"params": {
			"output": [
			"hostid",
			"host",
			"name",
			"status",
			"available",
			"lastaccess"
			],
			"selectGroups": ["groupid","name"],
			"filter": {
					"status": "0",
					
					},
			
			"selectInterfaces": [
			"interfaceid",
			"ip",

			],
		#"limit": "3",
		},
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
	)             
	request = urllib2.Request(url,data)
	for key in header:       
		request.add_header(key,header[key])
	result = urllib2.urlopen(request)
	response = json.loads(result.read())       
	result.close() 
	#print "ooooo" 
	print response['result']
	#for result_list in response['result']:
		# #print "aaaa"
		# #print result_list
		# for group in result_list['groups']:
			# if group['name'] == groups_name :
				# print "qqqq"
				# print group
				# result2.append(result_list)
				
				# continue
			# else:
				# print "pppp"
			
	return response['result']
	
def get_allhosts(request,groupid=''):
	#G_groups = request.POST['G_groups']
	# url = "http://59.108.38.73:9988/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	if groupid == 'None' or groupid == '':
		data = json.dumps(
		{"jsonrpc": "2.0",
		"method": "host.get",
		"params": {
			"output": [
			"hostid",
			"host",
			"name",
			
			],
			"expandData":"name",
            "sortfield": "name",
		},
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
	)
	else:
		data = json.dumps(
		{"jsonrpc": "2.0",
		"method": "host.get",
		"params": {
			"output": [
			"hostid",
			"host",
			"name",
		
			],
			"groupids": groupid,
			#"limit": "3",
			"expandData":"name",
            "sortfield": "name",
		},
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
		)             
	request = urllib2.Request(url,data)
	for key in header:       
		request.add_header(key,header[key])
	result = urllib2.urlopen(request)
	response = json.loads(result.read())       
	result.close() 
	#print "allhost######"
	#print response['result']
	return response['result']
		
	 
	
def get_groups(request):
	
	# url = "http://59.108.38.73:9988/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	data = json.dumps(
		{
		"jsonrpc": "2.0",
		"method": "hostgroup.get",
		"params": {
			"output":  ["groupid","name"],
			#"groupids": G_groups,
			#"limit": "3",
			"expandData":"name",
            "sortfield": "name",
		},		
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
	)             
	request = urllib2.Request(url,data)
	for key in header:       
		request.add_header(key,header[key])
	result = urllib2.urlopen(request)	
	response = json.loads(result.read())       
	result.close() 	
	#print request
	#print response['result']
	return response['result']
def get_group_id(request):
	
	# url = "http://59.108.38.73:9988/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	data = json.dumps(
		{
		"jsonrpc": "2.0",
		"method": "hostgroup.get",
		"params": {
			"output":  ["groupid","name"],
			#"groupids": G_groups,
			#"limit": "3",
		},		
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
	)             
	request = urllib2.Request(url,data)
	for key in header:       
		request.add_header(key,header[key])
	result = urllib2.urlopen(request)	
	response = json.loads(result.read())       
	result.close() 	
	#print request
	#print response['result']
	return response['result']
	
	
def get_alert():
	# url = "http://59.108.38.73:9988/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	alerts=[]
	data1 = json.dumps(
		{
		"jsonrpc": "2.0",
		"method": "event.get",
		"params": {
			"output": "extend",		
			"limit": "3",
			"filter":{
				"value": "1",
			}
		},		
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
	)	
	request1 = urllib2.Request(url,data1)
	for key in header:       
		request1.add_header(key,header[key])
	result1 = urllib2.urlopen(request1)
	response1 = json.loads(result1.read())       
	result1.close() 
	#print response1['result']
	for event in response1['result'] :
		data = json.dumps(
		{
		"jsonrpc": "2.0",
		"method": "alert.get",
		"params": {
			"output": ["eventid","clock","message"],
					
			"eventids": event['eventid'],

		},		
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
		) 
		#print data
		request = urllib2.Request(url,data)
		for key in header:       
			request.add_header(key,header[key])
		result = urllib2.urlopen(request)
		response = json.loads(result.read())       
		result.close()			
		alerts = alerts + response['result']
	#print 	alerts
	return alerts
	
	
def get_grapslist(request,hostid):
	#G_groups = request.POST['G_groups']
	#G_hosts = request.POST['G_hosts']
	#G_graphs = request.POST['G_graphs']
	#G_time = request.POST['G_time']
	#G_start = request.POST['G_start']
	#G_end = request.POST['G_end']
	# user_login()
	# url = "http://59.108.38.73:9988/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	data = json.dumps(
		{
		"jsonrpc": "2.0",
		"method": "graph.get",
		"params": {
			"output": ["graphid","name"],
			'hostids': hostid,
			#"limit": "3",
		},		
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
	)
	
	request = urllib2.Request(url,data)
	for key in header:       
		request.add_header(key,header[key])
	result = urllib2.urlopen(request)
	response = json.loads(result.read())       
	result.close() 
	#print response['result']
	return response['result']
	

def show_images(request,graphsid,stime,curtime,width,period):
	# #G_groups = request.POST['G_groups']
	# G_hosts = request.POST['G_hosts']
	# #G_graphs = request.POST['G_graphs']
	# G_time = request.POST['G_time']
	# G_start = request.POST['G_start']
	# G_end = request.POST['G_end']
	
	#graphsid = get_grapslist(request,G_hosts)
	url = "http://59.108.38.73:9988/zabbix/chart2.php?graphid="+ graphsid + "&period=" + str(period) + "&stime=" + str(stime) + "&width=" + width + "&curtime=" +str(curtime)
	#print url
	return url
def get_trigger():
	# url = "http://59.108.38.73:9988/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"trigger.get",
                           "params": {
										#"output": "extend",
										#"selectHosts": "extend",
                                      "output": [
                                                "triggerid",
                                                "description",
                                                "priority",
										
                                                ],
                                      "filter": {
                                                 "value": 1
                                                 },
                                      "expandData":"hostname",
                                      "sortfield": "hostname",
                                      "sortorder": "DESC"
                                    },	
		"id": 1,
		# "auth": "60f201a736cd7339c9840aa12a0d3a2a"
		"auth": token,
		}
	)             
	request = urllib2.Request(url,data)
	for key in header:       
		request.add_header(key,header[key])
	result = urllib2.urlopen(request)
	response = json.loads(result.read())       
	result.close() 
	#print response['result']
	return response['result']
	
# def make_graphs_list(request):
	# G_groups = request.POST['G_groups']
	# G_hosts = request.POST['G_hosts']
	# G_graphs = request.POST['G_graphs']
	# G_time = request.POST['G_time']
	# G_start = request.POST['G_start']
	# G_end = request.POST['G_end']
	
	# if G_groups != 'None': ## and G_hosts == 'None' and G_graphs == 'None':	
		# result['groups'] = get_groups(request)
		# result['allhosts'] = get_allhosts(request,G_groups)
		# result['grapslist'] = ''
	# elif G_hosts != 'None':
		# result['grapslist'] = get_grapslist(request,G_hosts)
	# elif G_graphs != 'None':
		# result['images_url'] = show_images(request)
		
	# return result
		
		
	
	

 