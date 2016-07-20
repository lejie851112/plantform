from django.contrib.auth.models import User,Group

def createuser(name,password,email='NULL'):
	user = User.objects.create_user(name, email, password)
	# user.last_name = 'Lennon'
	user.save()
def changepass(name,password):
	u = User.objects.get(username=name)
	u.set_password(password)
	u.save()
def creategroup(name):
	g = Group(name=name)
	# user.last_name = 'Lennon'
	g.save()
def grouplist():
	gl = Group.objects.all()
	# user.last_name = 'Lennon'
	# user.save()
	return gl
def userlist():
	ul = User.objects.all()
	return ul
def groupdel(gname):
	g = Group.objects.get(name=gname)
	g.delete()
def userdel(uname):
	user = User.objects.get(username=uname)
	# user.last_name = 'Lennon'
	user.delete()
def useredit(upass,uid):
	user = User.objects.get(id=uid)
	# user.last_name = 'Lennon'
	# user.update(username=uname)
	user.set_password(upass)
	user.save()
def userdetail(uid):
	user = User.objects.get(id=uid)
	# user.last_name = 'Lennon'
	return user
def userrole(name):
	user = User.objects.get(username=name)
	# user.last_name = 'Lennon'
	if str(user.is_superuser) == "True":
		return "True"
	else:
		return "False" 
def groupedit(gid,gname):
	g = Group.objects.filter(id=gid)
	g.update(name=gname)
def groupdetail(gid):
	g = Group.objects.get(id=gid)
	return g

# myuser.groups.set([group_list])
# myuser.groups.add(group, group, ...)
# myuser.groups.remove(group, group, ...)
# myuser.groups.clear()
# myuser.user_permissions.set([permission_list])
# myuser.user_permissions.add(permission, permission, ...)
# myuser.user_permissions.remove(permission, permission, ...)
# myuser.user_permissions.clear()
# django.contrib.auth.models.Group 