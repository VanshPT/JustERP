from django.db import models
from django_countries.fields import CountryField

class CompanyProfile(models.Model):
    company_id=models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    company_address = models.TextField(blank=True, null=True)
    business_description = models.TextField()

    
    country = CountryField()
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
