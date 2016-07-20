#!/usr/bin/python 
#coding:utf-8 

import urllib2
import urllib	


def get_graps():
	url = 'http://59.108.38.73:9989/ganglia/?r=hour&cs=&ce=&c=hadoop&h=hadoop3&tab=m&vn=&hide-hf=false&m=load_one&sh=1&z=large&hc=4&host_regex=&max_graphs=0&s=by+name'
	request = urllib2.Request(url) 
	result = urllib2.urlopen(request)
	response = result.read()
	result.close()        
	return 1

def test():
	return "123456"
