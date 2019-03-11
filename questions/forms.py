from django import forms

from .models import Question


class NewQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'content')
