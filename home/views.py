from django.shortcuts import render, redirect, get_object_or_404
from authapp.models import CustomUser,CompanyProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CompanyModule

# Create your views here.
@login_required
def dashboard(request):
    user=request.user
    if user.is_authenticated:
        company=CompanyProfile.objects.get(pk=user.company.company_id)
        modules_installed=CompanyModule.objects.filter(company=company)
        context={'company_id':user.company.company_id,'company_name':user.company.company_name, 'username':user.username, 'first_name':user.first_name, 'last_name': user.last_name, 'email': user.email, 'modules':modules_installed}
        return render(request, 'home/dashboard.html', context)
    else:
        return redirect('/auth/login/')


def error(request):
   return render(request, 'home/error.html')

@login_required
def company_profile(request):
    user=request.user
    if user.is_authenticated:
        company=get_object_or_404(CompanyProfile,company_id=user.company.company_id)

        context={'company_id':user.company.company_id,'company_name':user.company.company_name, 'username':user.username, 'first_name':user.first_name, 'last_name': user.last_name, 'email': user.email, 'company':company}
    return render(request,'home/companyProfile.html', context)