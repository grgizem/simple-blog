from django.http import HttpResponseRedirect

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import password_reset

from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from blog.forms import NewUserCreationForm
from blog.models import UserProfile
import datetime
from django.contrib import messages

from django.shortcuts import render_to_response, redirect, get_object_or_404


# user login:
def login(request):
    auth_login(request,{'template_name' : 'login.html'})
    return HttpResponseRedirect("/")

# user logout:
@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

# new user registeration:
def register(request):
    if request.method == 'POST':
	form = NewUserCreationForm(request.POST)
	if form.is_valid():
            form.save()
	    messages.add_message(request, messages.SUCCESS, 'The activation mail sent. Please check your inbox.')
            return HttpResponseRedirect("/")
    else:
        form = NewUserCreationForm()
    return render_to_response("register.html", {'form':form}, RequestContext(request))

# reset password:
def resetpass(request, template_name):
    return password_reset(request, template_name)

# new user confirmation:
def confirm(request,activation_key):
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    if user_profile.key_expires < datetime.datetime.today():
	messages.add_message(request, messages.ERROR, 'Your activation key expired, please send an email to more information and help to blog@blog.com')
	return HttpResponseRedirect('/')
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    messages.add_message(request, messages.SUCCESS, 'Your account activated. You can login now.')
    return HttpResponseRedirect('/')
