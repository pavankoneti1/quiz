from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *
# Create your views here.

def home(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request.POST)
        # form =
        # print(form.is_valid())
        # if form.is_valid():
            u = request.POST['username']#.get('username')
            p = request.POST['password']#.get('password')
            print(u, p)
            user = authenticate(username = u, password = p)
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/sub')
            else:
                return render(request, 'home.html', {'error':'invalid credentials'})#, 'form': AuthenticationForm})
        # else:
        #     print('error')
        #     messages.error(request, 'invalid credentials')
    return render(request, 'home.html')#, {'form': AuthenticationForm()})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return HttpResponseRedirect('/quiz')
    form = UserCreationForm()
    return render(request, 'register.html', {'form':form})

def subjects(request):
    sub = Subjects.objects.all().values()
    return render(request, 'subjects.html', {'subjects':sub})

def create_subject(request):
    if request.method == 'POST':
        s = request.POST.get('subject')
        Subjects.objects.create(subject = s)
        return HttpResponseRedirect('/quiz/')
    return render(request, 'add_sub.html')

def filter_data(request, data):
    s = Questions.objects.get(sub = data)
    return render(request, 'quiz.html', {'items':s})

def create_question(request):
    form = Form()
    if request.method == 'POST':
        s = request.POST['sub']
        q = request.POST['question']
        o1 = request.POST['option1']
        o2 = request.POST['option2']
        o3 = request.POST['option3']
        o4 = request.POST['option4']
        p = True if request.POST['public'] == 'on' else False
        k = request.POST['key'] if request.POST['key'].isalnum() else 0
        Questions.objects.create(sub_id=s, question = q, option1=o1, option2=o2, option3=o3, option4=o4, public = p, key=k)
        return render(request, 'users_list.html', {'ques': Questions.objects.all().values()})
    return render(request, 'users_list.html', {'form': form})

def tester(request):
    items = User.objects.values_list('id', 'username', 'password')
    print(items)
    return render(request, 'tester.html', {'items':items})

def attempt_quiz(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        questions = Questions.objects.get(key = key)
