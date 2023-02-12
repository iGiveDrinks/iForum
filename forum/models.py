from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
	text = models.CharField(max_length=40)
	about = models.TextField(max_length=100)
	slug = models.SlugField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.text

class Entry(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	title = models.CharField(max_length=40)
	slug = models.SlugField(max_length=250)
	text = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'entries'
		indexes = [
			models.Index(fields=['-date_added'])
		]

	def __str__(self):
		return self.title