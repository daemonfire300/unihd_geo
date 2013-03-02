from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_community.views.home', name='home'),
    # url(r'^django_community/', include('django_community.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^member/login/$', 'django.contrib.auth.views.login', {'template_name': 'member/login.html'}),
    url(r'^member/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/polls/1'}),
    url(r'^member/profile/$', 'member.views.index'),
    url(r'^member/register/$', 'member.views.register'),
    url(r'^lobby/create/$', 'lobbys.views.create'),
    url(r'^lobby/(?P<lobby_id>\d+)/$', 'lobbys.views.show'),
    url(r'^lobby/(?P<lobby_id>\d+)/list/$', 'lobbys.views.listplayers'),
    url(r'^lobby/(?P<lobby_id>\d+)/join/$', 'lobbys.views.join'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve'),
)
