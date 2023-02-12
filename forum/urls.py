from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
	# home page
	path('', views.index, name='index'),

	# topics and listed entries page
	path('topics/', views.topics, name='topics'),
	path('topics/<int:id>/', views.topic, name='topic'),

	# detailed entry page
	path('entry/<int:id>/', views.entry_detail, name='entry'),

	# page for adding a new topic and enrty
	path('new_topic/', views.new_topic, name='new_topic'),
	path('new_entry/<int:id>/', views.new_entry, name='new_entry'),
	path('edit_entry/<int:id>/', views.edit_entry, name='edit_entry')
]