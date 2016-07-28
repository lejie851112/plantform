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

def grpinfo():

def grpdel():

def grpupdate():


