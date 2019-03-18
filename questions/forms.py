from django import forms
from django.core.exceptions import ValidationError

from .models import Question, Answer, Tag


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['word']

        widgets = {
            'word': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_word(self):
        tag_list = self.cleaned_data['word'].split(',')
        if not tag_list or len(tag_list) > 3:
            raise ValidationError('Tags must be no more than 3')
        return tag_list
