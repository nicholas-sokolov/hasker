from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .models import Question
from .forms import NewQuestion


def index(request):
    latest_question_list = Question.objects.order_by('-created_date')[:20]
    context = {
        'latest_question_list': latest_question_list,
    }

    return render(request, 'questions/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'questions/detail.html', {'question': question})


def new_question(request):
    if request.method == 'POST':
        form = NewQuestion(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.created_date = timezone.now()
            question.save()
            return redirect('questions:detail', question_id=question.pk)
    else:
        form = NewQuestion()
    return render(request, 'questions/new_question.html', {'form': form})
