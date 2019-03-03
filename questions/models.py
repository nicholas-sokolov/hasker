import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.EmailField(max_length=50, blank=False, help_text="Enter your email")
    login = models.CharField(max_length=20, blank=False, help_text="Enter your login")
    password = models.CharField(max_length=50, blank=False, help_text="Enter your password")
    profile_photo = models.ImageField()
    register_date = models.DateField(auto_now=True)


class Question(models.Model):
    author = models.CharField(max_length=20)
    title = models.CharField(max_length=200, blank=False, help_text="Enter the title of your question")
    content = models.CharField(max_length=1000, blank=False, help_text="Enter the question text")
    created_date = models.DateTimeField(auto_now=True)
    # TODO: author, tags

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=1)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False, help_text="Enter the answer text that you want displayed")
    author = models.CharField(max_length=20, blank=False)
    created_date = models.DateField(auto_now=True)
    is_right_answer = models.BooleanField(default=False)
    # TODO: author, tags

    def __str__(self):
        return self.content


class Tag(models.Model):
    word = models.CharField(max_length=20)
