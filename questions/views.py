from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.db.models import Q

from .forms import QuestionForm, AnswerForm
from .models import Question, Tag
from .utils import ObjectCreateMixin, ObjectDetailMixin


def questions_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        questions = Question.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    else:
        questions = Question.objects.all()
    paginator = Paginator(questions, 20)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return render(request, 'questions/index.html', context=context)


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
        # TODO: processing ov votes
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


def get_vote_view(request):
    return print(request.POST['text'])
