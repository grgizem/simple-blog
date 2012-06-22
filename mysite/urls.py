from django.conf.urls.defaults import patterns, include, url
from blog.user_view import login, logout, register, resetpass
from blog.views import newpost
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',  'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),
    url(r'^newpost/$', newpost, name='newpost'),

)
urlpatterns += staticfiles_urlpatterns()
