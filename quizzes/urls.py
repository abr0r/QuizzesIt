from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
    path('quizzes/', views.QuizzesView.as_view(), name='quizzes'),
    path('<int:quiz_id>/', views.DisplayQuizView.as_view(), name='display_quiz'),
    path('<int:quiz_id>/questions/<int:question_id>', views.DisplayQuestionView.as_view(), name='display_question'),
    path('<int:quiz_id>/questions/<int:question_id>/grade/', views.GradeQuestionView.as_view(), name='grade_question'),
    path('results/<int:quiz_id>/', views.QuizResultsView.as_view(), name='quiz_results'),
]


