from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from django.shortcuts import render_to_response, redirect

# add comment:
@login_required
def add_entry(request):
    if request.POST:
        entryform = EntryForm(request.POST)
        if entryform.is_valid():
            entryform.save(request)
    else:
        entryform = EntryForm()
