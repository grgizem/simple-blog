from blog.models import Entry
from django.contrib import admin

def approve(modeladmin, request, queryset):
	queryset.update(approvement=True)
approve.short_description = "Approve selected entries"

class EntryAdmin(admin.ModelAdmin):
	list_display = ['title','author','approvement']
	ordering = ['title']
	actions = [approve]
	
admin.site.register(Entry,EntryAdmin)
