from django.shortcuts import render
from django.http import HttpResponse
from time import sleep
# Create your views here.

def home(request, start):
    # start = 0
    for i in range(10):
        start = int(start) + 1
        # sleep(1)
        return render(request, 'timer.html', {'time':start})
    return HttpResponse('success', request)