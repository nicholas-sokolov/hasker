from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.http import is_safe_url
from django.views import generic

from questions.models import Question, Answer
from .forms import UserProfileForm, UserForm
from .models import UserProfile


def profile_view(request, slug):
    if request.method == 'GET':
        profile = get_object_or_404(UserProfile, user=request.user)
        question_count = Question.objects.filter(author=profile.user).count()
        answer_count = Answer.objects.filter(author=profile.user).count()
        context = {
            'profile': profile,
            'question_count': question_count,
            'answer_count': answer_count
        }
        return render(request, 'accounts/profile.html', context)


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


@login_required(login_url='/users/login')
def custom_logout(request):
    logout(request)
    return redirect('questions:index')


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
