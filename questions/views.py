from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm, AnswerForm
from .models import Question, Tag
from .utils import ObjectCreateMixin, ObjectDetailMixin


class QuestionListView(generic.ListView):
    template_name = 'questions/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 20

    def get_queryset(self):
        """ Return last 20 published questions """
        return Question.objects.order_by('-created_date')


class TagDetail(ObjectDetailMixin, generic.View):
    model = Tag
    template = 'questions/tag_detail.html'


class QuestionDetail(ObjectDetailMixin, generic.View):
    model = Question
    template = 'questions/detail.html'

    def post(self, request, slug):
        question = Question.objects.get(slug__iexact=slug)
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect(request.path)
        return render(request, self.template, {'form': form})


class QuestionCreate(LoginRequiredMixin, ObjectCreateMixin, generic.View):
    form_model = QuestionForm
    template = 'questions/new_question.html'
    redirect_field_name = 'next'
    login_url = '/users/login'

    def post(self, request):
        form = self.form_model(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.created_date = timezone.now()
            question.save()
            return redirect('questions:detail', slug=question.slug)
        return render(request, self.template, {'form': form})
