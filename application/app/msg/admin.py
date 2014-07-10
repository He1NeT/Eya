#!/usr/bin/env python
#coding: utf-8

from django.contrib import admin
from app.msg.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'content','message','post_time']

admin.site.register(Message, MessageAdmin)


