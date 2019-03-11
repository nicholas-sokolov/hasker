from django.contrib.auth import get_user_model
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.utils.http import is_safe_url
from django.views import generic

from questions.models import Question
from .forms import UserProfileForm, UserForm
from .models import UserProfile


class ProfileView(generic.DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    slug_field = 'username'

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        print(UserProfile.objects.all())
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(author=self.kwargs.get('username'))


class SignUpView(generic.base.View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = UserProfileForm()
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'registration/register.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
        else:
            print(user_form.errors, profile_form.errors)
        return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})


def custom_logout(request):
    logout(request)
    return render(request, 'questions/index.html', {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                redirect_to = request.GET.get('next')
                if is_safe_url(redirect_to, request.get_host()):
                    return redirect(redirect_to)
                else:
                    return redirect('questions:index')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'registration/login.html', {})
