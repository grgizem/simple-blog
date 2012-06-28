from django.db import models
from django.contrib.auth.models import User
import datetime

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
	self.view_count=self.view_count+1
	super(Entry, self).save()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["view_count"]
        verbose_name_plural = "Entries"
