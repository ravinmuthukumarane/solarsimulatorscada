# # views.py

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse
# from .models import Inverter
# from .forms import InverterForm
# import threading
# import time
# import json
# import random
# from datetime import datetime
# import paho.mqtt.client as mqtt
# from django.apps import apps

# # Function to generate and send MQTT messages periodically
# def periodic_mqtt_task():
#     while True:
#         # Load inverters from the database
#         inverters = load_data()

#         # Send MQTT messages for each inverter
#         for inverter in inverters:
#             message = generate_mqtt_message(inverter)
#             send_mqtt_message_to_broker(message)

#         # Wait for 10 seconds before sending the next batch of messages
#         time.sleep(10)

# # Function to generate MQTT messages
# def generate_mqtt_message(inverter):
#     message = {
#         'Timestamp': datetime.now().strftime("%Y:%m:%d:%H:%M:%S"),
#         'inverterID': inverter['name'],
#         'category': 1,
#         'Voltage_L1-L2': random_value(inverter['voltage_l1_l2'], inverter['voltage_l1_l2_dev']),
#         'Voltage L3-L1': random_value(inverter['voltage_l3_l1'], inverter['voltage_l3_l1_dev']),
#         'Voltage L2-L3': random_value(inverter['voltage_l2_l3'], inverter['voltage_l2_l3_dev']),
#         'Voltage L1': random_value(inverter['voltage_l1'], inverter['voltage_l1_dev']),
#         'Voltage L2': random_value(inverter['voltage_l2'], inverter['voltage_l2_dev']),
#         'Voltage L3': random_value(inverter['voltage_l3'], inverter['voltage_l3_dev']),
#         'Current L1': random_value(inverter['current_l1'], inverter['current_l1_dev']),
#         'Current L2': random_value(inverter['current_l2'], inverter['current_l2_dev']),
#         'Current L3': random_value(inverter['current_l3'], inverter['current_l3_dev']),
#         'Power Factor (PF)': random_value(inverter['power_factor'], inverter['power_factor_dev']),
#         'Frequency 1 (Hz)': random_value(inverter['frequency_1'], inverter['frequency_1_dev']),
#         'Frequency 2 (Hz)': random_value(inverter['frequency_2'], inverter['frequency_2_dev']),
#         'Frequency 3 (Hz)': random_value(inverter['frequency_3'], inverter['frequency_3_dev']),
#         'DC Input Voltage (V)': random_value(inverter['dc_input_voltage'], inverter['dc_input_voltage_dev']),
#         'DC Input Current (A)': random_value(inverter['dc_input_current'], inverter['dc_input_current_dev']),
#         'DC Input Power (kW)': random_value(inverter['dc_input_power'], inverter['dc_input_power_dev']),
#         'Temperature': random_value(inverter['temperature'], inverter['temperature_dev']),
#         'Solar irradiance 1': random_value(inverter['solar_irradiance_1'], inverter['solar_irradiance_1_dev']),
#         'Solar irradiance 2': random_value(inverter['solar_irradiance_2'], inverter['solar_irradiance_2_dev']),
#         'Solar irradiance 3': random_value(inverter['solar_irradiance_3'], inverter['solar_irradiance_3_dev']),
#         'active 01 Power': random_value(inverter['active_power_01'], inverter['active_power_01_dev']),
#         'active 02 Power': random_value(inverter['active_power_02'], inverter['active_power_02_dev']),
#         'active 03 Power': random_value(inverter['active_power_03'], inverter['active_power_03_dev']),
#         'Reference Power 01': random_value(inverter['reference_power_01'], inverter['reference_power_01_dev']),
#         'Reference Power 02': random_value(inverter['reference_power_02'], inverter['reference_power_02_dev']),
#         'Reference Power 03': random_value(inverter['reference_power_03'], inverter['reference_power_03_dev']),
#     }
#     return message

# # Function to send MQTT message to the broker
# def send_mqtt_message_to_broker(message):
#     client = mqtt.Client()
#     client.connect("mqtt.eclipseprojects.io", 1883, 60)
#     client.publish("mqttsend", json.dumps(message))
#     client.disconnect()

