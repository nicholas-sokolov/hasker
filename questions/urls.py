from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.QuestionListView.as_view(), name='index'),
    path('ask/', views.NewQuestionView.as_view(), name='new_question'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='detail'),
]
