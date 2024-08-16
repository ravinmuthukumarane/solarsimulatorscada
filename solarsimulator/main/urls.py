from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load_inverter/<str:inverter_id>/', views.load_inverter, name='load_inverter'),
    path('create_json/', views.create_json, name='create_json'),
    path('send_mqtt/<str:inverter_id>/', views.send_mqtt, name='send_mqtt'),
    path('robot-configurations/', views.robot_configurations, name='robot_configurations'),

]
