from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from blog.forms import EntryForm, ChangeEmailForm
from blog.models import Entry

from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.mail import send_mail

# home page:
def home(request):
    obj_list = Entry.objects.all().order_by("-view_count")
    return render_to_response('home.html', {'entries' : obj_list[:5]}, RequestContext(request))

# add comment:
@login_required
def newpost(request):
    if request.POST:
        entryform = EntryForm(request.POST)
        if entryform.is_valid():
            e = entryform.save(request)
	    messages.add_message(request, messages.WARNING, 'Your post is waiting to approve by admin.')
	    return render_to_response('home.html', RequestContext(request))
    else:
        entryform = EntryForm()
	return render_to_response('post.html', {'form' : entryform}, RequestContext(request))

# change password redrirection:
@login_required
def changepass(request):
    messages.add_message(request, messages.SUCCESS, 'Your password successfuly changed.')
    return render_to_response('home.html', RequestContext(request))

# change email:
@login_required
def changeemail(request):
    if request.POST:
	emailform = ChangeEmailForm(request.POST)
	if emailform.is_valid():
	    e = emailform.save(request)
	    messages.add_message(request, messages.SUCCESS, 'Your e-mail successfuly changed.')
	    return render_to_response('home.html', RequestContext(request))
    else:
	emailform = ChangeEmailForm()
	return render_to_response('changeemail.html', {'form' : emailform}, RequestContext(request))

# profile page:
@login_required
def profile(request):
    return render_to_response('profile.html', RequestContext(request))

# approvement page:
@user_passes_test(lambda u: u.is_superuser)
def approvement(request):
    entries = Entry.objects.filter(approvement=False)
    if entries:
	return render_to_response('approve.html', {'entries' : entries}, RequestContext(request))
    else:
	messages.add_message(request, messages.INFO,'There is no entry which is waiting for approvement.')
	return HttpResponseRedirect('/')

# approving an entry:
@user_passes_test(lambda u: u.is_superuser)
def approve_entry(request,entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    entry.approve_entry()
    entries = Entry.objects.filter(approvement=False)
    ctx = {
	'entries' : entries
	}
    messages.add_message(request, messages.SUCCESS, 'Entry approved')
    return render_to_response('approve.html', ctx, RequestContext(request))

# disapproving an entry:
@user_passes_test(lambda u: u.is_superuser)
def disapprove_entry(request,entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    entry.delete()
    entries = Entry.objects.filter(approvement=False)
    ctx = {
	'entries' : entries
	}
    messages.add_message(request, messages.SUCCESS, 'Entry deleted. Regarding mail sent to the author of the entry to inform.')
    return render_to_response('approve.html', ctx, RequestContext(request))
