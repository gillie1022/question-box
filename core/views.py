from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return redirect(to='question_list')

    return render(request, 'core/home.html')

def list_questions(request):
    questions = Question.objects.all()
    return render(request, "questions/list_questions.html", {"questions": questions,})

def list_answers(request, question_pk):
    pass

@login_required
def ask_question(request):
    pass

@login_required
def answer_question(request, question_pk):
    pass

