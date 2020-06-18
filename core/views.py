from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return redirect(to='question_list')

    return render(request, 'core/home.html')

def list_questions(request):
    your_questions = request.user.questions.all()
    other_users_questions = [question for question in Question.objects.all() if not question in your_questions]
    return render(request, "core/list_questions.html", {"your_questions": your_questions, "other_users_questions": other_users_questions})

def question_detail(request, question_pk):
    question = get_object_or_404(Question.objects.all(), pk=question_pk)
    return render(request, "core/question_detail.html", {"question": question})


@login_required
def ask_question(request):
    if request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect(to='question_list')
    else:
        form = QuestionForm()

    return render(request, "core/ask_question.html", {"form": form})

@login_required
def edit_question(request, question_pk):
    question = get_object_or_404(request.user.questions, pk=question_pk)
    if request.method == "POST":
        form = QuestionForm(data=request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect(to='question_detail', question_pk=question.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, "core/edit_question.html", {"form": form, "question": question})


@login_required
def answer_question(request, question_pk):
    question = get_object_or_404(Question.objects.all(), pk=question_pk)
    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect(to="question_detail", question_pk=question.pk)
    else:
        form = AnswerForm()

    return render(request, "core/answer_question.html", {"form": form, "question": question})