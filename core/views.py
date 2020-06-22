from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Answer, search_questions_for_user
from .forms import QuestionForm, AnswerForm
from django.http import JsonResponse
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
    is_user_starred = request.user.is_starred_question(question)
    return render(request, "core/question_detail.html", {"question": question, "is_user_starred": is_user_starred,
    })

def search_questions(request):
    query = request.GET.get('q')

    if query is not None:
        questions = search_questions_for_user(request.user, query)
    else:
        questions = None
    
    return render(request, 'core/search_questions.html', {
        'query': query,
        'questions': questions,
    })

@login_required
@csrf_exempt
def toggle_star_question(request, question_pk):
    questions = Question.objects.all()
    question = get_object_or_404(questions, pk=question_pk)

    if request.user.is_starred_question(question):
        request.user.starred_questions.remove(question)
        return JsonResponse({"isStarred": False})
    else:
        request.user.starred_questions.add(question)
        return JsonResponse({"isStarred": True})

@login_required
@csrf_exempt
def mark_answer_correct(request, question_pk, answer_pk):
    questions = Question.objects.all()
    question = get_object_or_404(questions, pk=question_pk)
    answers = question.answers.all()
    answer = get_object_or_404(answers, pk=answer_pk)

    if answer.marked_correct == True:
        answer.marked_correct=False
        answer.save()
        return JsonResponse({"markedCorrect": False})
    else:
        answer.marked_correct=True
        answer.save()
        return JsonResponse({"markedCorrect": True})

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
            answer.author = request.user
            answer.save()
            return redirect(to="question_detail", question_pk=question.pk)
    else:
        form = AnswerForm()

    return render(request, "core/answer_question.html", {"form": form, "question": question})

@login_required
def delete_question(request, question_pk):
    question = get_object_or_404(request.user.questions, pk=question_pk)

    if request.method == "POST":
        question.delete()
        return redirect(to='question_list')

    return render(request, "core/delete_question.html", {"question": question})


@login_required
def user_profile(request):
    your_questions = request.user.questions.all()
    starred_questions = request.user.starred_questions.all()
    return render(request, "core/user_profile.html", {"your_questions": your_questions, "starred_questions": starred_questions})