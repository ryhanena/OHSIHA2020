from django.urls import path
from .views import FieldListView, FieldDetailView
from . import views

urlpatterns = [
    path('', FieldListView.as_view(), name='index'),
    path('<int:pk>/', FieldDetailView.as_view(), name='detail'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('delete/<int:pk>', views.delete, name='delete'),
]