# # Function to generate random values
# def random_value(value, deviation):
#     deviation_amount = value * (deviation / 100.0)
#     return round(value + random.uniform(-deviation_amount, deviation_amount), 2)

# # Function to load inverter data from the database
# def load_data():
#     Inverter = apps.get_model('main', 'Inverter')  # Lazily load the Inverter model
#     return list(Inverter.objects.all().values())

# # Function to start the periodic MQTT task in a background thread
# def start_periodic_task():
#     threading.Thread(target=periodic_mqtt_task, daemon=True).start()

# # View to display inverters and handle adding new ones
# def index(request):
#     if request.method == "POST":
#         form = InverterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = InverterForm()

#     inverters = Inverter.objects.all()
#     context = {
#         'inverters': inverters,
#         'form': form
#     }
#     return render(request, 'index.html', context)

# # View to send MQTT message for a specific inverter
# def send_mqtt(request, inverter_id):
#     inverter = get_object_or_404(Inverter, id=inverter_id)
#     message = generate_mqtt_message(inverter.__dict__)
#     send_mqtt_message_to_broker(message)
#     return JsonResponse({'status': 'success', 'message': 'MQTT message sent'})

# # Start the periodic task when the server starts
# start_periodic_task()

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse, HttpResponse
# from .models import Inverter
# from .forms import InverterForm
# import threading
# import time
# import json
# import random
# from datetime import datetime
# import paho.mqtt.client as mqtt
# from django.apps import apps
# import os

# # Path to the JSON file
# JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'inverters.json')

# # Function to generate and send MQTT messages periodically
# def periodic_mqtt_task():
#     while True:
#         # Load inverters from the JSON file
#         inverters = load_data()

#         # Send MQTT messages for each inverter
#         for inverter in inverters:
#             message = generate_mqtt_message(inverter)
#             send_mqtt_message_to_broker(message)

#         # Wait for 10 seconds before sending the next batch of messages
#         time.sleep(10)

# # Function to generate MQTT messages
# def generate_mqtt_message(inverter):
#     message = {
#         'Timestamp': datetime.now().strftime("%Y:%m:%d:%H:%M:%S"),
#         'inverterID': inverter['name'],
#         'category': 1,
#         'Voltage_L1-L2': random_value(inverter['voltage_l1_l2'], inverter['voltage_l1_l2_dev']),
#         'Voltage L3-L1': random_value(inverter['voltage_l3_l1'], inverter['voltage_l3_l1_dev']),
#         'Voltage L2-L3': random_value(inverter['voltage_l2_l3'], inverter['voltage_l2_l3_dev']),
#         'Voltage L1': random_value(inverter['voltage_l1'], inverter['voltage_l1_dev']),
#         'Voltage L2': random_value(inverter['voltage_l2'], inverter['voltage_l2_dev']),
#         'Voltage L3': random_value(inverter['voltage_l3'], inverter['voltage_l3_dev']),
#         'Current L1': random_value(inverter['current_l1'], inverter['current_l1_dev']),
#         'Current L2': random_value(inverter['current_l2'], inverter['current_l2_dev']),
#         'Current L3': random_value(inverter['current_l3'], inverter['current_l3_dev']),
#         'Power Factor (PF)': random_value(inverter['power_factor'], inverter['power_factor_dev']),
#         'Frequency 1 (Hz)': random_value(inverter['frequency_1'], inverter['frequency_1_dev']),
#         'Frequency 2 (Hz)': random_value(inverter['frequency_2'], inverter['frequency_2_dev']),
#         'Frequency 3 (Hz)': random_value(inverter['frequency_3'], inverter['frequency_3_dev']),
#         'DC Input Voltage (V)': random_value(inverter['dc_input_voltage'], inverter['dc_input_voltage_dev']),
#         'DC Input Current (A)': random_value(inverter['dc_input_current'], inverter['dc_input_current_dev']),
#         'DC Input Power (kW)': random_value(inverter['dc_input_power'], inverter['dc_input_power_dev']),
#         'Temperature': random_value(inverter['temperature'], inverter['temperature_dev']),
#         'Solar irradiance 1': random_value(inverter['solar_irradiance_1'], inverter['solar_irradiance_1_dev']),
#         'Solar irradiance 2': random_value(inverter['solar_irradiance_2'], inverter['solar_irradiance_2_dev']),
#         'Solar irradiance 3': random_value(inverter['solar_irradiance_3'], inverter['solar_irradiance_3_dev']),
#         'active 01 Power': random_value(inverter['active_power_01'], inverter['active_power_01_dev']),
#         'active 02 Power': random_value(inverter['active_power_02'], inverter['active_power_02_dev']),
#         'active 03 Power': random_value(inverter['active_power_03'], inverter['active_power_03_dev']),
#         'Reference Power 01': random_value(inverter['reference_power_01'], inverter['reference_power_01_dev']),
#         'Reference Power 02': random_value(inverter['reference_power_02'], inverter['reference_power_02_dev']),
#         'Reference Power 03': random_value(inverter['reference_power_03'], inverter['reference_power_03_dev']),
#     }
#     return message

