from django import template
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.contrib.auth.models import User
import markdown

from ..models import Forum, Thread, Comment
from ..forms import SearchForm


register = template.Library()

@register.simple_tag
def total_users():
	return User.objects.count()


@register.simple_tag
def total_forums():
	return Forum.public.count()


@register.simple_tag
def total_threads():
	return Thread.published.count()

@register.simple_tag
def total_comments():
	return Comment.published.count()


@register.inclusion_tag('forum/latest_threads.html')
def show_latest_threads(count=5):
	latest_threads = Thread.published.order_by('-publish')[:count]
	return {'latest_threads': latest_threads}


@register.inclusion_tag('forum/latest_members.html')
def show_latest_members(count=5):
	latest_members = User.objects.order_by('-date_joined')[:count]
	return {'latest_members': latest_members}


@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))