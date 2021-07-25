import decimal

from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from team.models import Team
from clients.models import Client

# Create your models here.

class Invoice(models.Model):
    INVOICE = 'invoice'
    CREDIT_NOTE = 'credit_note'

    CHOICES_TYPE = (
        (INVOICE, 'Invoice'),
        (CREDIT_NOTE, 'Credit note')
    ) 
    invoice_number= models.IntegerField(default=1)
    client_name = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    client_org_number = models.CharField(max_length=255, blank=True, null=True)
    client_address_number1 = models.CharField(max_length=255, blank=True, null=True)
    client_address_number2 = models.CharField(max_length=255, blank=True, null=True)
    client_zip_code = models.CharField(max_length=255, blank=True, null=True)
    client_place = models.CharField(max_length=255, blank=True, null=True)
    client_country = models.CharField(max_length=255, blank=True, null=True)
    client_contact_person = models.CharField(max_length=255, blank=True, null=True)
    client_contact_reference = models.CharField(max_length=255, blank=True, null=True)
    sender_reference = models.CharField(max_length=255, blank=True, null=True)
    invoice_type = models.CharField(max_length=20, choices=CHOICES_TYPE, default=INVOICE)
    due_days = models.IntegerField(default=14)
    is_credit_for = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    gross_amount = models.DecimalField(max_digits=6, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=6, decimal_places=2)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invoices')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices' )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_invoices' )
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_invoices' )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    bank_account = models.CharField(max_length=255, null=True, blank=True)
    is_credited = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
    def str__(self):
        return '%s' %self.client_name

    def get_due_date(self):
        return self.created_at + timedelta(days=self.due_days)

    def get_due_date_formatted(self):
        return self.get_due_date().strftime("%d.%m.%Y")

class Item(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)
    vat_rate = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)

    def get_gross_amount(self):
        vat_rate = decimal.Decimal(self.vat_rate/100)
        return self.net_amount + (self.net_amount * vat_rate)     
