import paho.mqtt.client as mqtt
import json
import datetime

LOCATION = 'Auckland'
DEVICE_TAG = 'Rex Living Room'
MQTT_BROKER_IP = '192.168.101.97'
MQTT_BROKER_PORT = 1883


# The callback for when the client receives a CONNECT response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/home/sensor", qos=2)  # subscribing to the topic
    print('subscribed')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Deserializing the message payload
    payload = json.loads(msg.payload)

    # Check if the received data type is one of the types we're interested in
    if 'pressure' in payload or ('temperature' in payload and 'humidity' in payload):
        # Add the timestamp, location and device label
        payload['time'] = str(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        payload['location'] = LOCATION
        payload['device'] = DEVICE_TAG
        print(payload)
        # After processing, publish it to another topic or database
        client.publish("/home/sensor/processed", json.dumps(payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_IP, MQTT_BROKER_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
try:
    client.loop_forever()
except Exception as e:
    print(f"An error occurred: {e}")

