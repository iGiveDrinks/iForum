from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity

from .forms import ForumCreateForm, ThreadCreateForm, CommentForm, SearchForm
from .models import Forum, Thread, Comment


# Create your views here.
def index(request):
	forums = Forum.public.all()

	paginator = Paginator(forums, 16)
	page_number = request.GET.get('page', 1)
	try:
		forums = paginator.page(page_number)
	except PageNotAnInteger:
		forums = paginator.page(1)
	except EmptyPage:
		forums = paginator.page(paginator.num_pages)

	return render(request, 'forum/index.html',
								{'forums': forums,})


@login_required
def forum_create(request):
	if request.method != 'POST':
		form = ForumCreateForm()
	else:
		form = ForumCreateForm(data=request.POST)
		if form.is_valid():
			form_create = form.save(commit=False)
			form_create.author = request.user
			form_create.slug = slugify(form_create.title)
			form_create.save()
			return redirect('forum:index')

	return render(request, 'forum/forum_create.html',
								{'form': form})


@login_required
def forum_edit(request, id):
	forum = get_object_or_404(Forum, id=id)

	if forum.author != request.user:
		raise Http404
	if request.method != 'POST':
		form = ForumCreateForm(instance=forum)
	else:
		form = ForumCreateForm(instance=forum,
								data=request.POST)
		if form.is_valid:
			form.save()
			return redirect('forum:thread_list', id=id)

	return render(request, 'forum/forum_edit.html',
								{'forum': forum,
								'form': form})


@login_required
def forum_delete(request, id):
	forum = get_object_or_404(Forum, id=id)

	if request.method == 'POST':
		forum.delete()
		return redirect('forum:index')

	return render(request, 'forum/forum_delete.html',
								{'forum': forum})


def thread_list(request, id):
	forum = Forum.objects.get(id=id)
	threads = forum.threads.all()

	paginator = Paginator(threads, 20)
	page_number = request.GET.get('page', 1)
	try:
		threads = paginator.page(page_number)
	except PageNotAnInteger:
		threads = paginator.page(1)
	except EmptyPage:
		threads = paginator.page(paginator.num_pages)

	return render(request, 'forum/thread_list.html',
								{'forum': forum,
								'threads': threads})


def thread_detail(request, year, month, day, thread):
	thread = get_object_or_404(Thread,
								status=Thread.Status.PUBLISHED,
								slug=thread,
								publish__year=year,
								publish__month=month,
								publish__day=day)
	forum = thread.forum
	comments = thread.comments.filter(active=True)
	form = CommentForm()

	paginator = Paginator(comments, 20)
	page_number = request.GET.get('page', 1)
	try:
		comments = paginator.page(page_number)
	except PageNotAnInteger:
		comments = paginator.page(1)
	except EmptyPage:
		comments = paginator.page(paginator.num_pages)

	thread_tag_ids = thread.tags.values_list('id', flat=True)
	similar_threads = Thread.published.filter(tags__in=thread_tag_ids)\
										.filter(forum=forum)\
										.exclude(id=thread.id)
	similar_threads = similar_threads.annotate(same_tags=Count('tags'))\
										.order_by('-same_tags', '-publish')[:6]

	return render(request, 'forum/thread_detail.html',
								{'thread': thread,
								'forum': forum,
								'comments': comments,
								'form': form,
								'similar_threads': similar_threads})


@login_required
@require_POST
def thread_comment(request, id):
	thread = get_object_or_404(Thread, id=id)
	comment = None
	form = CommentForm(data=request.POST)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.thread = thread
		comment.author = request.user
		comment.save()
		return redirect(thread.get_absolute_url())


@login_required
def comment_delete(request, id):
	comment = get_object_or_404(Comment, id=id)
	thread = comment.thread
	forum = thread.forum

	if comment.author != request.user:
		raise Http404
	if request.method == 'POST':
		comment.delete()
		return redirect(thread.get_absolute_url())

	return render(request, 'forum/comment_delete.html',
								{'comment': comment,
								'thread': thread,
								'forum': forum})


@login_required
def thread_create(request, id):
	forum = get_object_or_404(Forum, id=id)

	if request.method != 'POST':
		form = ThreadCreateForm()
	else:
		form = ThreadCreateForm(data=request.POST)
		if form.is_valid():
			thread_create = form.save(commit=False)
			thread_create.forum = forum
			thread_create.author = request.user
			thread_create.slug = slugify(thread_create.title)
			thread_create.save()
			form.save_m2m()
			return redirect('forum:thread_list', id=id) 

	return render(request, 'forum/thread_create.html',
								{'forum': forum,
								'form': form})


@login_required
def thread_edit(request, id):
	thread = get_object_or_404(Thread, id=id)
	forum = thread.forum

	if thread.author != request.user:
		raise Http404
	if request.method != 'POST':
		form = ThreadCreateForm(instance=thread)
	else:
		form = ThreadCreateForm(instance=thread, 
								data=request.POST)
		if form.is_valid:
			form.save()
			return redirect(thread.get_absolute_url())

	return render(request, 'forum/thread_edit.html',
								{'thread': thread,
								'forum': forum,
								'form': form})


@login_required
def thread_delete(request, id):
	thread = get_object_or_404(Thread, id=id)
	forum_id = thread.forum.id
	forum = thread.forum

	if thread.author != request.user:
		raise Http404
	if request.method == 'POST':
		thread.delete()
		return redirect('forum:thread_list', id=forum_id)

	return render(request, 'forum/thread_delete.html',
								{'thread': thread,
								'forum': forum})


def site_search(request):
	form = SearchForm()
	query = None
	results = []

	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Thread.published.annotate(
				similarity=TrigramSimilarity('title', query),
			).filter(similarity__gt=0.1,).order_by('-similarity')

	return render(request, 'forum/site_search.html',
								{'form': form,
								'query': query,
								'results': results})