from django.contrib import admin
from .models import Topic, Entry

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ['text', 'slug', 'owner', 'date_added']
	list_filter = ['owner']
	search_fields = ['text', 'owner']
	prepopulated_fields = {'slug': ('text',)}
	raw_id_fields = ['owner']
	date_hierarchy = 'date_added'
	ordering = ['date_added']

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'author', 'date_added']
	list_filter = ['topic']
	search_fields = ['title', 'author']
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ['author']
	date_hierarchy = 'date_added'
	ordering = ['date_added']