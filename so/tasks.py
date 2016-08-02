#!/usr/bin/python 
#coding:utf-8 
 
from so.models import tasktable,groups
import requests
import paramiko
# import pexpect
from celery import task
from so.models import userconf,devices

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


@task()
def task_run(arguments,model,h,g,type,id):
    r = {}
    if type == 'Group':
        gname = groups.objects.get(name=g)
        hs = gname.members.all()
        #print hs
        if model == 'test.ping':
            for h in hs:
                r.update(task_ping(h))
            d = r
            update_task(id,d)
            # return r.items()
        elif model == 'cmd.run' or 'state.sls':
            for h in hs:
                r.update(task_cmd(h,model,arguments))
            d = r
            update_task(id,d)
            # return r.items()
    
    else:
        if model == 'test.ping':        
            r.update(task_ping(h))
            d = r
            update_task(id,d)
            # return r.items()
        elif model == 'inits':
            # r.update(task_cmd(h,model,arguments))
            # print "########task ing##########"
            # r.update(initsalt(h, arguments))
            # r.update('a':'oeuouo')
            r.update(initsalt(h, arguments))

            d = r
            # print d
            update_task(id,d)
        else : #model == 'cmd.run' or 'state.sls':
            r.update(task_cmd(h,model,arguments))
            d = r
            update_task(id,d)
            # return r.items()
    

def task_ping(host):
        
    url = salturl + '/run'
    data = {
                "client": 'local',
                                    "tgt": host,
                                    "fun": 'test.ping',
                                    "username": username,
                                    "password": password,
                                    "eauth": 'pam',
                                    }               
    
    r = requests.post(url,data=data,verify=False)

    # print r.text
    a = r.json()
    result = a['return'][0]
    #print result
    return result ##.items()

    #print r.text
    #print r.status_code
    ## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb

def task_cmd(host,model,arguments):
    # url = 'https://59.108.38.73:9990/run'
    url = salturl + '/run'
    data = {
                "client": 'local',
                                    "tgt": host,
                                    "fun": model,
                                    "username": username,
                                    "password": password,
                                    "eauth": 'pam',
                                    "arg": arguments ,
                                    
                                    }       

    r = requests.post(url,data=data,verify=False)
    # print r.text
    a = r.json()
    result = a['return'][0]
    return result
    #return r.text
    #print r.status_code
    ## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb

def initsalt(host, passwd):
    '''
        1、修改/etc/salt/roster ，添加需要初始化的host
        例子：
                zabbix-server:
                 host: 10.1.0.52
        host2:
          host: 10.1.0.51
        2、初始化：安装saltclient，下发配置文件
    '''
    url = salturl + '/run'
    #初始化脚本
    cmd = "if uname -r|grep el6;then yum -y install http://repo.saltstack.com/yum/redhat/salt-repo-latest-1.el6.noarch.rpm;yum clean all;yum -y install salt-minion python;echo \'master: 10.0.50.152\' >> /etc/salt/minion;/etc/init.d/salt-minion restart;else echo \'os not centos\';fi"
    arguments = 'echo \'init:\' > /etc/salt/roster;echo \'  host: \'' +host+ ' >> /etc/salt/roster;echo \'  user: root\' >> /etc/salt/roster;echo \'  passwd: ' +passwd+ '\' >> /etc/salt/roster;/usr/bin/salt-ssh -i \'init\'  -r '+ '\"' + cmd + '\"'
    print "******************###################"
    print arguments
    # task_cmd
    data = {
        "client": 'local',
        "tgt": 'saltstack.idc',
        "fun": 'cmd.run',
        "username": username,
        "password": password,
        "eauth": 'pam',
        "arg": arguments,
        # "arg": 'ls /',

    }   
    # print data
    r = requests.post(url,data=data,verify=False)
    # return r.text
    a = r.json()
    result = a['return'][0]
    return result
    #return r.text
    # print result
    ## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb
def initzabbix(host, passwd):
    '''
        1、修改/etc/salt/roster ，添加需要初始化的host
        例子：
                zabbix-server:
                 host: 10.1.0.52
        host2:
          host: 10.1.0.51
        2、初始化：安装zabbix client，下发配置文件
    '''
    url = salturl + '/run'
    #初始化脚本
    cmd = "if uname -r|grep el6;then yum -y install http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/zabbix-release-2.4-1.el6.noarch.rpm;yum clean all;yum -y install zabbix-agent;echo \'Server=10.1.0.52\' >> /etc/zabbix/zabbix_agentd.conf;/etc/init.d/salt-minion restart;else echo \'os not centos\';fi"
    #ServerActive=10.1.0.52 
    # arguments = 'echo \'init:\' > /etc/salt/roster;echo \'  host: \'' +host+ ' >> /etc/salt/roster;echo \'  user: root\' >> /etc/salt/roster;echo \'  passwd: ' +passwd+ '\' >> /etc/salt/roster;/usr/bin/salt-ssh -i \'init\'  cmd.run '+ '\"' + cmd + '\"'
    print "******************###################"
    print arguments
    # task_cmd
    data = {
        "client": 'local',
        "tgt": 'saltstack.idc',
        "fun": 'cmd.run',
        "username": username,
        "password": password,
        "eauth": 'pam',
        "arg": cmd,
        # "arg": 'ls /',

    }   
    # print data
    r = requests.post(url,data=data,verify=False)
    # return r.text
    a = r.json()
    result = a['return'][0]
    return result
    #return r.text
    # print result
    ## bfe2890801bd0e2bd0075f6fae6bd664c83df1eb
# def initsys(host,passwd):
#     #初始化salt
#     initsalt(host, passwd)
#     #初始化zabbix
#     initzabbix(host, passwd)

def update_task(taskid,t_detail):
    # print taskid
    # print t_detail
    one = tasktable.objects.filter(id=taskid)
    one.update(detail=t_detail)

@task()
def update_info(devid,ip,user,passwd,port):
    cmds = {
        'hyper':'lscpu |grep \"Hypervisor vendor:\"|awk -F \":\" \'{print $2}\'',
        'disk':'fdisk -l|grep  \"Disk\"|grep \'/dev/\'|awk \'{print $2,$3,$4}\'',
        'partion':'ls -d /home',
        'mem':'free -m|grep "Mem:"|awk \'{print $2}\'',
        'cputype':'cat /proc/cpuinfo |grep \"model name\"|head -n 1|awk -F \":\" \'{print $2}\'',
        'cpunum':'lscpu |grep ^CPU\(s\):|awk -F \":\" \'{print $2}\'',
        'os':'uname -r'
    }
    res = {}
    paramiko.util.log_to_file('/tmp/paramiko.log')
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,username=user,password=passwd,port=port)
    for key in cmds.keys():
        # print key
        # print value
        # print "sudo %s" % cmds[key]
        stdin,stdout,stderr = ssh.exec_command("sudo %s" % cmds[key],get_pty=True)
        stdin.write('%s\n' % passwd)
        stdin.flush()
        line = stdout.read()
        # for line in stdout.readlines():
        print line.split(':',1)[1]
        res[key] = line.split(':',1)[1].strip()
            # print res[key]
            # print line
        # res.update(tmp)
    ssh.close()
    sql = devices.objects.filter(id=devid)
    sql.update(hyper=res['hyper'],
        disk=res['disk'],
        partion=res['partion'],
        mem=res['mem'],
        cputype=res['cputype'],
        cpunum=res['cpunum'],
        os=res['os'],
        )
   


