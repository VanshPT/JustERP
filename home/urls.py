from django.urls import path,include
from . import views

urlpatterns = [
  path('<int:customer_id>/dashboard/', views.dashboard, name="dashboard"),
  path('error/', views.error, name="Error")
]
