#!/usr/bin/python
#coding:utf-8
#created: 2012-3-11 下午10:16:33
#auth: lihuan, 227501@qq.com

import os
from datetime import datetime
import random
import Image
import ImageFilter
import ImageEnhance
from django.conf import settings
from django.utils.safestring import mark_safe
from app.bbs.models import Thread

from django import template
register = template.Library()

@register.simple_tag
def title_rand_class(s):
    rc = s.split(",")
    n = random.randint(0,len(rc)-1)
    return rc[n]
    


@register.inclusion_tag('header.threads.html', takes_context=True)
def header_threads(context,n):
    context['threads'] = Thread.objects.all()[:int(n)]
    return context