from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
	return render(request, 'forum/index.html')

def topics(request):
	topics = Topic.objects.order_by('-date_added')
	return render(request, 'forum/topics.html', {'topics': topics})

def topic(request, id):
	topic = Topic.objects.get(id=id)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'forum/topic.html', context)

def entry_detail(request, id):
	entry = get_object_or_404(Entry, id=id,)
	topic = entry.topic

	return render(request,
				'forum/detail.html',
				{'topic': topic, 'entry': entry})

@login_required
def new_topic(request):
	if request.method != 'POST':
		form = TopicForm()
	else:
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect('forum:topics')

	return render(request, 'forum/new_topic.html', {'form': form})

@login_required
def new_entry(request, id):
	topic = Topic.objects.get(id=id)

	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.author = request.user
			new_entry.save()
			return redirect('forum:topic', id=id)

	return render(request, 'forum/new_entry.html', {'topic': topic, 'form': form})

@login_required
def edit_entry(request, id):
	entry = Entry.objects.get(id=id)
	topic = entry.topic
	if entry.author != request.user:
		raise Http404

	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('forum:entry', id=id)

	return render(request, 'forum/edit_entry.html',
					{'entry': entry, 'topic': topic, 'form': form})