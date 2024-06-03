from django.urls import path,include
from . import views

urlpatterns = [
  path('company-registration/', views.company, name="company registration"),
  path('root-signup/',views.root_signup, name="Root Signup"),
  path('login/', views.login, name="login"),
  path('successfull-signup/', views.successfull_signup, name='successful; signup'),
  path('successfull-login/', views.successfull_login, name="Successfull Login"),
  path('logout/', views.logout, name='logout'),
  path('users', views.users, name='users'),
  path('profile' ,views.profile, name='profile view'),
  path('create-user/' ,views.create_user, name='create user'),
  path('permission/' ,views.permission, name='permission'),
  path('logs/' ,views.logs, name='logs'),
]
