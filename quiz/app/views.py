from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from .forms import *
# Create your views here.

# def login_required(func):
#     if user.is_authenticated():
#         return func
#     return home

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            u = request.POST['username']#.get('username')
            p = request.POST['password']#.get('password')
            user = authenticate(username = u, password = p)
            if user.is_staff and user is not None:
                print("---------------'i'm here")
                return render(request, 'staff page.html')
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('evaluator/')
            return render(request, 'home.html', {'form': AuthenticationForm(), 'error':'invalid credentials'})#, 'form': AuthenticationForm})
        return render(request, 'home.html', {'form': AuthenticationForm()})

    return render(request, 'home.html', {'form': AuthenticationForm()})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        staff = request.POST.get('staff')
        staff = True if staff == 'on' else False
        print(staff)
        User.objects.create_user(username=username, password=password, is_staff = staff)
        return HttpResponseRedirect('/quiz')
    form = UserCreationForm()
    return render(request, 'register.html', {'form':form})

def out(request):
    print('i\'m loged out -------')
    logout(request)
    return HttpResponseRedirect('/quiz/')

def evaluator(request):
    form = EvaluatorForm()
    if request.method == 'POST':
        key = request.POST.get('key').strip()
        is_private = request.POST.get('private')
        sub = request.POST.get('sub')

        if is_private == 'on' and (key == '' or len(str(key))!=4 ):
            return render(request, 'evaluator.html', {'warning':'enter the key(max legnth 4)', 'form':form})
        elif len(str(key)) > 0 and is_private != 'on':
            return render(request, 'evaluator.html', {'warning':'check the "is private"', 'form':form})
        elif len(key) == 4 and is_private == 'on':
            return HttpResponseRedirect(f'/quiz/attempt/{key}/{sub}/')
        key = 'public' if key== '' else key

        return HttpResponseRedirect(f'/quiz/attempt/public/{sub}/')
    return render(request, 'evaluator.html', {'form':form})

def subjects(request):
    sub = Subjects.objects.all().values()
    if request.method == 'POST':
        check = request.POST.get('check')
        sub = request.POST.get('sub')
        if check == 'on':
            return render(request, 'key.html')
        return HttpResponseRedirect('/quiz/attempt/subject/public/')
    return render(request, 'subjects.html', {'subjects':sub})

# @login_required
def create_subject(request):
    print(request.user, 'hi')
        # print('yes\n')
    if request.method == 'POST':
        s = request.POST.get('subject')
        Subjects.objects.create(subject = s)
        return render(request, 'staff page.html')
    return render(request, 'add_sub.html')

def filter_data(request, data):
    s = User.objects.filter(is_staff=True).values()
    if request.method == 'POST':
        check = request.POST.get('check')
        if check == 'on':
            pass

    return render(request, 'quiz.html', {'items':s})

@login_required
def pre_creator(request):
    if request.method == 'POST':
        form = EvaluatorForm
        key = request.POST.get('key').strip()
        is_private = request.POST.get('private')
        sub = request.POST.get('sub')

        if is_private == 'on' and (key == '' or len(str(key)) != 4):
            return render(request, 'evaluator.html', {'warning': 'enter the key(max legnth 4)', 'form': form})
        elif len(str(key)) > 0:
            return render(request, 'evaluator.html', {'warning': 'check the "is private"', 'form': form})
        key = 'public' if key == '' else key
        return HttpResponseRedirect(f'/quiz/disp/{key}/{sub}/')
    return render(request, 'evaluator.html', {'form':EvaluatorForm, 'create':1})

@login_required
def create_question(request, key, sub):
    form = Form()
    if request.method == 'POST':
        print('----------hi')
        q = request.POST.get('question')
        o1 = request.POST.get('option1')
        o2 = request.POST.get('option2')
        o3 = request.POST.get('option3')
        o4 = request.POST.get('option4')
        ans = request.POST.get('answer')
        button = request.POST.get('but')
        if button == 'exit':
            return render(request, 'staff page.html')

        p = True if key == '' else False
        d = {
            '1': o1,
            '2' : o2,
            '3' :o3,
            '4' :o4,
        }
        ans = d[ans]
        Questions.objects.create(sub_id=sub, question = q, option1=o1, option2=o2, option3=o3, option4=o4, public = p, key=key)
        return render(request, 'users_list.html', {'form': form, 'key':key, 'sub':sub})
    return render(request, 'users_list.html', {'form': form, 'key':key, 'sub':sub})

@login_required
@csrf_exempt
def attempt_quiz(request, sub=None,  key=None):
    print(key)
    questions = Questions.objects.filter(key=key).values()
    if key == 'public':
        if request.method == 'POST':
            title = request.POST.get('title')
            questions = Questions.objects.filter(sub_id=sub, title=title, key='public').values()
            if len(questions)>0:
                submitted = request.POST.get('submit')
                if submitted == 'Submit':
                    res = []
                    for i in range(len(questions)):
                        ans = 'q' + str(i + 1)
                        res.append(request.POST.get(ans))
                    score = evaluate(res, list(questions))
                    return render(request, 'user_page.html', {'score': score})
                return render(request, 'user_page.html', {'ques': questions, 'count':len(questions)})
            return render(request, 'user_page.html', {'error':'no questions to display'})
        else:
            title = Questions.objects.filter(sub_id=sub).values('title', 'sub_id')
            return render(request, 'title.html', {'title':title})

    questions = Questions.objects.filter(sub_id='sub', key=key).values()
    if len(questions)>0:
        submitted = request.POST.get('submit')
        if submitted == 'Submit':
            res = []
            for i in range(len(questions)):
                ans = 'q' + str(i + 1)
                res.append(request.POST.get(ans))
            score = evaluate(res, list(questions))
            return render(request, 'user_page.html', {'score': score})
        return render(request, 'user_page.html', {'ques': questions, 'count': len(questions)})
    return render(request, 'user_page.html', {'error':'no questions to display'})

# @login_required
def tester(request):
    print(request.user.is_authenticated)
    # items = User.objects.values_list('id', 'username', 'key')
    items = Questions.objects.filter(sub_id='maths').values('key')
    # print(type(items[0][0]))
    return render(request, 'tester.html', {'items':items})

def updater(request):
    q = Questions.objects.get(id=1)#.update(key = '1234')
    q.key = '1234'
    q.save()
    return HttpResponseRedirect('/quiz/test/')


def evaluate(result_array, q_list):#result_array, q_list):
    # result_array = ['1','3','4']
    # q_list = list(Questions.objects.filter(key=str('public')).values())
    score = 0
    for i in range(len(result_array)):
        if q_list[i]['answer'] == result_array[i]:
            score += 1
    return score
