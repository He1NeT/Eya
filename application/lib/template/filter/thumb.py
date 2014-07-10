#!/usr/bin/env python
#coding:utf-8
#Created on 2012-5-18 上午9:57:21
#author: lihuan, 227501@qq.com
import os
from urlparse import urlparse
from django.conf import settings
from django import template

register = template.Library()

class Thumbnail(object):
    def __init__(self, src, width=100, height=100, dir='', background="#ffffff",quality=100):
        self._src = src
        self._thumb_dir = dir
        self._thumb_width = width
        self._thumb_height = height
        self._thumb_background = background
        self._thumb_quality = quality
        self._thumb_sizes = self._thumb_width * self._thumb_height
        self._thumb_save_dir = '%s/%s' % (settings.MEDIA_ROOT, self._thumb_dir)
        
        if hasattr(self._src, 'path'):
            self._src_path = src.path
            self._src_suffix = src.name[-3:]            
        elif src.startswith('http://'):
            self._src_path = urlparse(src).path[1:]
            self._src_suffix = self._src_path[-3:]
        else:
            self._src_path = self._src
            self._src_suffix = self._src[-3:]
        
        if self._src_suffix.lower() not in ["jpg", "jpeg", "gif", "png"]:
            self._src_suffix = "jpg"        
        
        self._thumb_suffix_extra = "_%dx%d.%s" % (self._thumb_width, 
                                                  self._thumb_height, 
                                                  self._src_suffix)
        
        if '/' in self._src_path:
            self._thumb_name = self._src_path[self._src_path.find('/')+1:]
        else:
            self._thumb_name = self._src_path
        
        self._thumb_path = '%s/%s%s' % (self._thumb_save_dir, self._src_path, self._thumb_suffix_extra)
        
    @property
    def __command(self):        
        return "gm convert -colorspace RGB '%s' -thumbnail '%d@' -background '%s' -quality %d -gravity center -extent %dx%d %s" % (self._src, self._thumb_sizes, self._thumb_background, self._thumb_quality, self._thumb_width, self._thumb_height, self._thumb_path)
    
    def _create_thumb(self):
        try:
            _thumb_path_dir = os.path.dirname(self._thumb_path)
            if not os.path.exists(_thumb_path_dir):
                os.makedirs(_thumb_path_dir)
            if not os.path.exists(self._thumb_path):
                os.system(self.__command)
            thumb_uri = '%s%s/%s%s' % (settings.MEDIA_URL, self._thumb_dir, self._thumb_name, self._thumb_suffix_extra)
            return thumb_uri
        except:
            pass
    
    @property
    def thumb(self):
        return self._create_thumb()

@register.filter
def thumb(src, arg):
    if src:
        #thumb size
        s = 'x' in arg and 'x' or ':'
        w, h = arg.split(s)
        t = Thumbnail(src, width=int(w), height=int(h), 
                      dir=settings.UPLOAD_IMAGE_THUMB_DIR, 
                      background="#f3f3f3", quality=100)
        return t.thumb
thumb.is_safe = True