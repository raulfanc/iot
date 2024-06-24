
`gpio in` and `gpio out` with `Palette` to connect the TI **sensortag** not working, need to go to official doc to find the solution, see [link](https://flows.nodered.org/node/@ppatierno/node-red-node-sensortag)


## Configure Ti Sensor to work with Node-Red
Base resource are
- [Node-Red-Node-Sensortag Documentation](https://flows.nodered.org/node/@ppatierno/node-red-node-sensortag).


1. Set-up the Ti Sensor
   1. Insert a battery into the Sensor
   2. You can see the green light is starting blinking
<br><br>

2. Check the Ti Sensor
   1. Install **TI Sensor Tag App** on your iPhone
   2. Select the `CC2650 Sensor` Tag Device from the **Available bluetooth device** list
   3. Connect and Check the Data
<br><br>

3. Install Sensor Node in Node-Red
   1. Install Bluetooth Driver5
   ```shell
    sudo apt-get install libbluetooth-dev libudev-dev pi-bluetooth
    sudo setcap cap_net_raw+eip $(eval readlink -f `which node`)
   ```
   2. since the node-red is done by docker-compose, according to my [docker-compose file](/local/docker-compose-v2.yml)
   ```bash
   cd ~/node-red/data
   npm install @ppatierno/node-red-contrib-sensortag
   ```

4. restart the node-red

5. Test the Sensor Data
   1. Add `sensorTag` node into **Flow** in `Node-Red`
   2. choose the parameters I wanted to monitor from that button config window.
   3. UUID: optional
   4. Add `debug` node into **Flow**
   5. Connect both nodes
   6. Check on the `Debug Console`

6. create a `exec` node button
- to have python script
- `Command` 
- refer to below to read Raspberry's CPU usage:
```python
#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
 

while True:

try:

tFile = open('/sys/class/thermal/thermal_zone0/temp')

temp = float(tFile.read())

tempC = temp/1000

if tempC > 43.5:

print "HOT"

else:

print "COLD"

except:

tFile.close()

GPIO.cleanup()

exit
```


