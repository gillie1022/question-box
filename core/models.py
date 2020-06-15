from django.db import models
from django_markdown.models import MarkdownField
# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(to=User, on_delete=CASCADE, related_name="questions")
    title = models.CharField(max_length=255)
    body = MarkdownField()

class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=CASCADE, related_name="answers")
    body = MarkdownField()