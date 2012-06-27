from django.http import HttpResponseRedirect
from django.contrib import messages

def error_404(request):
    messages.add_message(request, messages.ERROR, 'A ninja stole this page. You must return when the moon has friends and the fox is borrowed.')
    return HttpResponseRedirect('/')

def error_500(request):
    messages.add_message(request, messages.ERROR, 'Someone on the staff is to blame for this! Rest assured, the proper person will get the proper amount of blame and humiliation dealt to them. If you have any choice words to pass along, please email grgizem@gmail.com')
    return HttpResponseRedirect('/')
