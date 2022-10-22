from django.urls import path
from .views import *

urlpatterns=[
    path('', home, name='home'),
    path('user/', users, name='users'),
    path('create_user/', create_user, name='create'),
    path('login/', login_system, name = 'login'),

]