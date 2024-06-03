from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



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
        return f"{self.company_id}: {self.company_name}"
    
class Department(models.Model):
    dept_id=models.AutoField(primary_key=True)
    dept_name=models.CharField(max_length=30)
    dept_desc=models.TextField(blank=True)

    def __str__(self):
        return self.dept_name


class Profile(models.Model):
    profile_id=models.AutoField(primary_key=True)
    dept=models.ForeignKey(Department, on_delete=models.CASCADE)
    profile_name=models.CharField(max_length=50)
    profile_desc=models.TextField()

    def __str__(self):
        return f"{self.dept.dept_name}: {self.profile_name}"
    
    
class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    modules=models.ManyToManyField('home.Module')

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, type='normal', company=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        if isinstance(company, int):
            company=CompanyProfile.objects.get(pk=company)

        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, type=type,company=company, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, company=None ,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, first_name, last_name, password,type='root', company=company, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company=models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=10, choices=[('root', 'Root'), ('normal', 'Normal')], default='normal')
    profile=models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    permissions=models.ManyToManyField(Permission)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company','username', 'first_name', 'last_name']

    def __str__(self):
        return self.username
    


