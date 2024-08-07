from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os
import random
from datetime import datetime
import paho.mqtt.client as mqtt
from django import forms
from .models import Inverter

class InverterForm(forms.ModelForm):
    class Meta:
        model = Inverter
        fields = '__all__'

DATA_FILE = 'inverter_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def inverter_home(request):
    if request.method == 'POST':
        form = InverterForm(request.POST)
        if form.is_valid():
            inverter_data = form.cleaned_data
            inverter_data['id'] = len(load_data()) + 1  # Assign a unique ID
            data = load_data()
            data.append(inverter_data)
            save_data(data)
            return redirect('inverter_home')
    else:
        form = InverterForm()
    
    inverters = load_data()
    return render(request, 'index.html', {'form': form, 'inverters': inverters})

def send_mqtt_message(request, inverter_id):
    inverters = load_data()
    inverter = next((inv for inv in inverters if inv['id'] == inverter_id), None)
    if not inverter:
        return JsonResponse({'error': 'Inverter not found'}, status=404)
    
    message = generate_mqtt_message(inverter)
    client = mqtt.Client()
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.publish("mqttsend", json.dumps(message))
    client.disconnect()
    return JsonResponse(message)
def generate_mqtt_message(inverter):
    message = {
        'Timestamp': datetime.now().strftime("%Y:%m:%d:%H:%M:%S"),
        'inverterID': inverter['name'],
        'category': 1,
        'Voltage_L1-L2': random_value(inverter['voltage_l1_l2'], inverter['voltage_l1_l2_dev']),
        'Voltage L3-L1': random_value(inverter['voltage_l3_l1'], inverter['voltage_l3_l1_dev']),
        'Voltage L2-L3': random_value(inverter['voltage_l2_l3'], inverter['voltage_l2_l3_dev']),
        'Voltage L1': random_value(inverter['voltage_l1'], inverter['voltage_l1_dev']),
        'Voltage L2': random_value(inverter['voltage_l2'], inverter['voltage_l2_dev']),
        'Voltage L3': random_value(inverter['voltage_l3'], inverter['voltage_l3_dev']),
        'Current L1': random_value(inverter['current_l1'], inverter['current_l1_dev']),
        'Current L2': random_value(inverter['current_l2'], inverter['current_l2_dev']),
        'Current L3': random_value(inverter['current_l3'], inverter['current_l3_dev']),
        'Power Factor (PF)': random_value(inverter['power_factor'], inverter['power_factor_dev']),
        'Frequency 1 (Hz)': random_value(inverter['frequency_1'], inverter['frequency_1_dev']),
        'Frequency 2 (Hz)': random_value(inverter['frequency_2'], inverter['frequency_2_dev']),
        'Frequency 3 (Hz)': random_value(inverter['frequency_3'], inverter['frequency_3_dev']),
        'DC Input Voltage (V)': random_value(inverter['dc_input_voltage'], inverter['dc_input_voltage_dev']),
        'DC Input Current (A)': random_value(inverter['dc_input_current'], inverter['dc_input_current_dev']),
        'DC Input Power (kW)': random_value(inverter['dc_input_power'], inverter['dc_input_power_dev']),
        'Temperature': random_value(inverter['temperature'], inverter['temperature_dev']),
        'Solar irradiance 1': random_value(inverter['solar_irradiance_1'], inverter['solar_irradiance_1_dev']),
        'Solar irradiance 2': random_value(inverter['solar_irradiance_2'], inverter['solar_irradiance_2_dev']),
        'Solar irradiance 3': random_value(inverter['solar_irradiance_3'], inverter['solar_irradiance_3_dev']),
        'active 01 Power': random_value(inverter['active_power_01'], inverter['active_power_01_dev']),
        'active 02 Power': random_value(inverter['active_power_02'], inverter['active_power_02_dev']),
        'active 03 Power': random_value(inverter['active_power_03'], inverter['active_power_03_dev']),
        'Reference Power 01': random_value(inverter['reference_power_01'], inverter['reference_power_01_dev']),
        'Reference Power 02': random_value(inverter['reference_power_02'], inverter['reference_power_02_dev']),
        'Reference Power 03': random_value(inverter['reference_power_03'], inverter['reference_power_03_dev']),
    }
    return message

def random_value(value, deviation):
    deviation_amount = value * (deviation / 100.0)
    return round(value + random.uniform(-deviation_amount, deviation_amount), 2)
