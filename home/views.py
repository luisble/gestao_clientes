from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView


def home(request):
    valor1 = 10
    valor2 = 20
    valor3 = valor1 * valor2
    return render(request, 'home/home.html', {'result':valor3})


def my_logout(request):
    logout(request)
    return redirect('home')

class HomePageView(TemplateView):

    template_name = "home3.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minhavariavel'] = 'Seja bem vindo a Home3'
        return context

class MinhaView(View):

    def get(self, request, *args, **kwargs):
        return render(request,'home4.html')
    
    def post(self, request, *args, **kwargs):
        return HttpResponse('Chamada pelo method=POST')
    