# # Function to send MQTT message to the broker
# def send_mqtt_message_to_broker(message):
#     client = mqtt.Client()
#     client.connect("mqtt.eclipseprojects.io", 1883, 60)
#     client.publish("mqttsend", json.dumps(message))
#     client.disconnect()

# # Function to generate random values
# def random_value(value, deviation):
#     deviation_amount = value * (deviation / 100.0)
#     return round(value + random.uniform(-deviation_amount, deviation_amount), 2)

# # Function to load inverter data from the JSON file
# def load_data():
#     if os.path.exists(JSON_FILE_PATH):
#         with open(JSON_FILE_PATH, 'r') as file:
#             return json.load(file)
#     return []

# # Function to save inverter data to the JSON file
# def save_data(inverters):
#     with open(JSON_FILE_PATH, 'w') as file:
#         json.dump(inverters, file, indent=4)

# # Function to start the periodic MQTT task in a background thread
# def start_periodic_task():
#     threading.Thread(target=periodic_mqtt_task, daemon=True).start()

# # View to display inverters and handle adding new ones
# def index(request):
#     if request.method == "POST":
#         form = InverterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             update_json_file()
#             return redirect('index')
#     else:
#         form = InverterForm()

#     inverters = Inverter.objects.all()
#     context = {
#         'inverters': inverters,
#         'form': form
#     }
#     return render(request, 'index.html', context)

# # View to create and save the JSON file
# def create_json(request):
#     inverters = list(Inverter.objects.all().values())
#     save_data(inverters)
#     return HttpResponse("JSON file created successfully")

# # View to send MQTT message for a specific inverter
# def send_mqtt(request, inverter_id):
#     inverter = get_object_or_404(Inverter, id=inverter_id)
#     message = generate_mqtt_message(inverter.__dict__)
#     send_mqtt_message_to_broker(message)
#     return JsonResponse({'status': 'success', 'message': 'MQTT message sent'})

# # Ensure the JSON file is updated when new inverters are added
# def update_json_file():
#     inverters = list(Inverter.objects.all().values())
#     save_data(inverters)

# # Start the periodic task when the server starts
# start_periodic_task()

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse, HttpResponse
# from .models import Inverter
# from .forms import InverterForm
# import threading
# import time
# import json
# import random
# from datetime import datetime
# import paho.mqtt.client as mqtt
# from django.apps import apps
# import os

# # Path to the JSON file
# JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'inverters.json')
# # Function to save inverter data to the JSON file
# def save_data(inverters):
#     # Convert datetime objects to strings
#     for inverter in inverters:
#         for key, value in inverter.items():
#             if isinstance(value, datetime):
#                 inverter[key] = value.strftime("%Y:%m:%d:%H:%M:%S")
#     with open(JSON_FILE_PATH, 'w') as file:
#         json.dump(inverters, file, indent=4)

# # Function to generate and send MQTT messages periodically
# def periodic_mqtt_task():
#     while True:
#         # Load inverters from the JSON file
#         inverters = load_data()

#         # Send MQTT messages for each inverter
#         for inverter in inverters:
#             message = generate_mqtt_message(inverter)
#             send_mqtt_message_to_broker(message)

