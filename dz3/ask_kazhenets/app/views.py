from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ProfileEditForm
from django.core.paginator import Paginator
from .models import Question, Tag, Answer, User, Profile
from django.contrib import messages
from django import forms
from django.urls import reverse


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
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_avatar = request.FILES.get('avatar')
        if new_username and new_username != user.username:
            user.username = new_username
        if new_email and new_email != user.email:
            user.email = new_email
        user.save()
        if new_avatar:
            profile.avatar = new_avatar
        profile.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('app:usersettings')
    initial_data = {
        'username': user.username,
        'email': user.email,
    }

    return render(request, 'usersettings.html', {
        'username': user.username,
        'email': user.email,
        'avatar_url': profile.avatar.url if profile.avatar else None,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })


@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            tags_str = request.POST.get('tags', '')
            tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)

            messages.success(request, 'Your question has been posted!')
            return redirect('app:question', question_id=question.id)
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {
        'form': form,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })


@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
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

