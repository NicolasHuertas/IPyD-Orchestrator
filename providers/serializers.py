from rest_framework import serializers
from .models import Provider, Article

class ProviderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Provider
        fields= '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields= '__all__'