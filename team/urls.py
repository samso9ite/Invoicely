from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register("teams", TeamViewSet, basename='teams')

urlpatterns = [
    path('', include(router.urls))
] 