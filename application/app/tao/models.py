#!/usr/bin/env python
#coding: utf-8

import datetime,random

from django.conf import settings
from django.db import models
from django.db.models import permalink
from lib.db.manager import get_filter_manager


class Category(models.Model):
    name = models.CharField("产品分类", max_length=255)
    parent = models.ForeignKey('self', verbose_name='上一级', null=True, blank=True, related_name='children')
    path = models.CharField("路径", max_length=255, null=True, blank=True, help_text="此项不用填写")
    js = models.TextField("js脚本文件", max_length=255, blank=True, null=True, help_text="用到的js脚本")
    keywords = models.CharField("页面关键词", max_length=255, null=True, blank=True)
    description = models.CharField("页面描述", blank=True, null=True, max_length=255)
    direct_link = models.CharField("转向链接", max_length=255, null=True, blank=True)
    is_active = models.BooleanField("是否生效", default=True)
    post_time = models.DateTimeField("发布时间", auto_now_add=True)
    admin_objects = models.Manager()
    objects = get_filter_manager(is_active=True)
    
    def __unicode__(self):
        if not self.path:
            return self.name
        if self.id == self.path:
            return self.name
        else:
            return self.node

    def _node(self):
        indent_num = len(self.path.split(':')) -1
        indent = '____' * indent_num
        node = u'%s%s' % (indent, self.name)
        return node
    node = property(_node)

    def url(self):
        if len(self.direct_link) > 0:
            return self.direct_link.replace(".","/")
        return ('tao.images.list', '', {'id':self.id})

    @models.permalink
    def get_absolute_url(self):
        return ('images.list', None, {'id':self.id})

    @property
    def has_children(self):
        return self.children.all().count() > 0 and True or False

    def get_parents(self):
        parents_path = self.path.split(":")
        if len(parents_path)> 1:
            path = parents_path[:-1]
        else:
            path = parents_path
        parents = Category.objects.filter(pk__in=parents_path)
        return parents

    def save(self, * args, ** kwargs):
        super(Category, self).save(*args, ** kwargs)
        if self.parent:
            self.path = '%s:%s' % (self.parent.path, self.id)
        else:
            self.path = self.id
        childrens = self.children.all()
        if len(childrens) > 0:
            for children in childrens:
                children.path = '%s:%s' % (self.path, children.id)
                children.save()
        super(Category, self).save(*args, ** kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = '产品分类'
        verbose_name_plural = '产品分类管理'

class Images(models.Model):
    category = models.ForeignKey(Category, verbose_name="产品分类", related_name='products')
    name = models.CharField("产品标题", max_length=255)
    title = models.CharField("淘宝标题", max_length=255, blank=True, null=True)
    price = models.CharField("产品价格", max_length=255, default="¥ ")
    link = models.CharField("产品链接", max_length=255)
    gallery = models.ImageField(upload_to=settings.UPLOAD_TO, verbose_name="产品图片")
    small_gallery = models.ImageField(upload_to=settings.UPLOAD_TO, verbose_name="产品小图", blank=True, null=True)
    keywords = models.CharField(verbose_name="产品关键字", max_length=255, blank=True, null=True)
    desc = models.TextField(verbose_name="产品描述", blank=True, null=True)
    click = models.IntegerField("浏览数", max_length=10, default=1, help_text="此项不用填写")
    is_public = models.BooleanField(default=True, verbose_name="是否公开")
    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    tag = models.TextField(verbose_name="标签", blank=True, null=True, help_text="请用英文,分隔每个标签")
    post_time = models.DateTimeField("发布时间", auto_now_add=True)
    end_time = models.DateTimeField("结束时间", default=datetime.datetime.now()+datetime.timedelta(days=90), help_text="如不添加，将在90天后结束")
    admin_objects = models.Manager()
    #objects = get_filter_manager(is_public=True, end_time__gte=datetime.datetime.now())
    objects = get_filter_manager(is_public=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tao.images.detail', '', {'id':self.id})

    @property
    def get_title(self):
        if len(self.title) > 0:
            return self.title
        else:
            return self.name
	
    def url(self):
        return self.get_absolute_url()

    class Meta:
        ordering = ['-id']
        verbose_name = '产品'
        verbose_name_plural = '产品管理'

