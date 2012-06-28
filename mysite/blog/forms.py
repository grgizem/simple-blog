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

	def save(self):
        	user = User.objects.create_user(self.cleaned_data["username"],self.cleaned_data["email"],self.cleaned_data["password1"])
		user.is_active=False
		user.save()
		# Activation properties
		salt = sha.new(str(random.random())).hexdigest()[:5]
		activation_key = sha.new(salt+user.username).hexdigest()
		key_expires = datetime.datetime.today()+datetime.timedelta(2)
		new_user = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
		new_user.save()
		# sending an activation email
		email_subject = 'Your new account confirmation'
		email_body = 'Hello, %s, and thanks for registering for the blog \n To active your account, click following link within 48 hours: \n http://localhost:8000/accounts/confirm/%s' %(user.username, new_profile.activation_key)
		send_email(email_subject, email_body, 'blog@blog.com', [user.email])

class EntryForm(ModelForm):
	class Meta:
		model = Entry
		exclude = ["pub_date","edit_date","view_count","author","approvement"]
		widgets = {'content' : Textarea(attrs={'cols':100,'rows':20}),}
	def save(self,request):
		entry = Entry(title = self.cleaned_data["title"], content = self.cleaned_data["content"], author = request.user)
		entry.save()
	def save_as(self,request,entry):
		entry.title = self.cleaned_data["title"]
		entry.content = self.cleaned_data["content"]
		entry.approvement = False
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
		
