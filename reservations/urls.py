from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    path('cancel/', views.cancel_reservation, name='cancel_reservation'),
]