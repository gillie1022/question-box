from django.db import models
from users.models import User


class Question(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name="answers")
    body = models.CharField(max_length=500)

    def __str__(self):
        return self.body