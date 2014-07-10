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
from app.cyp.models import Project
from app.cms.models import Article


from django import template
register = template.Library()

@register.inclusion_tag('header.ad.html', takes_context=True)
def project_header_ad(context,n):
    context['project_tops'] = Project.objects.filter(is_top=True)[:int(n)]
    return context
    
@register.inclusion_tag('cang.jing.ge.html', takes_context=True)
def cang_jing_ge(context):
    var = {"story_img": Article.objects.filter(category_id=5, gallery__startswith=settings.UPLOAD_DIR)[0:1],
              "story": Article.objects.filter(category_id=5)[:4],
              "case_img": Article.objects.filter(category_id=8, gallery__startswith=settings.UPLOAD_DIR)[0:1],
              "case": Article.objects.filter(category_id=8)[:4],
              "experience_img": Article.objects.filter(category_id=6, gallery__startswith=settings.UPLOAD_DIR)[0:1],
              "experience": Article.objects.filter(category_id=6)[:4],
              "start_img": Article.objects.filter(category_id=9, gallery__startswith=settings.UPLOAD_DIR)[0:1],
              "start": Article.objects.filter(category_id=9)[:4],
            }
    context.update(var)
    return context
    
@register.inclusion_tag('child.cang.jing.ge.html', takes_context=True)
def child_cang_jing_ge(context):
    var = {"story_img": Article.objects.filter(category_id=5, gallery__startswith=settings.UPLOAD_DIR)[0:1],
            "story": Article.objects.filter(category_id=5)[:5],
            "case_img": Article.objects.filter(category_id=8, gallery__startswith=settings.UPLOAD_DIR)[0:1],
            "case": Article.objects.filter(category_id=8)[:5],
            "experience_img": Article.objects.filter(category_id=6, gallery__startswith=settings.UPLOAD_DIR)[0:1],
            "experience": Article.objects.filter(category_id=6)[:5],
            "start_img": Article.objects.filter(category_id=9, gallery__startswith=settings.UPLOAD_DIR)[0:1],
            "start": Article.objects.filter(category_id=9)[:5],
            "start_img": Article.objects.filter(category_id=1, gallery__startswith=settings.UPLOAD_DIR)[0:1],
            "guide":Article.objects.filter(category_id=1)[:7],
            #"project_img":Project.objects.filter(is_hot=True).order_by('?')[:6],
            "project_img":Project.objects.all()[:6],
            #"project_img":Project.objects.all().order_by('?')[:6],
            }
    context.update(var)
    return context
    
@register.inclusion_tag('child.header.ad.html', takes_context=True)
def child_project_header_ad(context,n):
    return context
    
