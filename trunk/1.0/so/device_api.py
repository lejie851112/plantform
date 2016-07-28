#!/usr/bin/python 
#coding:utf-8 

import datetime,time
from so.models import *

#about idc
def saveidc(request):
    idcname = request.POST['idcname'] 
    contantname = request.POST['contantname'] 
    mobile = request.POST['mobile']
    phone = request.POST['phone']
    email = request.POST['email']
    address = request.POST['address']
    description = request.POST['description']
    ctime = datetime.datetime.now()
    if not idc.objects.filter(idcname=idcname):
        sql = idc(idcname=idcname,contantname=contantname,mobile=mobile,phone=phone,email=email,address=address,description=description,createtime=ctime)
        sql.save()
def showidc():
    idcs = idc.objects.all()
    return idcs
def idcinfo(idcid):
    idcs = idc.objects.get(id=idcid)
    return idcs
def idcdel(idcid):
    i = idc.objects.get(id=idcid)  
    i.device.clear()
    i.delete()
def updateidc(request,idcid):
    uidcname = request.POST['idcname'] 
    ucontantname = request.POST['contantname'] 
    umobile = request.POST['mobile']
    uphone = request.POST['phone']
    uemail = request.POST['email']
    uaddress = request.POST['address']
    udescription = request.POST['description']
    old = idc.objects.filter(id=idcid)
    old.update(idcname=uidcname,contantname=ucontantname,mobile=umobile,phone=uphone,email=uemail,address=uaddress,description=udescription)
#about dev group
def savegrp(request):
    name = request.POST['groupname'] 
    description = request.POST['description']
    
    if not devgroup.objects.filter(name=name):
        sql = devgroup(name=name,description=description)
        sql.save()

def showgrp():
    grps = devgroup.objects.all()
    return grps

def grpinfo(gid):
    grps = devgroup.objects.get(id=gid)
    return grps
def grpdel(gid):
    i = devgroup.objects.get(id=gid)  
    i.device.clear()
    i.delete()
def grpupdate(request,gid):
    name = request.POST['name'] 
    description = request.POST['description']
    grps = devgroup.objects.filter(id=gid)
    grps.update(name=name,description=description)

#about device
def showdev():
    devs = devices.objects.all()
    # relation_set.all()
    return devs
def device_add(request):
    hostname = request.POST['name']
    ip = request.POST['ip']
    sshport = request.POST['sshport']
    sshuser = request.POST['sshuser']
    sshpass = request.POST['sshpass']
    description = request.POST['description']
    devgrp = request.POST['dev_grp']
    devidc = request.POST['dev_idc']
    ctime = datetime.datetime.now()
    
    if not devices.objects.filter(hostname=hostname):
        sql = devices(hostname=hostname,ip=ip,sshport=sshport,sshuser=sshuser,sshpass=sshpass,createtime=ctime,description=description)
        sql.save()
        dev = devices.objects.get(hostname=hostname)

        devgroup(name=devgrp,device=dev).save()
        idc(idcname=devidc,device=dev).save()




