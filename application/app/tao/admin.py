#!/usr/bin/env python
#coding: utf-8

from django.conf import settings
from django.contrib import admin
from app.tao.models import Category, Images
from app.msg.models import Message

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','path','direct_link','treenode','images_count',]
    
    
    def path(self, obj):
        if obj.parent:
            return u'%s > %s' % (obj.parent, obj.name)
        return obj.name
    path.short_description = 'path'
    path.allow_tags = True
    
    def treenode(self, obj):
        indent_num = len(obj.path.split(':')) -1
        p = '<div style="text-indent:%spx;">%s</div>' % (indent_num*25, obj.name)
        return p
    treenode.short_description = '路径'
    treenode.allow_tags = True

    def images_count(self,obj):
        count = obj.products.all().count()
        return count
    images_count.short_description = '项目数'
    
class MessageAdmin(admin.TabularInline):

    model = Message

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_public','name','has_link', 'price',  'pic', 'remark','post_time']
    list_filter = ['is_public','category']
    search_fields = ['id', 'name', 'link', ]
    ordering = ['-id']
    inlines = [MessageAdmin]
    actions = ['mark_public','unmark_public']
	
	
    def pic(self, obj):
        return '<img src="%s%s" width="80"/ >' % (settings.MEDIA_URL, obj.gallery)
    pic.short_description = '预览图'
    pic.allow_tags = True
    
    def has_link(self, obj):
        img = 'no'
        if obj.link:
            img = 'yes'
        return '<img src="/static/admin/img/icon-%s.gif">' % img
    has_link.short_description = '链接'
    has_link.allow_tags = True
    
    def mark_public(self, request, queryset):
        queryset.update(is_public=True)
    mark_public.short_description = u"设置成公开"
    def unmark_public(self, request, queryset):
        queryset.update(is_public=False)
    unmark_public.short_description = u"取消公开"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Images, ImagesAdmin)

