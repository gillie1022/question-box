from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    pass


def list_questions(request):
    questions = request.user.questions.all()
    return render(request, "questions/list_questions.html", {"questions": questions,})

def question_detail(request, question_pk):
    pass

def add_question(request):
    pass

def add_answer(request, question_pk):
    pass

