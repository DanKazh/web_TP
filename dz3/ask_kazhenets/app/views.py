from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Tag, Answer, User, Profile

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

def login(request):
    return render(request, 'login.html', {
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

def signup(request):
    return render(request, 'signup.html', {
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

def ask(request):
    return render(request, 'ask.html', {
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })

def user_settings(request):
    return render(request, 'usersettings.html', {
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': User.best_members.get_best_members(),
    })