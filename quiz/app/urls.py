from django.urls import path
from .views import *
urlpatterns = [
    path('',home, name='home'),
    path('register/', register, name='register'),
    path('sub/', subjects, name='subjects'),
    path('addsub/', create_subject, name='createsub'),
    path('subject/<data>/', filter_data, name = 'filter_data'),
    path('disp', create_question, name='display'),
    path('test/', tester, name='tester'),
]