from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from .forms import LoginForm, RegisterForm, ProfileEditForm
from django.core.paginator import Paginator
from .models import Question, Tag, Answer, User, Profile
from django.contrib import messages
from django import forms
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import QuestionLike, AnswerLike
from django.http import HttpResponse

def benchmark_view(request):
    return HttpResponse("<html><body><h1>Dynamic Test</h1></body></html>")

def paginate(request, queryset, per_page=5):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def index(request):
    questions = Question.objects.all().order_by('-tags')
    page = paginate(request, questions)
    return render(request, 'index.html', {
        'page': page,
        'questions': page.object_list,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members()
    })

def hot(request):
    questions = Question.objects.get_hot_questions()
    page = paginate(request, questions)
    return render(request, 'index.html', {
        'page': page,
        'questions': page.object_list,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

def newq(request):
    questions = Question.objects.get_new_questions()
    page = paginate(request, questions)
    return render(request, 'index.html', {
        'page': page,
        'questions': page.object_list,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

def tag(request, tag_name):
    questions = Question.objects.filter(tags__name=tag_name)
    page = paginate(request, questions)
    return render(request, 'tagged.html', {
        'questions': page,
        'tag_name': tag_name,
        'page': page,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    page = paginate(request, answers)
    return render(request, 'question.html', {
        'question': question,
        'answers': page,
        'page': page,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'app:index')
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })


def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app:index')
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {
        'form': form,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def user_settings(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('app:usersettings')
    else:
        form = ProfileEditForm(instance=profile, user=user)

    return render(request, 'usersettings.html', {
        'form': form,
        'username': user.username,
        'email': user.email,
        'avatar_url': profile.avatar.url if profile.avatar else None,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, user=request.user)
        if form.is_valid():
            question = form.save()
            messages.success(request, 'Your question has been posted!')
            return redirect('app:question', question_id=question.id)
    else:
        form = QuestionForm(user=request.user)

    return render(request, 'ask.html', {
        'form': form,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            answer = form.save()
            return redirect(f"{reverse('app:question', kwargs={'question_id': question.id})}#answer-{answer.id}")
    return redirect('app:question', question_id=question_id)

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Enter tags separated by commas")

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #F5F5DC'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'background-color: #F5F5DC', 'rows': 5}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'background-color: #F5F5DC', 'rows': 5}),
        }


@login_required
@require_POST
def vote_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    value = int(request.POST.get('value', 0))

    if request.user == question.author:
        return JsonResponse({'error': 'You cannot vote for your own question'}, status=400)

    vote, created = QuestionLike.objects.get_or_create(
        question=question,
        user=request.user,
        defaults={'value': value}
    )

    if not created:
        if vote.value == value:
            vote.delete()
            value = 0
        else:
            vote.value = value
            vote.save()


    question.rating = question.questionlike_set.aggregate(models.Sum('value'))['value__sum'] or 0
    question.save()

    return JsonResponse({
        'rating': question.rating,
        'user_vote': value
    })


@login_required
@require_POST
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    value = int(request.POST.get('value', 0))

    if request.user == answer.author:
        return JsonResponse({'error': 'You cannot vote for your own answer'}, status=400)

    vote, created = AnswerLike.objects.get_or_create(
        answer=answer,
        user=request.user,
        defaults={'value': value}
    )

    if not created:
        if vote.value == value:
            vote.delete()
            value = 0
        else:
            vote.value = value
            vote.save()


    answer.rating = answer.answerlike_set.aggregate(models.Sum('value'))['value__sum'] or 0
    answer.save()

    return JsonResponse({
        'rating': answer.rating,
        'user_vote': value
    })


@login_required
@require_POST
def mark_correct(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if request.user != answer.question.author:
        return JsonResponse({'error': 'Only question author can mark answers'}, status=403)


    is_checked = request.POST.get('is_checked', 'false') == 'true'

    if is_checked:

        Answer.objects.filter(question=answer.question).update(is_correct=False)

        answer.is_correct = True
    else:
        answer.is_correct = False

    answer.save()

    return JsonResponse({'is_correct': answer.is_correct})


def search(request):
    query = request.GET.get('q', '')

    if query:
        questions = Question.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(text__icontains=query)
        ).order_by('-created_at')
    else:
        questions = Question.objects.none()

    page = paginate(request, questions)

    return render(request, 'search_results.html', {
        'page': page,
        'questions': page.object_list,
        'query': query,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })
