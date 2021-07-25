from django.shortcuts import render
from .serializers import ClientSerializer
from .models import Client
from rest_framework import viewsets


# Create your views here.

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all() 
    serializer_class = ClientSerializer

    def get_queryset(self):
        test =  self.queryset.filter(created_by=self.request.user)
        return test
    def perform_create(self, serializer) :
        serializer.save(created_by=self.request.user)   