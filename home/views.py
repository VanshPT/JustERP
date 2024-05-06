from django.shortcuts import render, redirect
from authapp.models import CustomUser,CompanyProfile
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
def dashboard(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request, email=email, password=password)
        if user is not None:
            context={'company_id':user.company.company_id, 'username':user.username, 'first_name':user.first_name, 'last_name': user.last_name}
            return render(request, 'home/dashboard.html', context)
        else:
            messages.error(request,"Wrong Company ID, User ID or Password!")
            return redirect('/auth/login/')

def error(request):
   return render(request, 'home/error.html')