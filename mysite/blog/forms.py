from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import Entry

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

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		exclude = ["pub_date","edit_date","view_count","author","approvement"]
	
	def save(self,request):
		entry = Entry(content = self.cleaned_data["content"], author = request.user)
		entry.save()

