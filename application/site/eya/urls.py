#!/usr/bin/python
#coding:utf-8

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import redirect_to, direct_to_template
import captcha
from app.tao.models import Category, Images

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
   

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^(static|public)/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%sfavicon.ico' % settings.MEDIA_URL}),
    url(r'^root\.txt$', 'django.views.generic.simple.redirect_to', {'url': '%sroot.txt' % settings.MEDIA_URL}),
    url(r'^xtaoAuth\.html$', 'django.views.generic.simple.redirect_to', {'url': '%sxtaoAuth.html' % settings.MEDIA_URL}),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^user/', include('app.user.urls')),
)

#static file
urlpatterns += patterns('',
    url(r'^(static|public)/(?P<path>.*)$',
        'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
)

urlpatterns += patterns('views',
    url(r'^$',  'index', {'template':'index.html'}, name='index'),
    url(r'^custom/$',  'custom', name='custom'),
    url(r'^eya/(?P<id>\d+)/$',  'tao_detail', {'template':'tao.detail.html'}, name='tao.images.detail'),
    url(r'^addcomment/$',  'msg', name='msg'),
    url(r'^search/$', 'search', {'template':'tao.list.html'}, name='search'),
    )


categories = Category.objects.all()
for c in categories:
    if len(c.direct_link) > 0:
        urlpatterns += patterns('views',
            url(r'^%s/$' % c.direct_link.replace(".","/"), 'tao_list', {'template':'tao.list.html', 'id':c.id}, name='%s' % c.direct_link),
        )

tao = Images.objects.all()
for c in tao:	
	urlpatterns += patterns('',
		('^eya/%s/buy/$' % c.id, redirect_to, {'url': c.link}),
	)
