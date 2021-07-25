from django.core.exceptions import RequestAborted
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model) :
    name= models.CharField(max_length=255)
    org_number = models.CharField(max_length=255)
    first_invoice_number = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, related_name='teams', on_delete=models.CASCADE)
    bank_account = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '%s' %self.name 