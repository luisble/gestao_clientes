from django.urls import path
from django.views.generic.base import TemplateView
from .views import home, my_logout, HomePageView, MinhaView


urlpatterns = [
    path('', home, name="home"),
    path('logout/', my_logout, name="logout"),
    path('home2/', TemplateView.as_view(template_name='home2.html')),
    path('home3/', HomePageView.as_view(), name='home3'),
    path('home4/', MinhaView.as_view(), name='minhaview'),
]