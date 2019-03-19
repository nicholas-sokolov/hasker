import datetime
from time import time

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from users.models import User


def gen_slug(s):
    new_slug = slugify(s)
    return f'{new_slug}-{int(time())}'


class Tag(models.Model):
    word = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, help_text="Enter the title of your question")
    content = models.CharField(max_length=1000, blank=False, help_text="Enter the question text")
    created_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def was_published_recently(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False, help_text="Enter the answer text that you want displayed")
    created_date = models.DateField(auto_now=True)
    is_right_answer = models.BooleanField(default=False)

    # TODO: author, tags

    def __str__(self):
        return self.content
