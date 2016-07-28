#!/usr/bin/python 
#coding:utf-8 

import datetime,time
from so.models import devices,idc,devtoidc,devtogroup


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
    idcs = idc.objects.filter(id=idcid)
    return idcs
def idc_del(idcid):
    i = idc.objects.get(id=idcid)  
    i.device.clear()
    i.delete()
def updateidc(request,idcid):
    idcname = request.POST['idcname'] 
    contantname = request.POST['contantname'] 
    mobile = request.POST['mobile']
    phone = request.POST['phone']
    email = request.POST['email']
    address = request.POST['address']
    description = request.POST['description']
    old = idc.objects.get(id=idcid)
    old.update(idcname=idcname,contantname=contantname,mobile=mobile,phone=phone,email=email,address=address,description=description)
    
