from django import forms

from .models import Forum, Thread, Comment

class ForumCreateForm(forms.ModelForm):
	class Meta:
		model = Forum
		fields = ['title', 'body']
		labels = {'title': 'Forum title', 'body': ''}

class ThreadCreateForm(forms.ModelForm):
	class Meta:
		model = Thread
		fields = ['title', 'tags', 'body']
		labels = {'title': 'Thread title',
				'tags': 'Tags', 
				'body': ''}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']
		labels = {'body': 'Write your reply...'}

class SearchForm(forms.Form):
	query = forms.CharField()