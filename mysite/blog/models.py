from django.db import models
from django.contrib.auth.models import User
import datetime

class Entry(models.Model):
    content = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(editable=False,default=0)
    author = models.ForeignKey(User, related_name="entries")

    def save(self):
        self.edit_date = datetime.datetime.now()
        self.view_count=self.view_count+1
        super(Entry, self).save()

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ["view_count"]
        verbose_name_plural = "Entries"
