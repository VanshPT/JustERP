from django.shortcuts import render
from .models import CompanyProfile
from django_countries import countries
from django_countries.fields import Country
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
        context={
            'company_id': company.company_id,
            'company_name': company.company_name
        }
    return render(request, 'authapp/rootSignup.html' , context)
