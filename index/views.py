from django.shortcuts import render
from home.models import Module

default_modules = [
    'Financial Management',
    'Human Resources Management (HRM)',
    'Customer Relationship Management (CRM)',
    'Inventory Management',
    'Sales and Distribution',
    'Reporting and Analytics',
    'Customer Service',
    'Project Management',
    'Users',
    'Support',
]

def index(request):
    existing_modules = Module.objects.values_list('module_name', flat=True)
    missing_modules = [module_name for module_name in default_modules if module_name not in existing_modules]

    if missing_modules:
        for module_name in missing_modules:
            Module.objects.create(module_name=module_name)
    
    return render(request, 'index/index.html')
