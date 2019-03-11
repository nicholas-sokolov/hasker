from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.QuestionListView.as_view(), name='index'),
    path('ask/', views.ask_question, name='new_question'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='detail'),
]
