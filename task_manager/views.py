from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = 'index.html'