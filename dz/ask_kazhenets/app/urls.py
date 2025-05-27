from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('newq/', views.newq, name='newq'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('vote_question/<int:question_id>/', views.vote_question, name='vote_question'),
    path('answer/<int:answer_id>/vote/', views.vote_answer, name='vote_answer'),
    path('answer/<int:answer_id>/mark_correct/', views.mark_correct, name='mark_correct'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>/answer/', views.add_answer, name='add_answer'),
    path('usersettings/', views.user_settings, name='usersettings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
