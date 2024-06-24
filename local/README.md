... set up raspberry pi 4 with ssh and [Raspberry PI imager](https://www.raspberrypi.com/software/)

```bash
sudo apt-get update
```

```bash
sudo apt-get install docker-compose
```

check docker status
```bash
systemctl status docker
```

docker without sudo check this [link](https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md)


- `node-red` and `grafana` will take data, so it is better to sort out file permissions before activate them, otherwise the container is not able to write the mounted volumes. 
- using `chown` to change the owner of the mounted volumes to the user id of the container.
```bash
sudo chown -R 472:472 ./grafana
```

```bash
sudo chown -R 1000:1000 ./node-red
```


create a docker-compose.yml file
```bash
nano docker-compose.yml
```

```yml
version: '3'
services:
  mosquitto:
    image: eclipse-mosquitto:latest
    volumes:
      - ./mosquitto/config/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    ports:
      - 1883:1883
      - 9001:9001
  node-red:
    image: nodered/node-red:latest
    volumes:
      - ./node-red/data:/data
    ports:
      - 1880:1880
    
  influxdb:
    image: influxdb:18
    volumes:
      - ./influxdb:/var/lib/influxdb
    ports:
      - 8086:8086
  grafana:
    image: grafana/grafana:latest
    volumes:
      - ./grafana:/var/lib/grafana
    ports:
      - 3000:3000
```

stop all containers at once
```bash
docker-compose stop
```

start all containers at once
```bash
docker-compose start
```





----


![](../pictures/Pasted%20image%2020230622211246.png)

![](../pictures/Pasted%20image%2020230622211321.png)


![](../pictures/Pasted%20image%2020230623090952.png)
![](../pictures/Pasted%20image%2020230623091105.png)

![](../pictures/Pasted%20image%2020230623093533.png)
![](../pictures/Pasted%20image%2020230623093601.png)


---
python script to read from TI SensorTag
1. install dependencies
```bash
pip install bluepy paho-mqtt
```
2. export path to bluepy-helper
```bash
echo 'export PATH=$PATH:/home/rex/.local/bin' >> ~/.bashrc
```

```bash
source ~/.bashrc
```

![](../pictures/Pasted%20image%2020230622144918.png)

3. use Python script to read data from the SensorTag and then publish the data to an MQTT topic.

devince Mac address: 54:6C:0E:52:F8:35
```bash
sudo hcitool lescan
```
![](../pictures/Pasted%20image%2020230622151722.png)

![](../pictures/Pasted%20image%2020230622183712.png)
- `object`: This could be the temperature of an object that an infrared sensor is pointing at.
- `ambient`: This could be the ambient temperature, measured by a temperature sensor.
- `pressure`: This is likely a pressure reading from a pressure sensor, possibly atmospheric pressure.
- `x`, `y`, `z`: These are typically accelerometer readings representing movement or orientation on three axes. In your log, these sets of `x`, `y`, `z` readings appear three times, so they might be coming from three different sensors, for example, an accelerometer, a gyroscope, and a magnetometer.
- `lux`: This is a light level reading from a light sensor.
- `temperature` and `humidity`: These are readings from a temperature sensor and a humidity sensor.

If you're only interested in monitoring certain types of data, you would need to configure the sensor tag node in Node-RED to only publish those data types. The specific steps to do this would depend on how your sensor tag node is set up, but generally you would go into the configuration for that node and deselect the sensors you're not interested in.

In the Python script, you could also modify the `on_message` function to only process the data types you're interested in. Just include those data types in the condition check inside the `if` statement. For example, if you're only interested in `object`, `ambient`, and `pressure`, the `if` statement would look like this:
```python
# If the data has all required fields
if {'object', 'ambient', 'pressure'}.issubset(data):
```

also, could turn them off thru sensor tag
![](../pictures/Pasted%20image%2020230622183952.png)
- IR Temperature: This is typically used to measure the temperature of an object that the sensor is pointed at, using infrared technology. As it's not explicitly the `temperature` reading you're interested in, you can disable it.
    
- Magnetometer: This sensor measures magnetic fields. As this is not one of the readings you're interested in, you can disable it.
    
- Accelerometer: This sensor measures acceleration forces. Since you're not interested in this type of reading, you can disable it.
    
- Gyroscope: This sensor measures angular velocity. You can disable it as well since it's not one of the readings you're interested in.
    
- Luminosity (CC2650 only): This is a light sensor. If your device model is CC2650, this option will be available. You can disable it as well, as it's not related to the `pressure`, `temperature`, or `humidity` readings.
    
- Button press: This indicates a state of a physical button on the device. It's not related to the measurements you want, so you can disable it.

![](../pictures/Pasted%20image%2020230622184622.png)

```python
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
client.subscribe("home/sensor") # subscribing to the topic  
  
  
# The callback for when a PUBLISH message is received from the server.  
def on_message(client, userdata, msg):  
# Deserializing the message payload  
payload = json.loads(msg.payload)  
  
# Check if the received data type is one of the types we're interested in  
if 'pressure' in payload or ('temperature' in payload and 'humidity' in payload):  
# Add the timestamp, location and device label  
payload['timestamp'] = str(datetime.datetime.now())  
payload['location'] = LOCATION  
payload['device'] = DEVICE_TAG  
print(payload)  
# After processing, publish it to another topic or database  
client.publish("home/sensor/processed", json.dumps(payload))  
  
  
client = mqtt.Client()  
client.on_connect = on_connect  
client.on_message = on_message  
  
client.connect(MQTT_BROKER_IP, MQTT_BROKER_PORT, 60)  
  
# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.  
client.loop_forever()
```

This Python script is designed to subscribe to the "home/sensor" topic on your MQTT broker. When a message is published to that topic, the `on_message` function is called with that message. The function then processes the message and publishes the processed data to the "home/sensor/processed" topic.

In this case, your original Node-RED instance is publishing raw sensor data to the "home/sensor" topic. This Python script (which could be running in another Docker container) then subscribes to that topic, processes the data, and publishes the processed data to the "home/sensor/processed" topic.

Another Node-RED flow or another application can subscribe to the "home/sensor/processed" topic to receive and further handle the cleaned data. For example, you could have another Node-RED flow that subscribes to the "home/sensor/processed" topic and writes the processed data to a database, a file, or another service.

The MQTT broker serves as the central hub for this communication. The broker could be running on the same machine as Node-RED and your Python script, or it could be running on a different machine. As long as all your applications can connect to the MQTT broker (i.e., they're all on the same network and the MQTT broker's IP and port are reachable), they can communicate with each other by publishing and subscribing to topics on the broker.

![](../pictures/Pasted%20image%2020230622193336.png)

### build docker file
![](../pictures/Pasted%20image%2020230622194514.png)

![](../pictures/Pasted%20image%2020230622195156.png)


## influx DB
![](../pictures/Pasted%20image%2020230622205121.png)

![](../pictures/Pasted%20image%2020230622210745.png)

---
## Challenges:
Running Node-RED directly on the host environment can indeed simplify some aspects of the development process, particularly when dealing with hardware interfacing and some native dependencies. Direct hardware access is straightforward, and you don't need to manage Docker volumes for persistent data.

However, using Docker also has significant benefits:

1. Isolation: Docker provides a great level of isolation, which means that the Node-RED and its dependencies won't interfere with the system and other applications.

2. Portability: If you ever need to move your application to another system, Docker makes this process straightforward. The application and all its dependencies are in the Docker image, so it will run the same regardless of the host system.

3. Version control and reproducibility: Docker allows for precise control over the environment your application runs in. You can specify versions of Node-RED, Node.js, and any other dependencies. This can make your application more stable and predictable.

4. Microservices architecture: If your project grows to include other services, Docker makes it easy to manage these services independently. This is especially true if you use a tool like Docker Compose.



Act as a senior IOT dev, develop the task:Barometric and environmental readings should be sampled and stored in a database using
json format and include metadata such as: timestamp, signal-readings, location, device- label.

1. The bluepy library in Python can interact with BLE devices, and paho-mqtt can publish data to an MQTT broker
2. use a Python script to read Barometric and environmental data from the SensorTag(TI cc2650) and then publish the data to an MQTT topic (/home/sensor), script can be run on the Raspberry Pi.
3. in Node-RED, you would have a flow with an MQTT in node listening to the /home/sensor topic
4. send it to InfluxDB using the InfluxDB out node.
5. create a database in InfluxDB called sensor_data and create a table called table_data
6. use grafana to visualize the data in the database

currently my docker hosted services are below:
```bash
rex@rex:~/IOTstack $ docker-compose ps
WARNING: Some networks were defined but are not used by any service: nextcloud
    Name                  Command                  State                                       Ports                                 
-------------------------------------------------------------------------------------------------------------------------------------
grafana        /run.sh                          Up (healthy)   0.0.0.0:3000->3000/tcp                                                
influxdb       /entrypoint.sh influxd           Up (healthy)   0.0.0.0:8086->8086/tcp                                                
mosquitto      /docker-entrypoint.sh /usr ...   Up (healthy)   0.0.0.0:1883->1883/tcp                                                
nodered        ./entrypoint.sh                  Up (healthy)   0.0.0.0:1880->1880/tcp                                                
portainer-ce   /portainer                       Up             0.0.0.0:8000->8000/tcp, 0.0.0.0:9000->9000/tcp, 0.0.0.0:9443->9443/tcp
```


**1. Develop the Python script to interact with the SensorTag and publish data to the MQTT broker**

The script should perform the following steps:

- Connect to the SensorTag using `bluepy`.
- Read the barometric and environmental data from the SensorTag.
- Add metadata (timestamp, location, device-label).
- Publish the data to the MQTT broker on the topic `/home/sensor`.


```python
from bluepy.sensortag import SensorTag
from bluepy.btle import Scanner
import paho.mqtt.client as mqtt
import json
import time

SENSOR_TAG_LABEL = "Living Room"
LOCATION = "Auckland"
BROKER = "localhost"

# Scanning for BLE devices
scanner = Scanner()
devices = scanner.scan(2.0)

# Looking for SensorTag
for dev in devices:
    print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        if value == "CC2650 SensorTag":
            SENSOR_TAG_MAC = dev.addr

if not SENSOR_TAG_MAC:
    raise Exception("SensorTag not found")

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
```




Make sure to replace `<device_label>` and `<location>` with your actual device label and location.

This script reads the barometric and environmental data every minute. You can adjust this delay to suit your needs.

**2. Set up the Node-RED flow**

1. Open the Node-RED UI and add an `mqtt in` node.
2. Configure it to listen to the `/home/sensor` topic on your MQTT broker.
3. Connect the `mqtt in` node to a `json` node to convert the incoming string to a JSON object.
4. Connect the `json` node to an `influxdb out` node.
5. Configure the `influxdb out` node to connect to your InfluxDB instance and write data to the `table_data` table in the `sensor_data` database.

**3. Create the database and table in InfluxDB**

You can create the database and table through the InfluxDB UI, CLI, or API. Here's how you do it with the CLI:

1. Access the InfluxDB shell: `docker exec -it influxdb influx`
2. Create the database: `CREATE DATABASE sensor_data`
3. Use the new database: `USE sensor_data`
4. Create the table: Since InfluxDB is a time-series database, you don't need to explicitly create tables. When you write data to a new table, InfluxDB will create it automatically.

**4. Set up Grafana to visualize the data**

1. Add your InfluxDB instance as a data source in Grafana.
2. Create a new dashboard.
3. Add a panel and configure it to display data from the `table_data` table in the `sensor_data` database.
4. Configure the panel to your liking. For example, you can display the barometric and environmental data over time.

I hope this gives you a good start on your IoT project. Let me know if you have any questions or run into any issues.


---

Prepare a formal final report which includes the evidence of examination, design, development and validation. Acceptable word length range is from 1700 to 2000.

This project makes use of best practices in IoT, including the MQTT protocol for publish/subscribe architecture.

# Act as a senior dev, Examination of Barometric and Environmental Signals, the examination must include the things listed below. (keep it simple and relative to my below deployment)

• What can be found from continuous monitoring of barometric pressure and environmental signals.

• How does barometric pressure affect people?

# The deployment uses a Raspberry Pi 4 with a 32-bit operating system,

1.     List our real-world applications using Python for data ETL for IOT devices instead of Javascripts-based solutions and tell why (act as a senior IOT Engineer lists facts)

2.     trying to stay away from node-red since it is built on Node.js, Javascripts upgrade too frequently, easily have components or libraries outdated. Not stable to use.

3.     Hence, I’d rather use Python instead, write some content here about the python `bluepy` cannot connect to Ti sensor tag cc2650, so that we have to use a Pi `hosted node-red`(1st node-red) with sensor tag node to read data from the sensor tag cc2650, connected to a mqtt-out node, publish the topic "/home/sensor/rex/living" in "broker.hivemq.com:1883" a publicly available MQTT broker. 

4.     talk about why using dockerised services:

(1)   fast up and down

(2)   can run anywhere without `server name` issue, for example, if the Pi’s location and network is changed, don’t need to change any python scripts (pointing to MQTT server). Influx server, MQTT server, Grafana server.

(3)   Other advantages please list here, act as a senior IOT Engineer

5.     using IOTStack Github (https://sensorsiot.github.io/IOTstack/), IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi. run Docker-compose, and 2nd docker-hosted `Node-RED`, `InfluxDB`, `Mosquitto` (MQTT broker), and `Grafana` are hosted .

6.     Introduce about what sensors cc2650 has, and below:

-        IR Temperature: This is typically used to measure the temperature of an object that the sensor is pointed at, using infrared technology. As it's not explicitly the `temperature` reading you're interested in, you can disable it.

-        Magnetometer: This sensor measures magnetic fields. As this is not one of the readings you're interested in, you can disable it.

-        Accelerometer: This sensor measures acceleration forces. Since you're not interested in this type of reading, you can disable it.

-        Gyroscope: This sensor measures angular velocity. You can disable it as well since it's not one of the readings you're interested in.

-        Luminosity (CC2650 only): This is a light sensor. If your device model is CC2650, this option will be available.

-        You can disable it as well, as it's not related to the `pressure`, `temperature`, or `humidity` readings.

7.     Still trying to utilise with Python for data cleaning(Time stamp, location, filtered parameters, device_tag). The monitored data is `pressure`, `humidity`, and `temperature`. Also used `pyho` lib to connect to follow the best practice with MQTT. Python script listen to the `/home/sensor` topic (raw data from the PI-hosted node-red) and the cleaned data push to a topic called `/home/sensor/processed`.

8.     Docker-hosted node-red (2nd) has another MQTT-out listen to `/home/sensor/processed`, and connected to another node called `influxDB in` node.

9.     The `influxDB in` set up with the docker-hosted influxDB (rex.local again for the server address). Here is to store data

10.  Docker-hosted Grafana to visualize data from reading from InfluxDB



---

