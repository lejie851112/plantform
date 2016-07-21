#!/usr/bin/python 
#coding:utf-8 

from so.models import devices,idc,devtoidc


def saveidc(name):
    if not idc.objects.filter(iname=name):
        sql = idc(iname=name)
        sql.save()
def showidc():
    idcs = idc.objects.all()
    return idcs