#!/usr/bin/env python
#coding:utf-8
#created: 2012-3-11 下午10:16:33
#auth: lihuan, 227501@qq.com
from __future__ import division

from datetime import datetime
from django.utils.safestring import mark_safe
from django.template.base import Library

register = Library()

@register.filter
def replace(v, s):
    b,d = s.split(":")
    return v.replace(b,d)

@register.filter
def strip(v):
    return v.strip()

@register.filter
def split(v, s):
    return v.split('%s' % s)

@register.filter
def time_pass(value):
    delta = datetime.now() - value
    if delta.days >= 365:
        s = '%d年前' % (delta.days / 365)
    elif delta.days >= 30:
        s = '%d个月前' % (delta.days / 30)
    elif delta.days > 0:
        s = '%d天前' % delta.days
    elif delta.seconds < 60:
        s = '<span class="sec_ago">%d秒前</span>' % delta.seconds
    elif delta.seconds < 60 * 60:
        s = '<span class="min_ago">%d分钟前</span>' % (delta.seconds / 60)
    else:
        s = "%d小时前" % (delta.seconds / 60 / 60)
    return mark_safe(s)
time_pass.is_safe=True