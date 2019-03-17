import datetime

from django.db import models
from django.utils import timezone

from users.models import User


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, help_text="Enter the title of your question")
    content = models.CharField(max_length=1000, blank=False, help_text="Enter the question text")
    created_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, blank=True)

    # TODO: author, tags

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=1)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False, help_text="Enter the answer text that you want displayed")
    created_date = models.DateField(auto_now=True)
    is_right_answer = models.BooleanField(default=False)

    # TODO: author, tags

    def __str__(self):
        return self.content


class Tag(models.Model):
    word = models.CharField(max_length=20)
