from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.attendance_table_view,name = 'attendance-home'),
    path('test', views.hex_test),
    path('android',views.andr_file),

    
]