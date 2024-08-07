from django.urls import path
from . import views

urlpatterns = [
    path('', views.inverter_home, name='inverter_home'),
    path('send/<int:inverter_id>/', views.send_mqtt_message, name='send_mqtt_message'),
]
