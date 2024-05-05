from django.urls import path,include
from . import views

urlpatterns = [
  path('company-registration/', views.company, name="company registration"),
  path('root-signup/',views.root_signup, name="Root Signup")
]
