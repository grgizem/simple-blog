from django.http import HttpResponseRedirect

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import password_reset


from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django import oldforms as forms

from django.shortcuts import render_to_response, redirect

# user login:
def login(request):
    auth_login(request)
    return HttpResponseRedirect("/")

# user logout:
@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

# new user registeration:
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            new_user = form.save(data)
            return HttpResponseRedirect()
    else:
        data, errors = {}, {}
    return render_to_response("register.html",
            {'form':forms.FormWrapper(form,data,errors)})

# reset password:
def resetpass(request, template_name):
    return password_reset(request, template_name)
