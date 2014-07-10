#!/usr/bin/python
#coding:utf-8
#Created on 2012-4-24 上午10:21:46
#author: lihuan, 227501@qq.com

from django.db import models

def get_filter_manager(*args, **kwargs):
    class FilterManager(models.Manager):
        def get_query_set(self):
            return super(self.__class__, self).get_query_set().filter(*args, **kwargs)
    return FilterManager()