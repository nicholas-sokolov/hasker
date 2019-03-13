from django import forms

from .models import Question, Answer


class NewQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'content')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
