from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from blog.forms import EntryForm
from django.shortcuts import render_to_response, redirect

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

# profile page:
@login_required
def profile(request):
    return render_to_response('profile.html', RequestContext(request))
