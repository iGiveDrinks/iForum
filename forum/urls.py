from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
	# home page
	path('', views.index, name='index'),

	path('forums/forum_create/',
		views.forum_create, name='forum_create'),

	path('forums/forum_edit/<int:id>/',
		views.forum_edit, name='forum_edit'),

	path('forums/forum_delete/<int:id>/',
		views.forum_delete, name='forum_delete'),

	path('forums/<int:id>/',
		views.thread_list, name='thread_list'),

	path('thread/<int:year>/<int:month>/<int:day>/<slug:thread>/',
		views.thread_detail, name='thread_detail'),

	path('thread_comment/<int:id>/',
		views.thread_comment, name='thread_comment'),

	path('comment_delete/<int:id>/',
		views.comment_delete, name='comment_delete'),

	path('thread_create/<int:id>/',
		views.thread_create, name='thread_create'),

	path('thread_edit/<int:id>/',
		views.thread_edit, name='thread_edit'),

	path('thread_delete/<int:id>/',
		views.thread_delete, name='thread_delete'),

	path('search/', views.site_search, name='site_search'),
]