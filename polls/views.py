from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Question, Vote
from django.contrib import messages
from users.utils import paginateObjects


class QuestionsView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        questions = Question.objects.all()
        custom_range, questions = paginateObjects(request, questions, 3)
        context = {'questions': questions, 'profile': profile, 'custom_range': custom_range}
        return render(request, 'polls/questions.html', context)


class DisplayQuestionView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        profile = request.user.profile
        question = get_object_or_404(Question, pk=question_id)
        return redirect(reverse('polls:question', kwargs={'question_id': question.pk}))


class QuestionResults(LoginRequiredMixin, View):
    def get(self, request, question_id):
        profile = request.user.profile
        question = get_object_or_404(Question, pk=question_id)
        labels = []
        data = []
        votes = question.choice_set.select_related('question').all() 
        for item in votes:
            labels.append(item.name)
            data.append(item.votes)
        context = {'question': question, 
        'profile': profile, 
        'labels': labels, 
        'data': data}    
        return render(request, 
            'polls/results.html', context)


class VoteView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        profile = request.user.profile
        question = get_object_or_404(Question, pk=question_id)
        try:
            user_choice = question.choice_set.get(pk=request.POST['choice'])
            if not question.user_voted(request.user):
                messages.error(request, 
                    'You have already voted in this poll.')
                return render(request, 
                    'polls/question.html',  
                    {'question': question,'profile': profile})
            if user_choice:
                user_choice.votes += 1
                user_choice.save()
                vote = Vote(user=request.user, question=question, choice=user_choice)
                vote.save()
                return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        except (KeyError, UnboundLocalError):
            messages.error(request, 'You did not select a choice!')
            return render(request, 'polls/question.html', {'question': question})
        return render(request, 
            'polls/results.html', 
            {'question': question, 'profile': profile})