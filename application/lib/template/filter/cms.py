#!/usr/bin/env python
#coding: utf-8

from django import template
register = template.Library()

from app.cms.models import Article

@register.inclusion_tag('left/news.html', takes_context=True)
def left_news(context,n):
    context['articles'] = Article.objects.all().order_by('-id')[:int(n)]
    return context