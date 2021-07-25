from django.db.models import fields
from rest_framework import serializers
from .models import *
from clients.models import Client


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_field =(
            'invoice',
        )

        fields = (
            'id',
            'title',
            'quantity',
            'unit_price',
            'net_amount',
            'vat_rate',
            'discount',
        )

class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    bank_account = serializers.CharField(required=False)
    # client = serializers.HyperlinkedRelatedField(view_name='client-detail', read_only=True)
    class Meta:
        model=Invoice
        read_only_fields = (
            'created_by',
            'modified_by',
            'created_at',
            'modified_at',
            'team',
            'invoice_number'
        )
        
        fields= (
            'id',
            'client',
            'invoice_number',
            'client_name',
            'client_email',
            'client_org_number',
            'client_address_number1',
            'client_address_number2',
            'client_zip_code',
            'client_place',
            'client_country',
            'client_contact_person',
            'client_contact_reference',
            'sender_reference',
            'invoice_type',
            'due_days',
            'is_credit_for',
            'is_sent',
            'is_paid',
            'gross_amount',
            'vat_amount',
            'net_amount',
            'discount_amount',
            'items',
            'bank_account',
            'get_due_date_formatted',
            'is_credited',
            
        )
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            Item.objects.create(invoice=invoice, **item)

        return invoice