#         # Wait for 10 seconds before sending the next batch of messages
#         time.sleep(10)

# # Function to generate MQTT messages
# def generate_mqtt_message(inverter):
#     message = {
#         'Timestamp': datetime.now().strftime("%Y:%m:%d:%H:%M:%S"),
#         'inverterID': inverter['name'],
#         'category': 1,
#         'Voltage_L1-L2': random_value(inverter['voltage_l1_l2'], inverter['voltage_l1_l2_dev']),
#         'Voltage L3-L1': random_value(inverter['voltage_l3_l1'], inverter['voltage_l3_l1_dev']),
#         'Voltage L2-L3': random_value(inverter['voltage_l2_l3'], inverter['voltage_l2_l3_dev']),
#         'Voltage L1': random_value(inverter['voltage_l1'], inverter['voltage_l1_dev']),
#         'Voltage L2': random_value(inverter['voltage_l2'], inverter['voltage_l2_dev']),
#         'Voltage L3': random_value(inverter['voltage_l3'], inverter['voltage_l3_dev']),
#         'Current L1': random_value(inverter['current_l1'], inverter['current_l1_dev']),
#         'Current L2': random_value(inverter['current_l2'], inverter['current_l2_dev']),
#         'Current L3': random_value(inverter['current_l3'], inverter['current_l3_dev']),
#         'Power Factor (PF)': random_value(inverter['power_factor'], inverter['power_factor_dev']),
#         'Frequency 1 (Hz)': random_value(inverter['frequency_1'], inverter['frequency_1_dev']),
#         'Frequency 2 (Hz)': random_value(inverter['frequency_2'], inverter['frequency_2_dev']),
#         'Frequency 3 (Hz)': random_value(inverter['frequency_3'], inverter['frequency_3_dev']),
#         'DC Input Voltage (V)': random_value(inverter['dc_input_voltage'], inverter['dc_input_voltage_dev']),
#         'DC Input Current (A)': random_value(inverter['dc_input_current'], inverter['dc_input_current_dev']),
#         'DC Input Power (kW)': random_value(inverter['dc_input_power'], inverter['dc_input_power_dev']),
#         'Temperature': random_value(inverter['temperature'], inverter['temperature_dev']),
#         'Solar irradiance 1': random_value(inverter['solar_irradiance_1'], inverter['solar_irradiance_1_dev']),
#         'Solar irradiance 2': random_value(inverter['solar_irradiance_2'], inverter['solar_irradiance_2_dev']),
#         'Solar irradiance 3': random_value(inverter['solar_irradiance_3'], inverter['solar_irradiance_3_dev']),
#         'active 01 Power': random_value(inverter['active_power_01'], inverter['active_power_01_dev']),
#         'active 02 Power': random_value(inverter['active_power_02'], inverter['active_power_02_dev']),
#         'active 03 Power': random_value(inverter['active_power_03'], inverter['active_power_03_dev']),
#         'Reference Power 01': random_value(inverter['reference_power_01'], inverter['reference_power_01_dev']),
#         'Reference Power 02': random_value(inverter['reference_power_02'], inverter['reference_power_02_dev']),
#         'Reference Power 03': random_value(inverter['reference_power_03'], inverter['reference_power_03_dev']),
#     }
#     return message

# # Function to send MQTT message to the broker
# def send_mqtt_message_to_broker(message):
#     client = mqtt.Client()
#     client.connect("mqtt.eclipseprojects.io", 1883, 60)
#     client.publish("mqttsend", json.dumps(message))
#     client.disconnect()

# # Function to generate random values
# def random_value(value, deviation):
#     deviation_amount = value * (deviation / 100.0)
#     return round(value + random.uniform(-deviation_amount, deviation_amount), 2)

# # Function to load inverter data from the JSON file
# def load_data():
#     if os.path.exists(JSON_FILE_PATH):
#         with open(JSON_FILE_PATH, 'r') as file:
#             return json.load(file)
#     return []

# # Function to start the periodic MQTT task in a background thread
# def start_periodic_task():
#     threading.Thread(target=periodic_mqtt_task, daemon=True).start()

