from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('polls/', views.QuestionsView.as_view(), name='questions'),
    path('question/<int:question_id>/', views.DisplayQuestionView.as_view(), name='question'),
    path('question/<int:question_id>/results/', views.QuestionResults.as_view(), name='results'),
    path('question/<int:question_id>/vote/', views.VoteView.as_view(), name='vote'),
]