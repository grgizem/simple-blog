from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from blog.forms import EntryForm, ChangeEmailForm
from blog.models import Entry

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.mail import send_mail

# home page:
def home(request):
    obj_list = Entry.objects.filter(approvement=True).order_by("-view_count")
    paginator = Paginator(obj_list, 5)
    try:
	page = int(request.GET.get('page','1'))
    except ValueError:
	page = 1
    try:
	entries = paginator.page(page)
    except (EmptyPage,InvalidPage):
	entries = paginator.page(paginator.num_pages)
    return render_to_response('home.html', {'entries' : entries} , RequestContext(request))

# add comment:
@login_required
def newpost(request):
    if request.POST:
        entryform = EntryForm(request.POST)
        if entryform.is_valid():
            entryform.save(request)
	    messages.add_message(request, messages.WARNING, 'Your post is waiting to approve by admin.')
	    return render_to_response('home.html', RequestContext(request))
    else:
        entryform = EntryForm()
	return render_to_response('newpost.html', {'form' : entryform}, RequestContext(request))

# change password redrirection:
@login_required
def changepass(request):
    messages.add_message(request, messages.SUCCESS, 'Your password successfuly changed.')
    return HttpResponseRedirect('/')

# change email:
@login_required
def changeemail(request):
    if request.POST:
	emailform = ChangeEmailForm(request.POST)
	if emailform.is_valid():
	    emailform.save(request)
	    messages.add_message(request, messages.SUCCESS, 'Your e-mail successfuly changed.')
	    return HttpResponseRedirect('/')
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
    messages.add_message(request, messages.SUCCESS, 'Entry approved')
    return render_to_response('approve.html', {'entries' : entries}, RequestContext(request))

# disapproving an entry:
@user_passes_test(lambda u: u.is_superuser)
def disapprove_entry(request,entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    send_mail('Simple Blog', 'Your following post is disapproved, because it found inappropriate.\nPost: %s'%entry.content, 'blog@blog.com', [entry.author.email], fail_silently=False)
    entry.delete()
    entries = Entry.objects.filter(approvement=False)
    messages.add_message(request, messages.SUCCESS, 'Entry deleted. Regarding mail sent to the author of the entry to inform.')
    return render_to_response('approve.html', {'entries' : entries}, RequestContext(request))

# edit an entry:
@login_required
def edit(request,entry_id):
    e = get_object_or_404(Entry, id=entry_id)
    if request.user.id == e.author.id:
        if request.POST:
            entryform = EntryForm(request.POST)
            if entryform.is_valid():
		entryform.save_as(request,e)
		messages.add_message(request, messages.WARNING, 'Your post is waiting for approvement.')
                return HttpResponseRedirect('/')
        else:
            entryform = EntryForm({'title' : e.title, 'content' : e.content})
            return render_to_response('edit.html', {'entry_id' : entry_id, 'form' : entryform}, RequestContext(request))
    else:
        messages.add_message(request, messages.ERROR, 'You can not edit this post, because you are not the author of it.')
        return HttpResponseRedirect('/')

# delete an entry:
@login_required
def delete(request,entry_id):
    e = get_object_or_404(Entry, id=entry_id)
    if request.user.id == e.author.id:
    	e.delete()
	messages.add_message(request, messages.SUCCESS, 'Your post deleted.')
    	return HttpResponseRedirect('/')
    else:
	message.add_message(request, messages.ERROR, 'You can not delete this post, because you are not the author of it.')
	return HttpResponseRedirect('/')

# show an entry:
def post(request,entry_id):
    e = get_object_or_404(Entry, id=entry_id)
    e.viewed()
    return render_to_response('post.html', {'entry' : e}, RequestContext(request))
