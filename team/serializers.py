from django.db.models import fields
from rest_framework.fields import ReadOnlyField
from .models import *
from rest_framework import serializers

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        read_only_field= ('created_by')

        fields = (
            "id",
            "name",
            "org_number",
            "first_invoice_number",
            "bank_account", 
            "place",
            "zipcode",
            "address",
            "email"
        )