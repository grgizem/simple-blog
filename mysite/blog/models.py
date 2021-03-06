import datetime

from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    title = models.CharField(max_length=300)
    content = models.CharField(max_length=5000)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(editable=False,default=0)
    author = models.ForeignKey(User, related_name="entries")
    approvement = models.BooleanField(default=False)

    def approve_entry(self):
	self.approvement = True
	super(Entry, self).save()

    def viewed(self):
        Entry.objects.filter(id=self.id).update(view_count=models.F('view_count')+1)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["view_count"]
        verbose_name_plural = "Entries"

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
