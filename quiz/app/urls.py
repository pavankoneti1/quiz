from django.urls import path
from .views import *
urlpatterns = [
    path('',home, name='home'),
    path('register/', register, name='register'),
    path('logout/', out, name='logout'),
    path('sub/', subjects, name='subjects'),
    path('addsub/', create_subject, name='createsub'),
    path('precreatesub/', pre_creator, name='precreator'),
    path('subject/<data>/', filter_data, name = 'filter_data'),
    path('disp/<str:key>/<str:sub>/', create_question, name='display'),
    path('evaluator/', evaluator, name='evaluator'),
    path('attempt/<str:key>/<str:sub>/', attempt_quiz, name='attempt'),
    path('test/', tester, name='tester'),
    path('update/', updater, name = 'update'),
    path('eval/', evaluate, name='eval'),
]