# # View to display inverters and handle adding new ones
# def index(request):
#     if request.method == "POST":
#         form = InverterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             update_json_file()
#             return redirect('index')
#     else:
#         form = InverterForm()

#     inverters = Inverter.objects.all()
#     context = {
#         'inverters': inverters,
#         'form': form
#     }
#     return render(request, 'index.html', context)

# # View to create and save the JSON file
# def create_json(request):
#     inverters = list(Inverter.objects.all().values())
#     save_data(inverters)
#     return HttpResponse("JSON file created successfully")

# # View to send MQTT message for a specific inverter
# def send_mqtt(request, inverter_id):
#     inverter = get_object_or_404(Inverter, id=inverter_id)
#     message = generate_mqtt_message(inverter.__dict__)
#     send_mqtt_message_to_broker(message)
#     return JsonResponse({'status': 'success', 'message': 'MQTT message sent'})

# # Ensure the JSON file is updated when new inverters are added
# def update_json_file():
#     inverters = list(Inverter.objects.all().values())
#     save_data(inverters)

# # Start the periodic task when the server starts
# start_periodic_task()

# views.py

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse, HttpResponse
# from .forms import InverterForm
# import threading
# import time
# import json
# import random
# from datetime import datetime
# import paho.mqtt.client as mqtt
# import os

# # Path to the JSON file
# JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'inverters.json')

# # Function to save inverter data to the JSON file
# def save_data(inverters):
#     # Convert datetime objects to strings
#     for inverter in inverters:
#         for key, value in inverter.items():
#             if isinstance(value, datetime):
#                 inverter[key] = value.strftime("%Y:%m:%d:%H:%M:%S")
#     with open(JSON_FILE_PATH, 'w') as file:
#         json.dump(inverters, file, indent=4)

# # Function to load inverter data from the JSON file
# def load_data():
#     if os.path.exists(JSON_FILE_PATH):
#         with open(JSON_FILE_PATH, 'r') as file:
#             return json.load(file)
#     return []

# # Function to generate and send MQTT messages periodically
# def periodic_mqtt_task():
#     while True:
#         # Load inverters from the JSON file
#         inverters = load_data()

#         # Send MQTT messages for each inverter
#         for inverter in inverters:
#             message = generate_mqtt_message(inverter)
#             send_mqtt_message_to_broker(message)

#         # Wait for 10 seconds before sending the next batch of messages
#         time.sleep(10)

# # Function to generate MQTT messages
# def generate_mqtt_message(inverter):
#     message = {
#         'Timestamp': datetime.now().strftime("%Y:%m:%d:%H:%M:%S"),
#         'inverterID': inverter['name'],
#         'category': 1,
#         'Voltage_L1-L2': random_value(inverter['voltage_l1_l2'], inverter['voltage_l1_l2_dev']),
#         'Voltage L3-L1': random_value(inverter['voltage_l3_l1'], inverter['voltage_l3_l1_dev']),
#         'Voltage L2-L3': random_value(inverter['voltage_l2_l3'], inverter['voltage_l2_l3_dev']),
#         'Voltage L1': random_value(inverter['voltage_l1'], inverter['voltage_l1_dev']),
#         'Voltage L2': random_value(inverter['voltage_l2'], inverter['voltage_l2_dev']),
#         'Voltage L3': random_value(inverter['voltage_l3'], inverter['voltage_l3_dev']),
#         'Current L1': random_value(inverter['current_l1'], inverter['current_l1_dev']),
#         'Current L2': random_value(inverter['current_l2'], inverter['current_l2_dev']),
#         'Current L3': random_value(inverter['current_l3'], inverter['current_l3_dev']),
#         'Power Factor (PF)': random_value(inverter['power_factor'], inverter['power_factor_dev']),
#         'Frequency 1 (Hz)': random_value(inverter['frequency_1'], inverter['frequency_1_dev']),
#         'Frequency 2 (Hz)': random_value(inverter['frequency_2'], inverter['frequency_2_dev']),
#         'Frequency 3 (Hz)': random_value(inverter['frequency_3'], inverter['frequency_3_dev']),
#         'DC Input Voltage (V)': random_value(inverter['dc_input_voltage'], inverter['dc_input_voltage_dev']),
#         'DC Input Current (A)': random_value(inverter['dc_input_current'], inverter['dc_input_current_dev']),
#         'DC Input Power (kW)': random_value(inverter['dc_input_power'], inverter['dc_input_power_dev']),
#         'Temperature': random_value(inverter['temperature'], inverter['temperature_dev']),
#         'Solar irradiance 1': random_value(inverter['solar_irradiance_1'], inverter['solar_irradiance_1_dev']),
#         'Solar irradiance 2': random_value(inverter['solar_irradiance_2'], inverter['solar_irradiance_2_dev']),
#         'Solar irradiance 3': random_value(inverter['solar_irradiance_3'], inverter['solar_irradiance_3_dev']),
#         'active 01 Power': random_value(inverter['active_power_01'], inverter['active_power_01_dev']),
#         'active 02 Power': random_value(inverter['active_power_02'], inverter['active_power_02_dev']),
#         'active 03 Power': random_value(inverter['active_power_03'], inverter['active_power_03_dev']),
#         'Reference Power 01': random_value(inverter['reference_power_01'], inverter['reference_power_01_dev']),
#         'Reference Power 02': random_value(inverter['reference_power_02'], inverter['reference_power_02_dev']),
#         'Reference Power 03': random_value(inverter['reference_power_03'], inverter['reference_power_03_dev']),
#     }
#     return message

