from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Приветствие!")

class IndexView(TemplateView):
    template_name = 'index.html'