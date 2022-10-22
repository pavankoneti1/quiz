from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class Form(ModelForm):
    class Meta():
        model = Questions
        fields = '__all__'

class Users(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