# # Function to send MQTT message to the broker
# def send_mqtt_message_to_broker(message):
#     client = mqtt.Client()
#     client.connect("mqtt.eclipseprojects.io", 1883, 60)
#     client.publish("mqttsend", json.dumps(message))
#     client.disconnect()

# # Function to generate random values
# def random_value(value, deviation):
#     deviation_amount = value * (deviation / 100.0)
#     return round(value + random.uniform(-deviation_amount, deviation_amount), 2)

# # Function to start the periodic MQTT task in a background thread
# def start_periodic_task():
#     threading.Thread(target=periodic_mqtt_task, daemon=True).start()

# # View to display inverters and handle adding new ones
# def index(request):
#     if request.method == "POST":
#         form = InverterForm(request.POST)
#         if form.is_valid():
#             # Save data to JSON file
#             inverters = load_data()
#             inverters.append(form.cleaned_data)
#             save_data(inverters)
#             return redirect('index')
#     else:
#         form = InverterForm()

#     inverters = load_data()
#     context = {
#         'inverters': inverters,
#         'form': form
#     }
#     return render(request, 'index.html', context)

# # View to create and save the JSON file
# def create_json(request):
#     inverters = load_data()
#     save_data(inverters)
#     return HttpResponse("JSON file created successfully")

# # View to send MQTT message for a specific inverter
# def send_mqtt(request, inverter_id):
#     inverters = load_data()
#     inverter = next((inv for inv in inverters if inv['id'] == inverter_id), None)
#     if inverter:
#         message = generate_mqtt_message(inverter)
#         send_mqtt_message_to_broker(message)
#         return JsonResponse({'status': 'success', 'message': 'MQTT message sent'})
#     return JsonResponse({'status': 'error', 'message': 'Inverter not found'}, status=404)

# # # Start the periodic task when the server starts
# # start_periodic_task()


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

# View to send MQTT message for a specific inverter
def send_mqtt(request, inverter_id):
    inverters = load_data()
    inverter = next((inv for inv in inverters if inv['name'] == inverter_id), None)
    if inverter:
        message = generate_mqtt_message(inverter)
        send_mqtt_message_to_broker(message)
        return JsonResponse({'status': 'success', 'message': 'MQTT message sent'})
    return JsonResponse({'status': 'error', 'message': 'Inverter not found'}, status=404)

# View to load inverter data based on selected inverter ID
def load_inverter(request, inverter_id):
    inverters = load_data()
    inverter = next((inv for inv in inverters if inv['name'] == inverter_id), None)
    if inverter:
        return JsonResponse({'status': 'success', 'inverter': inverter})
    return JsonResponse({'status': 'error', 'message': 'Inverter not found'}, status=404)

# Start the periodic task when the server starts
start_periodic_task()
