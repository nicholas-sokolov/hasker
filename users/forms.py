from django import forms
from django.contrib.auth.admin import User

from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture', ]

        widgets = {
            'picture': forms.FileInput(attrs={'class': 'file-upload'}),
        }
