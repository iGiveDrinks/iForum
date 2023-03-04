from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import Forum, Thread


class ForumSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.8

	def items(self):
		return Forum.public.all()

	def location(self, item):
		return reverse('forum:index')

	def lastmod(self, obj):
		return obj.updated


class ThreadSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		return Thread.published.all()

	def lastmod(self, obj):
		return obj.updated