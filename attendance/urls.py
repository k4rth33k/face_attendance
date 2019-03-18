from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload_file,name = 'attendance-home'),
    path('test', views.hex_test),
    path('android',views.andr_file),
    
]