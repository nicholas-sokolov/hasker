from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views import generic

from .forms import NewQuestion
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


class NewQuestionView(generic.base.View):
    def get(self, request, *args, **kwargs):
        form = NewQuestion()
        context = {'form': form}
        return render(request, 'questions/new_question.html', context)

    def post(self, request, *args, **kwargs):
        form = NewQuestion(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.created_date = timezone.now()
            question.save()
            return redirect('questions:detail', question_id=question.pk)


