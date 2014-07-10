#!/usr/bin/env python
#coding:utf-8

import json

from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response

from app.tao.models import Category, Images
from app.msg.models import Message
from app.msg.forms import MessageForm

def index(request, template):
    display = 60
    after_range_num = 5
    befor_range_num = 4
    s_template = request.session.get("template",None)
    
    if not s_template:
        request.session['template'] = False 
    elif request.session['template'] == True:
        template = "index.t.html"
    elif request.session['template'] == False:
        template = "index.html"
    
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    paginator = Paginator(Images.objects.all().order_by('-id'), display)
    try:
        items = paginator.page(page)
    except:
        items = paginator.page(1)
        #page range
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page + befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + befor_range_num]
    #template = "index.t.html"
    return render(request, template, locals())

def custom(request):
    s_template = request.session.get("template",None)
    
    if not s_template:
        request.session['template'] = False
    if request.method == 'POST':
        if request.POST['customset'] == '1':
            
            data = {'successful':True}
            result = json.dumps(data)
            request.session['template'] = True
            return HttpResponse(result, mimetype="javascript/json")
        else:
            a = request.POST['csrfmiddlewaretoken']
            data = {'successful':True}
            result = json.dumps(data)
            request.session['template'] = False
            return HttpResponse(result, mimetype="javascript/json")

def tao_list(request, template, id):
    display = 21
    after_range_num = 5
    befor_range_num = 4
    list_tao = True
    s_template = request.session.get("template",None)
    
    if not s_template:
        request.session['template'] = False
    elif request.session['template'] == True:
        template = "tao.list.t.html"
    elif request.session['template'] == False:
        template = "tao.list.html"
        
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
        
    category = get_object_or_404(Category, pk=id)

    paginator = Paginator(category.products.all().order_by('-id'), display)
    try:
        items = paginator.page(page)
    except:
        items = paginator.page(1)
        #page range
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page + befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + befor_range_num]
    
    return render(request, template, locals())

def tao_detail(request, template, id):
    images = get_object_or_404(Images, pk=id)
    comments = Message.objects.filter(message__exact=id)[:8]
    #i_id = images.category.id
    #category = get_object_or_404(Category, pk=i_id)
    #i_images = category.products.exclude(id=id).order_by('?')[:18]
    i_images = Images.objects.exclude(id=id).order_by('?')[:18]
    images.click += 1
    images.save()
    faces_id = [x+1 for x in range(20)]
    return render(request, template, locals())    

  
def msg(request):
    if request.method == 'POST':
    #if request.is_ajax():
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            face = form.cleaned_data['face']
            content = form.cleaned_data['content']
            data = {'successful':True,'face':face,'content':content}
            result = json.dumps(data)
            return HttpResponse(result, mimetype="javascript/json")
        else:
            data = {'successful':False,'face':'','content':'', 'error':form.errors}
            form = MessageForm(initial={'message':images.id})
    
    result = json.dumps(data)
    return HttpResponse(result)
    
def search(request, template):
    search = True
    q = request.GET.get('q', '')
    display = 60
    after_range_num = 5
    befor_range_num = 4

    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1 
        
    if q:
        ps = Images.objects.filter(Q(name__icontains=q) | Q(title__icontains=q) | Q(desc__icontains=q) | Q(tag__icontains=q) | Q(price__icontains=q)).order_by('-id')
    else:
        ps = Images.objects.all().order_by('-id')
        
    paginator = Paginator(ps, display)
    try:
        items = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        items = paginator.page(1)
    #page range
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page + befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + befor_range_num]
    
    page_count = paginator.count/display + 1
    return render(request, template, locals())
