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
    info = []
    idcs = idc.objects.all()
    for i in idcs:
        tmp = {}
        tmp1 = []
        t_data = idc.objects.get(id=i.id)
        for n in t_data.device.all():
            tmp1.append(n.hostname)
        tmp = {'info':i,'hostname': len(tmp1)}
        info.append(tmp)
    return info
    
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
    gs = []
    grps = devgroup.objects.all()
    for g in grps:
        h = []
        tmp = {}
        g_member = devgroup.objects.get(name=g.name)
        for m in g_member.device.all():
            h.append(str(m.hostname))
        # print h
        tmp = {'id': g.id,'name': g.name,'host': len(h),'description': g.description}
        gs.append(tmp)
     
    return gs

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
    data = []

    for info in devices.objects.all():
        tmp = {}
        gname = []
        iname =[]
        for g in info.devtogroup_set.all():
            gname.append(g.iname.name)
        for i in info.devtoidc_set.all():
            iname.append(i.iname.idcname)
        tmp = {'info': info,'group': gname,'idc': iname}
        data.append(tmp)
    return data
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
        g = devgroup.objects.get(name=devgrp)
        i = idc.objects.get(idcname=devidc)
        devtogroup(iname=g,dname=dev).save()
        devtoidc(iname=i,dname=dev).save()
def device_edit(devid):
    info = devices.objects.get(id=devid)
    for g in info.devtogroup_set.all():
        gname = g.iname.name
    for i in info.devtoidc_set.all():
        iname = i.iname.idcname
    data = {'info': info,'group': gname,'idc': iname}
    return data

def device_update(request,devid):
    hostname = request.POST['name']
    ip = request.POST['ip']
    sshport = request.POST['sshport']
    sshuser = request.POST['sshuser']
    sshpass = request.POST['sshpass']
    description = request.POST['description']
    # devgrp = request.POST['dev_grp']
    # devidc = request.POST['dev_idc']
    # ctime = datetime.datetime.now()
    
    sql = devices.objects.filter(id=devid)
    sql.update(\
        hostname=hostname,\
        ip=ip,\
        sshport=sshport,\
        sshuser=sshuser,\
        sshpass=sshpass,\
        description=description,\
        cpunum=request.POST['cpunum'],\
        mem=request.POST['mem'],\
        os=request.POST['os'],\
        hyper=request.POST['hyper'],\
        disk=request.POST['disk'],\
        partion=request.POST['partion'],\
        remotecard=request.POST['remotecard'],\
        remoteaddr=request.POST['remoteaddr'],\
        remoteuser=request.POST['remoteuser'],\
        remotepass=request.POST['remotepass'],\

        )
        # sql.save()
        # dev = devices.objects.get(hostname=hostname)

        # devgroup(name=devgrp,device=dev).save()
        # idc(idcname=devidc,device=dev).save()

def device_del(request):
    devid = request.GET.get('id', '')

    if devid:
        g = devtogroup.objects.filter(dname__id=devid)
        i = devtoidc.objects.filter(dname__id=devid)
        d = devices.objects.get(id=devid)  
        #
        g.delete()
        i.delete()
        d.delete()
    if request.method == 'POST':
        asset_id_all = str(request.POST.get('asset_id_all', ''))
        for devid in asset_id_all.split(','):
            g = devtogroup.objects.filter(dname__id=devid)
            i = devtoidc.objects.filter(dname__id=devid)
            d = devices.objects.get(id=devid)  
            #
            g.delete()
            i.delete()
            d.delete()

# def device_detail():
    
