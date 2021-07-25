from django.conf.urls import url
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework import urlpatterns

app_name = 'invoices'
router = DefaultRouter()
router.register('invoices', InvoiceViewSet, basename='invoices')
# router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
    path('invoices/<int:invoice_id>/generate_pdf/', generate_pdf, name='generate_pdf'),
    path('invoices/<int:invoice_id>/send_reminder/', send_reminder, name= 'send_reminder'),
]
