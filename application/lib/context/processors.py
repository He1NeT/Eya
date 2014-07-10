#!/usr/bin/python
#coding:utf-8
#Created on 2012-9-16  下午4:50:37
#author: lihuan, 227501@qq.com
#desc: 
from django.conf import settings

def site_info(request):
    context = {'SITE_DOMAIN':settings.SITE_DOMAIN,
               'SITE_ID': settings.SITE_ID}
    return context