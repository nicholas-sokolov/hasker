from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.QuestionListView.as_view(), name='index'),
    path('ask/', views.QuestionCreate.as_view(), name='new_question'),
    path('<str:slug>/', views.QuestionDetail.as_view(), name='detail'),
]
