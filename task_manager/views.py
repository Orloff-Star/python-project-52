from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Приветствие!")

def index(request):
       return render(request, 'myapp/index.html', {'title': 'Home Page'})