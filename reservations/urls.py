from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    path('delete/', views.delete_reservation, name='delete_reservation'),
]