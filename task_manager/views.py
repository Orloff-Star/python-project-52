from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Приветствие!")

def index(request):
       return render(request, 'index.html', {'title': 'Home Page'})