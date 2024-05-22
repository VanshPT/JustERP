from django.urls import path,include
from . import views

urlpatterns = [
  path('company-registration/', views.company, name="company registration"),
  path('root-signup/',views.root_signup, name="Root Signup"),
  path('login/', views.login, name="login"),
  path('successfull-signup/', views.successfull_signup, name='successful; signup'),
  path('successfull-login/', views.successfull_login, name="Successfull Login"),
  path('logout/', views.logout, name='logout')
]
