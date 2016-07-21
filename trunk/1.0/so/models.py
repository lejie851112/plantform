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
    def __str__(self):
        return self.name
class groups(models.Model):
    #print "==groups==="
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    members = models.ManyToManyField(hosts, through='relation')
    def __str__(self):
        return self.name
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

class devices(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name
class idc(models.Model):
    name = models.CharField(max_length=32)
    device = models.ManyToManyField(devices, through='devtoidc')
    def __str__(self):
        return self.name
class devtoidc(models.Model):
    #print "==relation==="
    dname = models.ForeignKey(devices, on_delete=models.CASCADE)
    iname = models.ForeignKey(idc, on_delete=models.CASCADE)
