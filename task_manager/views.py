from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

import os

from django.conf import settings

class IndexView(TemplateView):
    template_name = 'index.html'

    def index_view(request):
        print("Текущая рабочая директория:", os.getcwd())
        print("Директории шаблонов:", settings.TEMPLATES[0]['DIRS'])
        return render(request, 'index.html')

def index_view(request):
        print("Текущая рабочая директория:", os.getcwd())
        print("Директории шаблонов:", settings.TEMPLATES[0]['DIRS'])
        return render(request, 'index.html')