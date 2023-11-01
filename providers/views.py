from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProviderSerializer, ArticleSerializer
from .models import Provider, Article
# Create your views here.
class ProviderView(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

class ArticleView(viewsets.ModelViewSet):
    serializer_class=ArticleSerializer
    queryset = Article.objects.all()