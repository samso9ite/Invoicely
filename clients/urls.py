from django.urls import include, path
from .views import ClientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("client", ClientViewSet, basename="client")

urlpatterns =[
    path('', include(router.urls)),
]