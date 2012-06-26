from django.http import HttpResponseRedirect

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import password_reset

from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from blog.forms import NewUserCreationForm

from django.shortcuts import render_to_response, redirect

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
            return HttpResponseRedirect("/")
    else:
        form = NewUserCreationForm()
    return render_to_response("register.html", {'form':form}, RequestContext(request))

# reset password:
def resetpass(request, template_name):
    return password_reset(request, template_name)
