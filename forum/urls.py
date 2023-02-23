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

	path('forums/<int:id>/',
		views.thread_list, name='thread_list'),

	path('thread/<int:year>/<int:month>/<int:day>/<slug:thread>/',
		views.thread_detail, name='thread_detail'),

	path('thread_comment/<int:id>/',
		views.thread_comment, name='thread_comment'),

	path('thread_create/<int:id>/',
		views.thread_create, name='thread_create'),

	path('thread_edit/<int:id>/',
		views.thread_edit, name='thread_edit'),
]