from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import Entry
from django.forms import ModelForm, Textarea

class NewUserCreationForm(UserCreationForm):
	email = forms.EmailField(required = True)
	
	class Meta:
		model = User
		fields = ("username","email","password1","password2")

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

class EntryForm(ModelForm):
	class Meta:
		model = Entry
		exclude = ["pub_date","edit_date","view_count","author","approvement"]
		widgets = {'content' : Textarea(attrs={'cols':100,'rows':20}),}
	def save(self,request):
		entry = Entry(title = self.cleaned_data["title"], content = self.cleaned_data["content"], author = request.user)
		entry.save()

class ChangeEmailForm(forms.Form):
	email = forms.EmailField(required = True)
	
	class Meta:
		model = User
		fields = ("email")

	def save(self,request):
		u = request.user
		u.email = self.cleaned_data["email"]
		u.save()
		
