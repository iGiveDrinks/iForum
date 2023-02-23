from django.contrib import admin
from .models import Forum, Thread, Comment

# Register your models here.
@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'body', 'author', 'created', 'status', 
					'active']
	list_filter = ['status', 'active', 'created', 'author']
	search_fields = ['title', 'author']
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ['author']
	date_hierarchy = 'created'
	ordering = ['created', 'status']

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
	list_display = ['short_title', 'short_body', 'author', 'publish', 'status',
					'upvote', 'pinned', 'active']
	list_filter = ['status', 'active', 'created', 'forum', 'author',]
	search_fields = ['title', 'author']
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ['author']
	date_hierarchy = 'publish'
	ordering = ['publish', 'status']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['short_body', 'author', 'publish', 'status', 'upvote',
					'active']
	list_filter = ['status', 'active', 'created', 'thread', 'author']
	search_fields = ['body', 'author']
	raw_id_fields = ['author']
	date_heirachy = 'publish'
	ordering = ['publish', 'status']