from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    name = models.CharField(max_length=300)
    published = models.DateTimeField(auto_now_add=True)

    def user_voted(self, user):
        user_votes = user.vote_set.all()
        done = user_votes.filter(question=self)
        if done.exists():
            return False
        return True
    
    class Meta:
        ordering = ['published']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.name


class Choice(models.Model):
    question = models.ForeignKey(Question, 
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Variant'
        verbose_name_plural = 'Variants'

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, 
        on_delete=models.CASCADE)
    question = models.ForeignKey(Question, 
        on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, 
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return f'{self.question.name[:15]} - {self.choice.name[:15]} - {self.user.username}'

