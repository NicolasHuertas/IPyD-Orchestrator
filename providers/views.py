from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProviderSerializer, ArticleSerializer
from .models import Provider, Article
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

my_counter = Counter('my_counter', 'This is a counter')

class ProviderView(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

    def list(self, request, *args, **kwargs):
        my_counter.inc()  # Increment the counter
        logger.info('Listing providers')  # Log message
        return super().list(request, *args, **kwargs)

class ArticleView(viewsets.ModelViewSet):
    serializer_class=ArticleSerializer
    queryset = Article.objects.all()

    def list(self, request, *args, **kwargs):
        my_counter.inc()  # Increment the counter
        logger.info('Listing articles')  # Log message
        return super().list(request, *args, **kwargs)

def metrics(request):
    return HttpResponse(generate_latest(REGISTRY), content_type=CONTENT_TYPE_LATEST)