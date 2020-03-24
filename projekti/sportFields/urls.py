from django.urls import path
from . import views



urlpatterns = [
    path('', views.api, name='api'),
    path('index/', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('delete/<int:pk>', views.delete, name='delete'),
]