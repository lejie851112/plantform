#coding:utf-8 
from django.db import models
from django.contrib.auth.models import AbstractUser

class hosts(models.Model):
    #print "==hosts==="
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    ip = models.CharField(max_length=64) 
    os = models.CharField(max_length=32) 
    cpu = models.CharField(max_length=64) 
    mem = models.CharField(max_length=32) 
    virt= models.CharField(max_length=32) 

class groups(models.Model):
    #print "==groups==="
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    members = models.ManyToManyField(hosts, through='relation')

class relation(models.Model):
    #print "==relation==="
    groupname = models.ForeignKey(groups, on_delete=models.CASCADE)
    hostname = models.ForeignKey(hosts, on_delete=models.CASCADE)
###配置和文件的关系
class files(models.Model):
    name = models.CharField(max_length=32)
    createuser = models.CharField(max_length=32)
    createtime = models.DateTimeField()
class config(models.Model):
    confname = models.CharField(max_length=32)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)
    createuser = models.CharField(max_length=32)
    detail = models.TextField()
class tasktable(models.Model):
    # TASK_ST = (
    # ('',''),
    # (),
    # ()
            # # if job_data == 'FAILURE': #PENDING SUCCESS STARTED
            # # one1.update(status=3)
        # # elif job_data == 'SUCCESS':
            # # one1.update(status=2)
        # # elif job_data == 'STARTED':
            # # one1.update(status=1)
        # # elif job_data == 'PENDING':
            # # one1.update(status=0)
    # )
    hosts = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    args = models.CharField(max_length=128)
    #result = models.BooleanField()   ## result: 0 is true,1 is false
    detail = models.TextField()
    status = models.CharField(max_length=32) ## 0 peding;1 run;2 success;3 faild
    createtime = models.DateTimeField()
    createuser = models.CharField(max_length=32)
    cuuid = models.CharField(max_length=128)
class userconf(models.Model):
    zabbix_url = models.CharField(max_length=128)
    zabbix_user = models.CharField(max_length=32)
    zabbix_pass = models.CharField(max_length=128)
    zabbix_token = models.CharField(max_length=128)
    salt_url = models.CharField(max_length=128)
    salt_user = models.CharField(max_length=32)
    salt_pass = models.CharField(max_length=128)
    salt_token = models.CharField(max_length=128)
#资产 
class devices(models.Model):
    hostname = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    #ssh
    sshport = models.CharField(max_length=32)
    sshuser = models.CharField(max_length=32)
    sshpass = models.CharField(max_length=32)
    #虚拟化
    hyper = models.CharField(max_length=32) #vimware xen hyper-v kvm  none
    #
    disk = models.CharField(max_length=32)
    partion = models.CharField(max_length=128)
    mem = models.CharField(max_length=32)
    cputype = models.CharField(max_length=128)
    cpunum = models.CharField(max_length=32)
    os = models.CharField(max_length=128)
    #
    description = models.CharField(max_length=128)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)
    #
    devsn = models.CharField(max_length=32)
    compsn = models.CharField(max_length=32)
    remotecard = models.CharField(max_length=128)
    remoteaddr = models.CharField(max_length=32)
    remoteuser = models.CharField(max_length=32)
    remotepass = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    #
    racknum = models.CharField(max_length=32)
    linenum = models.CharField(max_length=32)
    #
    # didc = models.ForeignKey(idc)
    # dgroup = models.ManyToManyField(devgroup)

#资产组
class devgroup(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    device = models.ManyToManyField(devices, through='devtogroup')
   
#IDC
class idc(models.Model):
    idcname = models.CharField(max_length=32)
    contantname = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)
    device = models.ManyToManyField(devices, through='devtoidc')

#资产和组关系
class devtogroup(models.Model):
    dname = models.ForeignKey(devices, on_delete=models.CASCADE)
    iname = models.ForeignKey(devgroup, on_delete=models.CASCADE)
#资产和IDC关系
class devtoidc(models.Model):
    #print "==relation==="
    dname = models.ForeignKey(devices, on_delete=models.CASCADE)
    iname = models.ForeignKey(idc, on_delete=models.CASCADE)
