#!/usr/bin/env python
#coding: utf-8

from django.conf import settings
from django.db import models
from app.tao.models import Images



class Message(models.Model):
    message = models.ForeignKey(Images, verbose_name="产品留言", null=True, blank=True)
    face = models.CharField("头像", max_length=255)
    content = models.TextField("留言")
    post_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message.name

    class Meta:
        ordering = ['-id']
        verbose_name = '留言'
        verbose_name_plural = '客户留言'
