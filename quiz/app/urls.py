from django.urls import path
from .views import *
urlpatterns = [
    path('',home, name='home'),
    path('register/', register, name='register'),
    path('logout/', out, name='logout'),
    path('sub/', subjects, name='subjects'),
    path('addsub/', create_subject, name='createsub'),
    path('precreatesub/', pre_creator, name='precreator'),
    path('result/', filter_result, name = 'result'),
    path('disp/<str:key>/<str:sub>/<str:title>/', create_question, name='display'),
    path('evaluator/', evaluator, name='evaluator'),
    # path('attempt/<str:key>/<str:sub>/', attempt_quiz, name='attempt'),
    path('attempt/<str:key>/<str:sub>/<str:title>/', attempt_quiz, name='attempt1'),
    path('seltitle/<str:key>/<str:sub>/', select_title, name='select title'),
    path('test/', tester, name='tester'),
    path('eval/', evaluate, name='eval'),
]