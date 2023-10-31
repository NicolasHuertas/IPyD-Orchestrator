from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from providers import views

router = routers.DefaultRouter()
router.register(r'providers', views.ProviderView, 'providers')

urlpatterns = [
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title="Providers API"))
]