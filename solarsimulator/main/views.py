from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import InverterForm
import threading
import time
import json
import random
from datetime import datetime
import paho.mqtt.client as mqtt
import os
from django.views.decorators.csrf import csrf_exempt

# Path to the JSON file
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'inverters.json')

# Function to save inverter data to the JSON file
def save_data(inverters):
    # Convert datetime objects to strings
    for inverter in inverters:
        for key, value in inverter.items():
            if isinstance(value, datetime):
                inverter[key] = value.strftime("%Y:%m:%d:%H:%M:%S")
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(inverters, file, indent=4)

# Function to load inverter data from the JSON file
def load_data():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    return []

# Function to generate and send MQTT messages periodically
def periodic_mqtt_task():
    while True:
        # Load inverters from the JSON file
        inverters = load_data()

        # Send MQTT messages for each inverter
        for inverter in inverters:
            message = generate_mqtt_message(inverter)
            send_mqtt_message_to_broker(message)

        # Wait for 10 seconds before sending the next batch of messages
        time.sleep(10)

# Function to generate MQTT messages
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

# Function to send MQTT message to the broker
def send_mqtt_message_to_broker(message):
    client = mqtt.Client()
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.publish("mqttsend", json.dumps(message))
    client.disconnect()

# Function to generate random values
def random_value(value, deviation):
    deviation_amount = value * (deviation / 100.0)
    return round(value + random.uniform(-deviation_amount, deviation_amount), 2)

# Function to start the periodic MQTT task in a background thread
def start_periodic_task():
    threading.Thread(target=periodic_mqtt_task, daemon=True).start()

# View to display inverters and handle adding new ones
@csrf_exempt
def index(request):
    if request.method == "POST":
        form = InverterForm(request.POST)
        if form.is_valid():
            inverters = load_data()
            updated_inverter = form.cleaned_data
            for i, inverter in enumerate(inverters):
                if inverter['name'] == updated_inverter['name']:
                    inverters[i] = updated_inverter
                    break
            save_data(inverters)
            return redirect('index')
    else:
        form = InverterForm()

    inverters = load_data()
    context = {
        'inverters': inverters,
        'form': form
    }
    return render(request, 'index.html', context)

# View to create and save the JSON file
def create_json(request):
    inverters = load_data()
    save_data(inverters)
    return HttpResponse("JSON file created successfully")


def send_mqtt(request, inverter_id=None, robot_id=None):
    if inverter_id:
        inverters = load_data()
        inverter = next((inv for inv in inverters if inv['name'] == inverter_id), None)
        if inverter:
            message = generate_mqtt_message(inverter)
            send_mqtt_message_to_broker(message)
            return JsonResponse({'status': 'success', 'message': 'MQTT message sent'})
        return JsonResponse({'status': 'error', 'message': 'Inverter not found'}, status=404)
    
    if robot_id:
        robots = load_robot_data()
        robot = next((rob for rob in robots if rob['robot'] == robot_id), None)
        if robot:
            message = generate_robot_mqtt_message(robot)
            send_mqtt_message_to_broker(message)
            return JsonResponse({'status': 'success', 'message': 'MQTT message sent'})
        return JsonResponse({'status': 'error', 'message': 'Robot not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# View to load inverter data based on selected inverter ID
def load_inverter(request, inverter_id):
    inverters = load_data()
    inverter = next((inv for inv in inverters if inv['name'] == inverter_id), None)
    if inverter:
        return JsonResponse({'status': 'success', 'inverter': inverter})
    return JsonResponse({'status': 'error', 'message': 'Inverter not found'}, status=404)

# Start the periodic task when the server starts
# start_periodic_task()
def load_robot_data():
    JSON_FILE_PATH2 = os.path.join(os.path.dirname(__file__), 'robots_config.json')
    if os.path.exists(JSON_FILE_PATH2):
        with open(JSON_FILE_PATH2, 'r') as file:
            return json.load(file)
    return []
def periodic_mqtt_task():
    while True:
        # Load inverters and robots from the JSON files
        inverters = load_data()
        robots = load_robot_data()

        # Send MQTT messages for each inverter
        for inverter in inverters:
            message = generate_mqtt_message(inverter)
            send_mqtt_message_to_broker(message)

        # Send MQTT messages for each robot
        for robot in robots:
            message = generate_robot_mqtt_message(robot)
            send_mqtt_message_to_broker(message)

        # Wait for 10 seconds before sending the next batch of messages
        time.sleep(10)
# Function to generate MQTT messages for robots
def generate_robot_mqtt_message(robot):
    message = {
        'Timestamp': datetime.now().strftime("%Y:%m:%d:%H:%M:%S"),
        'robot': robot['robot'],
        'connection': robot['connection'],
        'status': robot['status'],
        'cleaning_status': robot['cleaning_status'],
        'category': "2"
    }
    return message
def robot_configurations(request):
    if request.method == 'POST':
        # Retrieve data from the form
        robots_data = [
            {'robot': 'Robot 1', 'connection': request.POST.get('connection_1'), 'status': request.POST.get('status_1'), 'cleaning_status': request.POST.get('cleaning_status_1')},
            {'robot': 'Robot 2', 'connection': request.POST.get('connection_2'), 'status': request.POST.get('status_2'), 'cleaning_status': request.POST.get('cleaning_status_2')},
            {'robot': 'Robot 3', 'connection': request.POST.get('connection_3'), 'status': request.POST.get('status_3'), 'cleaning_status': request.POST.get('cleaning_status_3')},
            {'robot': 'Robot 4', 'connection': request.POST.get('connection_4'), 'status': request.POST.get('status_4'), 'cleaning_status': request.POST.get('cleaning_status_4')},
            {'robot': 'Robot 5', 'connection': request.POST.get('connection_5'), 'status': request.POST.get('status_5'), 'cleaning_status': request.POST.get('cleaning_status_5')},
            {'robot': 'Robot 6', 'connection': request.POST.get('connection_6'), 'status': request.POST.get('status_6'), 'cleaning_status': request.POST.get('cleaning_status_6')},
            {'robot': 'Robot 7', 'connection': request.POST.get('connection_7'), 'status': request.POST.get('status_7'), 'cleaning_status': request.POST.get('cleaning_status_7')},
            {'robot': 'Robot 8', 'connection': request.POST.get('connection_8'), 'status': request.POST.get('status_8'), 'cleaning_status': request.POST.get('cleaning_status_8')},
            {'robot': 'Robot 9', 'connection': request.POST.get('connection_9'), 'status': request.POST.get('status_9'), 'cleaning_status': request.POST.get('cleaning_status_9')},
            {'robot': 'Robot 10', 'connection': request.POST.get('connection_10'), 'status': request.POST.get('status_10'), 'cleaning_status': request.POST.get('cleaning_status_10')},
        ]
        
        JSON_FILE_PATH2 = os.path.join(os.path.dirname(__file__), 'robots_config.json')
        
        # Save data to a JSON file
        with open(JSON_FILE_PATH2, 'w') as json_file:
            json.dump(robots_data, json_file, indent=4)
        
        # Return a success response
        return JsonResponse({'message': 'Configurations saved successfully'})

    # Render the form
    return render(request, 'robot.html')
