## Configure Node-Red Server on Raspberry Pi Device
Base resource is [Node-Red Documentation](https://nodered.org/docs/getting-started/raspberrypi).

Run the following commands on Raspberry Pi Device to install and configure Node-Red Server

1. **install** `Node-Red Server`, referring to [official link](https://nodered.org/docs/getting-started/raspberrypi)
```shell
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```
**in case** it's not working, for instance, your system is not supporting the `bash` above.
Using `wget` then have the downloaded executable with `chmod +x`

2. Run As a **Linux Service**
   **enable** the `Node-Red Server` to **start at boot**
   ```shell
   sudo systemctl enable nodered.service
   ```

   2**disable the automatic start** of the `Node-Red Server`
   ```shell
   sudo systemctl disable nodered.service
   ```

   3**stop the currently running** `Node-Red Server`
   ```shell
   sudo systemctl stop nodered.service
   ```

   4**start** the `Node-Red Server`
   ```shell
   sudo systemctl start nodered.service
   ```
   
3. Run manually (Debug Purpose)
   1. **Start** Service
   ```shell
   node-red-start
   ```

   2. **Stop** Service
   ```shell
   node-red-stop
   ```
   
   3. **Restart** Service
   ```shell
   node-red-restart
   ```
   
   4. **Display Logs** of the Service
   ```shell
   node-red-log
   ```

4. Connect with Node-Red UI
    1. Open Browser on the Laptop
    2. Navigate to `http://<the ip address>:1880`
replace the the ip address appearing in the terminal

---

`timestamp` buttons
- msg.payload

`debug` button
- debug message click

`deploy` red button
- going to be running on the server
- a prompt green pop window will notify the result

then need to flow to the MQTT broker: [Mosquitto](https://mosquitto.org/) or HiveMQ

`mqtt out` button added in Node-red 
1. add `server` (using either mosquitto or hivemq)
2. add `Topic`
3. add `QoS` , 0, 1 or 2, means sender. `Retain` (need some research on this)

open the GUI or interface software to configure the `broker` (generate a new `Client ID` if using local software)

subscribe the topic just created from Node-Red

create a function from Node-red
```java
var v1 = Number(msg.payload);
var v2 = v1*4+40;
msg.payload =v2;
return msg;
```

connect to another `debug` button, and have the gui to listen to the new topic to test.







