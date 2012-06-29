from django.conf.urls.defaults import patterns, include, url
from blog.user_view import logout, register, confirm, disable
from blog.views import newpost, profile, changeemail, approvement, approve_entry, disapprove_entry, home, edit, delete, post
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', home),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$',  'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),
    url(r'^accounts/disable/$', disable),

    url(r'^accounts/changepass/$', 'django.contrib.auth.views.password_change', {'template_name' : 'changepass.html'}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name' : 'profile.html'}),
    url(r'^accounts/changeemail/$', changeemail, name="changeemail"),
    url(r'^accounts/profile/$', profile),
    url(r'^confirm/(?P<activation_key>\w+)/$', confirm, name="confirm"),

    url(r'^/accounts/password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'password_reset_form.html', 'email_template_name': 'password_reset_email.html'}),
    url(r'^/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}),

    url(r'^approve/$', approvement),
    url(r'^approve/entry/(?P<entry_id>\d+)/$', approve_entry, name="approve_entry"),
    url(r'^disapprove/entry/(?P<entry_id>\d+)/$', disapprove_entry, name="disapprove_entry"),

    url(r'^newpost/$', newpost, name="newpost"),
    url(r'^edit/(?P<entry_id>\d+)/$', edit, name="edit"),
    url(r'^delete/(?P<entry_id>\d+)/$', delete, name="delete"),
    url(r'^post/(?P<entry_id>\d+)/$', post, name="post"),    
)
#urlpatterns += staticfiles_urlpatterns()

urlpatterns+= patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': "/home/gizem/Documents/blog/projects/simple-blog/mysite/static/"}))

handler404 = 'blog.error_view.error_404'
handler500 = 'blog.error_view.error_500'
