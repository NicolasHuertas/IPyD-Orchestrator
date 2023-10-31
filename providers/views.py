from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProviderSerializer
from .models import Provider
# Create your views here.
class ProviderView(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()