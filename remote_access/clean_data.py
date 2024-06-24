import paho.mqtt.client as mqtt
import json
import datetime
import os

LOCATION = os.getenv('LOCATION', 'Auckland')
DEVICE_TAG = os.getenv('DEVICE_TAG', 'Rex Living Room')
SUBSCRIBE_BROKER_IP = os.getenv('SUBSCRIBE_BROKER_IP', '192.168.101.97')
PUBLISH_BROKER_IP = os.getenv('PUBLISH_BROKER_IP', '192.168.101.97')
SUBSCRIBE_TOPIC = os.getenv('SUBSCRIBE_TOPIC', '/home/sensor')
PUBLISH_TOPIC = os.getenv('PUBLISH_TOPIC', '/home/sensor/processed')

# The callback for when the client receives a CONNECT response from the server.
def on_subscribe_connect(client, userdata, flags, rc):
    print(f"Subscribe Client Connected with result code {rc}")
    client.subscribe(SUBSCRIBE_TOPIC, qos=2)
    print('subscribed')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Deserializing the message payload
    payload = json.loads(msg.payload)

    # Check if the received data type is one of the types we're interested in
    if 'pressure' in payload or ('temperature' in payload and 'humidity' in payload):
        # Add the timestamp, location and device label
        payload['times'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payload['location'] = LOCATION
        payload['device'] = DEVICE_TAG
        print(payload)

        # After processing, publish it to another topic or database using publish client
        publish_client = mqtt.Client()
        publish_client.connect(PUBLISH_BROKER_IP, 1883, 60)
        publish_client.publish(PUBLISH_TOPIC, json.dumps(payload))
        publish_client.disconnect()


subscribe_client = mqtt.Client()
subscribe_client.on_connect = on_subscribe_connect
subscribe_client.on_message = on_message

subscribe_client.connect(SUBSCRIBE_BROKER_IP, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
try:
    subscribe_client.loop_forever()
except Exception as e:
    print(e)
