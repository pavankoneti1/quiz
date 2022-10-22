from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .forms import *
# Create your views here.

def create_user(request):
    # User.objects.all().delete()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            u = request.POST.get('username')
            p = request.POST.get('password')
            User.objects.create_user(username=u, password=p)
            return HttpResponseRedirect('/log/user')
        # return render(request, 'register.html', {'form':form})

    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form':form})

def login_system(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # form = AuthForm(request.POST)
        print(form.is_valid())
        # print(AuthenticationForm())
        if form.is_valid():
            u = request.POST.get('username')
            p = request.POST.get('password')
            user = authenticate(request, username = u, password = p)
            print(user)
            if user is not None:
                login(request, user)
                return render(request, 'user_page.html')
            else:
                form = AuthForm()
                return render(request, 'home.html', {'form':form})
        # return render(request, 'home.html', {'form': AuthenticationForm()})
    return render(request, 'home.html', {'form':AuthenticationForm()})

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


# def signup(request):
#     # if request.user.is_authenticated:
#     #     return redirect('/books')
#
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         print(form.is_valid())
#         if form.is_valid():
#              print('post')
#              # form.save()
#              username = form.cleaned_data.get('username')#['username']
#              password = form.POST['password1']
#              user = authenticate(username=username, password=password)
#              print(username, password, user)
#              login(request, user)
#              return HttpResponse('success', request)
#
#         else:
#             return render(request, 'home.html', {'form': form})
#
#     else:
#
#         print('get')
#         form = AuthenticationForm()
#         print(form)
#         return render(request, 'home.html', {'form': form})

def users(request):
    u = User.objects.all().values_list('password')
    return render(request, 'tester.html', {'items':u})

def home(request):
    return HttpResponse('pavan', request)

class Login(LoginView):
    model = User
    fields = '__all__'
    template_name = 'home.html'
    redirect_authenticated_user = True
