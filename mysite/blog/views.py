from django.http import HttpResponseRedirect

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django import oldforms as forms

from django.shortcuts import render_to_response, redirect, get_object_or_404

def login(request):
    auth_login(request)
    return HttpResponseRedirect("/")

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

def register(request):
    form = UserCreationForm()

    if request.method == 'POST'
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            new_user = form.sava(data)
            return HttpResponseRedirect()
    else:
        data, errors = {}, {}
    return render_to_response("register.html",
            {'form':forms.FormWrapper(form,data,errors)})
