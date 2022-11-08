from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class Form(ModelForm):
    class Meta():
        model = Questions
        fields = ('question', 'option1', 'option2', 'option3', 'option4', 'answer')

class EvaluatorForm(ModelForm):
    class Meta:
        model = Questions
        fields = ('sub',)

class Users(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
