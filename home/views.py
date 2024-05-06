from django.shortcuts import render, redirect
from authapp.models import CustomUser,CompanyProfile
from django.contrib import messages

# Create your views here.
def dashboard(request):
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
            root_user= CustomUser(username=username, email=email, first_name=first_name, last_name=last_name, company=company_obj, type='root', is_active=True, is_staff=True)

            if password !=conf_password:
                messages.error(request,'Password and Confirm Password must be same!')
                return redirect('/home/error/')
            root_user.set_password(password)
            root_user.save()
        context={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'company_name': company_name
        }
            
    return render(request, 'home/dashboard.html' , context)

def error(request):
   return render(request, 'home/error.html')