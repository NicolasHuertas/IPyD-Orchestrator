from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservationViewSet.as_view({'get': 'list'}), name='reservations'),
    path('<int:pk>/', views.ReservationViewSet.as_view({'get': 'retrieve'}), name='reservation'),
    path('create/', views.create_reservation, name='create_reservation'),
    path('cancel/', views.cancel_reservation, name='cancel_reservation'),
]