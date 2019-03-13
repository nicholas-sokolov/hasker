from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views import generic

from .forms import NewQuestion, AnswerForm
from .models import Question


class QuestionListView(generic.ListView):
    template_name = 'questions/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 20

    def get_queryset(self):
        """ Return last 20 published questions """
        return Question.objects.order_by('-created_date')


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'questions/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Question, pk=self.kwargs.get('pk'))


def view_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user.username
            answer.save()
            return redirect(request.path)
        return render(request, 'questions/detail.html', {'question': question})
    else:
        return render(request, 'questions/detail.html', {'question': question})


@login_required(redirect_field_name='next', login_url='/users/login')
def ask_question(request):
    if request.method == 'POST':
        form = NewQuestion(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.created_date = timezone.now()
            question.save()
            return redirect('questions:detail', question_id=question.pk)
        else:
            return render(request, 'questions/new_question.html', {'form': form, 'error': 'Not valid'})
    else:
        form = NewQuestion()
        return render(request, 'questions/new_question.html', {'form': form})
