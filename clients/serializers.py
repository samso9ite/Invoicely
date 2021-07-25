# from django.db import models
# from django.db.models import fields
# from django.db.models.base import Model
from django.db import models
from django.db.models import fields
from .models import Client
from invoices.models import Invoice

from rest_framework import serializers

class ClientInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            'id',
            'invoice_number',
            'is_sent',
            'is_paid',
            'gross_amount',
            'vat_amount',
            'net_amount',
            'get_due_date_formatted',
            'invoice_type',
            'is_credited',
        )

class ClientSerializer(serializers.ModelSerializer):
    invoices = ClientInvoiceSerializer(many=True)
    class Meta:
        model = Client
        read_only_fields =(
            'created_by',
            'created_at'
        )
        fields = (
            "id",
            "name",
            "email",
            "address2",
            "address1",
            "zipcode",
            "place",
            "country",
            "contact_person",
            "contact_reference",
            "invoices",
        )