from django.shortcuts import render, redirect
from authapp.models import CustomUser,CompanyProfile,Permission
from django.contrib import messages
from django_countries import countries
from django_countries.fields import Country
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from home.models import CompanyModule, Module
from django.contrib.auth.decorators import login_required

# Create your views here.
def company(request):
    countries_list = list(countries)
    context = {
    'countries': countries_list
    }   
    return render(request, 'authapp/companyReg.html', context)

def root_signup(request):
    if request.method == 'POST':
        company_name=request.POST.get('company_name')
        contact_person_name=request.POST.get('contact_person_name')
        contact_email=request.POST.get('contact_email')
        contact_phone=request.POST.get('contact_phone')
        company_address=request.POST.get('company_address')
        business_description=request.POST.get('business_description')
        country=request.POST.get('country')
        registration_number=request.POST.get('registration_number')
        budget=request.POST.get('budget')
        
        country_code=country[2:4]
        country = Country(code=country_code)
       
        company=CompanyProfile(company_name=company_name, contact_person_name=contact_person_name, contact_email= contact_email,contact_phone=contact_phone, company_address=company_address, business_description=business_description,country=country,registration_number=registration_number, budget=budget)
        company.save()

        module_codes=['financial-management', 'human-resources-management-hrm', 'customer-relationship-management-crm', 'inventory-management', 'sales-and-distribution','reporting-and-analytics','customer-service', 'project-management', 'users', 'support']

        default_modules_objects=Module.objects.filter(module_code__in=module_codes)
        for module in default_modules_objects:
            CompanyModule.objects.create(company=company, module=module)
        context={
            'company_id': company.company_id,
            'company_name': company.company_name
        }
    return render(request, 'authapp/rootSignup.html' , context)

def successfull_signup(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_id = request.POST.get('company')
        password=request.POST.get('password')
        conf_password=request.POST.get('conf_password')
        type = 'root'

        existing_user= CustomUser.objects.filter(type='root', company_id=company_id).exists()
        company_obj=CompanyProfile.objects.get(company_id=company_id)
        company_name=company_obj.company_name
        if existing_user:
            messages.error(request,'Root User already exists for this account! Cannot sign in as root user!')
            return redirect('/home/error/')
        else:
            all_access_permission, created = Permission.objects.get_or_create(
                name="All Access",
                defaults={
                    'description': 'Full access to all modules'
                }
            )

            if created:
                all_modules = Module.objects.all()
                all_access_permission.modules.set(all_modules)
                all_access_permission.save()
            root_user= CustomUser(username=username, email=email, first_name=first_name, last_name=last_name, company=company_obj, type='root', is_active=True, is_staff=True)

            if password !=conf_password:
                messages.error(request,'Password and Confirm Password must be same!')
                return redirect('/home/error/')
            root_user.set_password(password) 
            root_user.save()

            root_user.permissions.add(all_access_permission)
            root_user.save()
            
        return redirect('/')

def login(request):
    return render(request, 'authapp/login.html')
@require_POST
def successfull_login(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    user=authenticate(request, email=email, password=password)
    if user is not None:
         auth_login(request, user)
         return redirect('/home/dashboard/')
    else:
        messages.error(request, "Wrong Company ID, User ID or Password!")
        return render(request, 'authapp/login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def users(request):
    user=request.user
    if user.is_authenticated:
        context={'company_id':user.company.company_id,'company_name':user.company.company_name, 'username':user.username, 'first_name':user.first_name, 'last_name': user.last_name, 'email': user.email}
    return render(request,'authapp/users.html', context)
