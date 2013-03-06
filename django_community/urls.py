from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.gis import admin as gisadmin
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
    url(r'^geoadmin/', include(gisadmin.site.urls)),
    url('', include('django_socketio.urls')),
    #('^accounts/', include('django.contrib.auth.urls')),
    url(r'^member/login/$', 'django.contrib.auth.views.login', {'template_name': 'member/login.html'}),
    url(r'^member/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/member/login/'}),
    url(r'^member/profile/$', 'member.views.index'),
    url(r'^member/register/$', 'member.views.register'),
    url(r'^member/request/(?P<friend_id>\d+)/(?P<action>\d+)/$', 'member.views.accept_friendrequest'),
    url(r'^member/request/send/(?P<friend_id>\d+)/$', 'member.views.send_friendrequest'),
    url(r'^lobby/create/$', 'lobbys.views.create'),
    url(r'^lobby/all/$', 'lobbys.views.show_all'),
    url(r'^lobby/(?P<lobby_id>\d+)/$', 'lobbys.views.show'),
    url(r'^lobby/(?P<lobby_id>\d+)/list/$', 'lobbys.views.listplayers'),
    url(r'^lobby/(?P<lobby_id>\d+)/join/$', 'lobbys.views.join'),
    url(r'^lobby/(?P<lobby_id>\d+)/invite/(?P<user_id>\d+)/$', 'lobbys.views.invite'),
    url(r'^lobby/(?P<lobby_id>\d+)/invite/process/(?P<action>\d+)$', 'lobbys.views.response_invite'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve'),
)
