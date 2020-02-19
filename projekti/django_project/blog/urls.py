from django.urls import path
from . import views

urlpatterns = [
    #Mistä polusta 
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]