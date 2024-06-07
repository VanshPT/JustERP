from django.urls import path
from . import views

urlpatterns = [
    path('', views.inquiry_form_1, name='Inquiry form 1'),
    path('f2', views.inquiry_form_2, name='Inquiry form 2'),
    path('f3', views.inquiry_form_3, name='Inquiry form 3'),
    path('uploader', views.inquiry_uploader, name="Inquiry uploader"),
    path('inquiry-table', views.inquiry_table, name="Inquiry Table"),
    path('placement-table', views.placement_table, name="Placement Table"),
    path('merge', views.merge, name="Merge View")
]
