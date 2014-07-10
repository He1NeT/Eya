#!/usr/bin/python
#coding:utf-8
#Created on 2012-3-23 下午1:41:52
#author: lihuan, 227501@qq.com
import os
from PIL import Image
from django.conf import settings
from django import template

register = template.Library()

def thumbnail(src, thumb_width=0, thumb_height=0, thumb_dir='',quality=100):
    img = Image.open(src.path)
    w, h = img.size
    w = float(w)
    h = float(h)
    thumb_width = float(thumb_width)
    thumb_height = float(thumb_height)
    if thumb_height == 0:
        thumb_height = (thumb_width/w)*h
    else:
        thumb_width = (thumb_height/h)*w

    src_suffix = src.name[-3:]
    if src_suffix.lower() not in ["jpg", "jpeg", "gif", "png"]:
        src_suffix = "jpg"
    thumb_size_s = thumb_width * thumb_height
    thumb_additioinal_suffix = "_%dx%d.%s" % (thumb_width, thumb_height, src_suffix)
    
    thumb_os_dir = '%s/%s' % (settings.MEDIA_ROOT, thumb_dir)
    if '/' in src.name:
        thumb_name = src.name[src.name.find('/')+1:]
    else:
        thumb_name = src.name
    thumb_path = '%s/%s%s' % (thumb_os_dir, thumb_name, thumb_additioinal_suffix)    
    command = "/usr/bin/convert -colorspace RGB '%s' -thumbnail '%d@' -quality %d -gravity center -extent %dx%d %s" % (src.path, thumb_size_s, quality, thumb_width, thumb_height, thumb_path)
    
    try:
        thumb_path_dir = os.path.dirname(thumb_path)
        if not os.path.exists(thumb_path_dir):
            os.makedirs(thumb_path_dir)
        if not os.path.exists(thumb_path):
            os.system(command)
    except:
        pass
    thumb_url = '%s%s/%s%s' % (settings.MEDIA_URL, thumb_dir, thumb_name, thumb_additioinal_suffix)
    return thumb_url

@register.filter
def thumb(src, arg):
    if src:
        #thumb size
        s = 'x' in arg and 'x' or ':'
        w, h = arg.split(s)
        return thumbnail(src, int(w),int(h), thumb_dir=settings.UPLOAD_IMAGE_THUMB_DIR)
    else:
        return '%s%s' % (settings.MEDIA_URL, 'images/1x1.jpg')
thumb.is_safe = True
