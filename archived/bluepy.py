from bluepy.sensortag import SensorTag
import paho.mqtt.client as mqtt
import json
import time

SENSOR_TAG_LABEL = "Living Room"
LOCATION = "Auckland"
BROKER = "localhost"
SENSOR_TAG_MAC = "54:6C:0E:52:F8:35"  # Set SensorTag's MAC address directly

# Connect to the SensorTag
tag = SensorTag(SENSOR_TAG_MAC)

# Enable the sensors you are interested in
tag.humidity.enable()
tag.barometer.enable()

# Give the sensor time to start up
time.sleep(1.0)

# Connect to the MQTT broker
client = mqtt.Client()
client.connect(BROKER)

while True:
    # Read the sensor data
    humidity = tag.humidity.read()
    barometer = tag.barometer.read()
    timestamp = time.time()

    # Format the data as JSON
    data = json.dumps({
        "timestamp": timestamp,
        "location": LOCATION,
        "device_label": SENSOR_TAG_LABEL,
        "humidity": humidity,
        "barometer": barometer
    })

    # Publish the data to the /home/sensor MQTT topic
    client.publish("/home/sensor", data)

    time.sleep(10)  # Delay before the next reading
