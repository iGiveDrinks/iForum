from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['text', 'about',]
		labels = {'text': 'Community name...',
				'about': 'Whats your topic about?',}

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['title', 'text']
		labels = {'title': 'Title', 'text': 'Type here...',}
		widgets = {'text': forms.Textarea(attrs={'cols': 80})}