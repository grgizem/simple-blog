from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from blog.forms import EntryForm, ChangeEmailForm
from blog.models import Entry

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.mail import send_mail

# add comment:
@login_required
def newpost(request):
    if request.POST:
        entryform = EntryForm(request.POST)
        if entryform.is_valid():
            e = entryform.save(request)
	    ctx = {
		  'notification' : "Your post is waiting to approve by admin."
		  }
	    return render_to_response('home.html', ctx, RequestContext(request))
    else:
        entryform = EntryForm()
	return render_to_response('post.html', {'form' : entryform}, RequestContext(request))

# change password redrirection:
@login_required
def changepass(request):
    ctx = {
	  'notification' : "Your password successfuly changed."
	  }
    return render_to_response('home.html', ctx, RequestContext(request))

# change email:
@login_required
def changeemail(request):
    if request.POST:
	emailform = ChangeEmailForm(request.POST)
	if emailform.is_valid():
	    e = emailform.save(request)
	    ctx = {
		  'notification' : "Your e-mail successfuly changed."
		  }
	    return render_to_response('home.html', ctx, RequestContext(request))
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
	return render_to_response('home.html', {'notification' : "There is no entry which is waiting for approvement. Thank you!"})

# approving an entry:
@user_passes_test(lambda u: u.is_superuser)
def approve_entry(request,entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    entry.approve_entry()
    entries = Entry.objects.filter(approvement=False)
    ctx = {
	'entries' : entries,
	'notification' : "Entry approved."
	}
    return render_to_response('approve.html', ctx, RequestContext(request))

# disapproving an entry:
@user_passes_test(lambda u: u.is_superuser)
def disapprove_entry(request,entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    send_mail('Blog entry deleted', 'Dear Blogger, your item is deleted, because it found inappropriate. Your post was %s'%entry.content, 'grgizem@gmail.com', [request.user.email], fail_silently=False)
    entry.delete()
    entries = Entry.objects.filter(approvement=False)
    ctx = {
	'entries' : entries,
	'notification' : "Entry deleted and mail sent to the author of the entry."
	}
    return render_to_response('approve.html', ctx, RequestContext(request))
