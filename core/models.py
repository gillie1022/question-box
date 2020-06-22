from django.db import models
from users.models import User
from django.db.models import Q
from django.contrib.postgres.search import SearchVector


class Question(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="questions"
    )
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=500)
    asked_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    starred_by = models.ManyToManyField(to=User, related_name="starred_questions")
    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, related_name="answers"
    )
    question = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, related_name="answers"
    )
    body = models.CharField(verbose_name="Response", max_length=500)
    answered_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    marked_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.body

def search_questions_for_user(user, search_term):
    questions = Question.objects.all()
    return questions \
        .annotate(search=SearchVector('title', 'body', 'answers__body')) \
        .filter(search=search_term) \
        .distinct('pk')