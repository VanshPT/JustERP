from django.urls import path,include
from . import views

urlpatterns = [
  path('<int:company_id>/dashboard/', views.dashboard, name="dashboard"),
  path('<int:company_id>/company-profile/', views.company_profile, name="Company Profile"),
  path('error/', views.error, name="Error")
]
