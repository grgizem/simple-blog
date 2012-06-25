from django.conf.urls.defaults import patterns, include, url
from blog.user_view import logout, register, resetpass
from blog.views import newpost, profile, changeemail, approvement, approve_entry, disapprove_entry, home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^/', home),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$',  'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),

    url(r'^accounts/changepass/$', 'django.contrib.auth.views.password_change', {'template_name' : 'changepass.html'}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name' : 'profile.html'}),
    url(r'^accounts/changeemail/$', changeemail, name='changeemail'),
    url(r'^accounts/profile/$', profile),

    url(r'^approve/$', approvement),
    url(r'^approve/entry/(?P<entry_id>\d+)/', approve_entry, name='approve_entry'),
    url(r'^disapprove/entry/(?P<entry_id>\d+)/', disapprove_entry, name='dissapprove_entry'),

    url(r'^newpost/$', newpost, name='newpost'),
    
)
urlpatterns += staticfiles_urlpatterns()
