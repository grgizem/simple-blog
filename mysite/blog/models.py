from django.db import models
from django.contrib.auth.models import User
import datetime

class Entry(models.Model):
    content = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(editable=False,default=0)
    author = models.ForeignKey(User, related_name="entries")
    approvement = models.BooleanField(default=False)

    def save(self):
        self.edit_date = datetime.datetime.now()
        super(Entry, self).save()
    
    def approve_entry(self):
	self.approvement = True
	super(Entry, self).save()

    def viewed(self):
	self.view_count=self.view_count+1

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ["view_count"]
        verbose_name_plural = "Entries"
