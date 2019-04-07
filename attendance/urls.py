from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.attendance_table_view,name = 'attendance-home'),
    path('test', views.hex_test),
    path('android',views.andr_file),
    path('att_admin_tasks/',views.att_admin_tasks, name='att_admin-tasks'),
    path('desktop/',views.upload_file, name='desktop'),
    
]