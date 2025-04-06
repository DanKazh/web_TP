from django.shortcuts import render
from django.http import HttpResponse
import random

all_tags = ['Python', 'C++', 'JavaScript', 'HTML', 'CSS', 'Assembly', 'C', 'C#']
def index(request):
    questions = []
    for i in range(1, 21):
        questions.append({
            'title': f'Question title {i}',
            'id': i,
            'text': f'This is text for question {i}. With supporting text below as a natural lead-in to additional content.',
            'answers_count': i % 5,
            'rating': random.randint(-10, 10),
            'tags': ['Python', 'C++'] if i % 2 else ['JavaScript', 'HTML']
        })
    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]

    return render(request, 'index.html', {
        'questions': questions,
        'page_title': 'New Questions',
        'popular_tags': popular_tags,
        'best_members': best_members,
    })


def hot(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': f'Hot question {i}',
            'id': i,
            'text': f'This is popular question {i}. With supporting text below as a natural lead-in to additional content.',
            'answers_count': i % 3,
            'rating': 50 - i,
            'tags': ['Python', 'CSS'] if i % 2 else ['JavaScript', 'C++']
        })

    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]

    return render(request, 'index.html', {'questions': questions, 'page_title': 'Hot Questions', 'popular_tags': popular_tags,
        'best_members': best_members})


def tag(request, tag_name):
    questions = []
    for i in range(1, 21):
        questions.append({
            'title': f'Question about {tag_name} {i}',
            'id': i,
            'text': f'This is question about {tag_name} {i}. With supporting text below as a natural lead-in to additional content.',
            'answers_count': i % 4,
            'rating': 20 - i,
            'tags': [tag_name, 'CSS'] if i % 2 else [tag_name, 'C++']
        })

    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]

    return render(request, 'tagged.html', {'questions': questions, 'tag_name': tag_name, 'popular_tags': popular_tags,
        'best_members': best_members})


def question(request, question_id):
    """Страница вопроса с ответами"""
    question_data = {
        'title': f'Question title {question_id}',
        'id': question_id,
        'text': f'This is text for question {question_id}. With supporting text below as a natural lead-in to additional content.',
        'rating': 15,
        'tags': ['Python', 'C++']
    }

    answers = []
    for i in range(1, 5):
        answers.append({
            'text': f'This is answer {i} to question {question_id}. Thats a tough question...',
            'rating': random.randint(0, 3),
            'is_correct': i == 1
        })

    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]

    return render(request, 'question.html', {
        'question': question_data,
        'answers': answers,
        'popular_tags': popular_tags,
        'best_members': best_members
    })


def login(request):
    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]
    """Форма входа"""
    return render(request, 'login.html', {'popular_tags': popular_tags,
        'best_members': best_members})


def signup(request):
    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]
    return render(request, 'signup.html', {'popular_tags': popular_tags,
                                          'best_members': best_members})


def ask(request):
    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]
    return render(request, 'ask.html', {'popular_tags': popular_tags,
                                          'best_members': best_members})


def user_settings(request):
    popular_tags = [
        {'name': 'Python'},
        {'name': 'Django'},
        {'name': 'JavaScript'},
        {'name': 'HTML'},
        {'name': 'CSS'},
        {'name': 'Bootstrap'},
    ]
    best_members = [
        {'username': 'Dr. Musk'},
        {'username': 'User700'},
        {'username': 'TPTeacher'},
        {'username': 'BMSTUstudent'},
    ]
    return render(request, 'usersettings.html', {'popular_tags': popular_tags,
                                          'best_members': best_members})