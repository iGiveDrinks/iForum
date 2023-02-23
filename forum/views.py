from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import ForumCreateForm, ThreadCreateForm, CommentForm
from .models import Forum, Thread, Comment

# Create your views here.
def index(request):
	forums = Forum.public.all()

	paginator = Paginator(forums, 32)
	page_number = request.GET.get('page', 1)
	try:
		forums = paginator.page(page_number)
	except PageNotAnInteger:
		forums = paginator.page(1)
	except EmptyPage:
		forums = paginator.page(paginator.num_pages)

	return render(request, 'forum/index.html',
								{'forums': forums})


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

	return render(request, 'forum/thread_detail.html',
								{'thread': thread,
								'forum': forum,
								'comments': comments,
								'form': form})


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