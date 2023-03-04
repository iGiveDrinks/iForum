from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.
class PublicManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Forum.Status.PUBLIC)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Thread.Status.PUBLISHED)\
                    .filter(status=Comment.Status.PUBLISHED)


class Forum(models.Model):

    class Status(models.TextChoices):
        PRIVATE = 'PR', 'Private'
        PUBLIC = 'PB', 'Public'

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date='created')
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                            related_name='forums')
    body = models.TextField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, 
                            default=Status.PUBLIC)
    active = models.BooleanField(default=True)

    objects = models.Manager() # Default manager
    public = PublicManager()

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread_list', 
                    args=[self.created.year,
                        self.created.month,
                        self.created.day,
                        self.slug])


class Thread(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique_for_date='publish')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE,
                            related_name='threads')
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                            related_name='threads')
    body = models.TextField(max_length=2000)
    upvote = models.IntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status.choices,
                            default=Status.PUBLISHED)
    pinned = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    tags = TaggableManager()


    objects = models.Manager() # Default manager
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    @property
    def short_title(self):
        return truncatechars(self.title, 30)

    @property
    def short_body(self):
        return truncatechars(self.body, 30)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread_detail',
                    args=[self.publish.year,
                        self.publish.month,
                        self.publish.day,
                        self.slug])


class Comment(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PB', 'Published'

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,
                            related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name='comments')
    body = models.TextField(max_length=2000)
    upvote = models.IntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, 
                            default=Status.PUBLISHED)
    active = models.BooleanField(default=True)

    objects = models.Manager() # Default manager
    published = PublishedManager()

    class Meta:
        ordering = ['publish']
        indexes = [
            models.Index(fields=['publish'])
        ]

    @property
    def short_body(self):
        return truncatechars(self.body, 30)

    def __str__(self):
        return self.body