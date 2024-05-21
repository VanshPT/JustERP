from django.shortcuts import render, redirect
from authapp.models import CustomUser,CompanyProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request, customer_id):
    user=request.user
    if user.is_authenticated:
        context={'company_id':user.company.company_id,'company_name':user.company.company_name, 'username':user.username, 'first_name':user.first_name, 'last_name': user.last_name}
        return render(request, 'home/dashboard.html', context)
    else:
        return redirect('/auth/login/')


def error(request):
   return render(request, 'home/error.html')