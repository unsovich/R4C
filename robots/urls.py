from django.urls import path
from . import views

app_name = 'robots'

urlpatterns = [
    path('', views.robot_list, name='robot_list'),
    path('api/create_robot/', views.create_robot, name='create_robot'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('download-report/', views.download_report, name='download_report'),
    path('robot_detail/<int:robot_id>/<str:model>/<str:version>/', views.robot_detail, name='robot_detail'),
]