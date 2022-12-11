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

@csrf_exempt
def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            u = request.POST['username']#.get('username')
            p = request.POST['password']#.get('password')
            user = authenticate(username = u, password = p)
            if user.is_staff and user is not None:
                login(request, user)
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

        return HttpResponseRedirect(f'/quiz/seltitle/public/{sub}/')
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
        # print('yes\n')
    if request.method == 'POST':
        s = request.POST.get('subject')
        Subjects.objects.create(subject = s)
        return render(request, 'staff page.html')
    return render(request, 'add_sub.html')

def filter_result(request):
    s = Questions.objects.all().values()
    # s = ResultForm()
    print(s)

    return render(request, 'quiz.html', {'items':s})

@login_required
def pre_creator(request):
    if request.method == 'POST':
        form = EvaluatorForm
        key = request.POST.get('key').strip()
        is_private = request.POST.get('private')
        sub = request.POST.get('sub')
        title = request.POST.get('title')

        if is_private == 'on' and (key == '' or len(str(key)) != 4):
            return render(request, 'evaluator.html', {'warning': 'enter the key(max legnth 4)', 'form': form})
        elif len(str(key)) > 0:
            return render(request, 'evaluator.html', {'warning': 'check the "is private"', 'form': form})
        key = 'public' if key == '' else key
        return HttpResponseRedirect(f'/quiz/disp/{key}/{sub}/{title}/')
    return render(request, 'evaluator.html', {'form':EvaluatorForm, 'create':1})

@login_required
def create_question(request, key, sub, title):
    form = Form()
    if request.method == 'POST':
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
        Questions.objects.create(sub_id=sub, question = q, option1=o1, option2=o2, option3=o3, option4=o4, answer=ans, public = p, key=key, title=title)
        return render(request, 'users_list.html', {'form': form, 'key':key, 'sub':sub, 'title':title})
    return render(request, 'users_list.html', {'form': form, 'key':key, 'sub':sub, 'title':title})

def select_title(request, sub=None,  key=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        return HttpResponseRedirect(f'/quiz/attempt/{key}/{sub}/{title}/')

    title = Questions.objects.filter(sub_id=sub).values('title').distinct()
    return render(request, 'title.html', {'title': title, 'sub': sub, 'key': key})


@login_required
@csrf_exempt
def attempt_quiz(request, sub=None,  key=None, title=None):
    # questions = Questions.objects.filter(key=key).values()
    if key == 'public':
        # if request.method == 'POST':
            # title = request.POST.get('title')
            questions = Questions.objects.filter(sub_id=sub, title=title, key='public').values()
            length = len(questions)
            submitted = request.POST.get('submit')
            if submitted == 'Submit':
                res = []
                for i in range(length):
                    ans = 'q' + str(i + 1)
                    print(ans, request.POST.get(ans))
                    res.append(request.POST.get(ans))
                score = evaluate(res, list(questions))
                print(res, questions)
                user_id = User.objects.get(id=request.user.id)
                sub_id = Subjects.objects.get(subject=sub)
                res1 = Results.objects.create(name=request.user, score=score, subject=sub_id)
                return render(request, 'user_page.html', {'score': score, 'length':length})

            if len(questions)>0:
                return render(request, 'user_page.html', {'ques': questions, 'count':len(questions)})
            return render(request, 'user_page.html', {'error':'no questions to display'})
        # else:
        #     return HttpResponseRedirect(f'/quiz/seltitle/{key}/{sub}/')
    questions = Questions.objects.filter(sub_id='sub', key=key).values()
    length = len(questions)
    submitted = request.POST.get('submit')
    if submitted == 'Submit':
        res = []
        for i in range(length):
            ans = 'q' + str(i + 1)
            res.append(request.POST.get(ans))
        score = evaluate(res, list(questions))
        return render(request, 'user_page.html', {'score': score, 'length':length})

    if len(questions)>0:
        return render(request, 'user_page.html', {'ques': questions, 'count': len(questions)})
    return render(request, 'user_page.html', {'error':'no questions to display'})

# @login_required
@csrf_exempt
def tester(request):
    res = User.objects.get(id = request.user.id)
    print(res)
    res1 = Results.objects.create(name=res, score=20)
    items = Results.objects.all().values()
    if request.method == 'POST':
        form = ResultForm()
        print('---------------')
        n = request.POST.get('name')
        s = request.POST.get('score')
        print(n,s)
    # print(res)
    form = ResultForm()
    items = User.objects.get(id=24)
    return render(request, 'tester.html', {'items':items, 'form':form})

def evaluate(result_array, q_list):#result_array, q_list):
    # result_array = ['1','3','4']
    # q_list = list(Questions.objects.filter(key=str('public')).values())
    score = 0
    for i in range(len(result_array)):
        if q_list[i]['answer'] == result_array[i]:
            score += 1
    return score
