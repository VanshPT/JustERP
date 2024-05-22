from django.urls import path,include
from . import views

urlpatterns = [
  path('dashboard/', views.dashboard, name="dashboard"),
  path('company-profile/', views.company_profile, name="Company Profile"),
  path('error/', views.error, name="Error")
]
