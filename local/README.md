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

```bash
```

- check mDNS
```bash
sudo apt-get install avahi-daemon
```

- enable avahi-daemon when starting
```bash
/lib/systemd/systemd-sysv-install enable avahi-daemon
```
or.....
```bash
sudo systemctl enable avahi-daemon
```

- update the localhost
```nano
127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1       rex
```

set up cc2650 TI sensortag with node-red:
- install nodejs
```bash
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs
```
- and then refer to [this guide](/cloud/Ti%20Sensor_Node-Red.md) for the rest of the setup

---
## Challenges:
Running Node-RED directly on the host environment can indeed simplify some aspects of the development process, particularly when dealing with hardware interfacing and some native dependencies. Direct hardware access is straightforward, and you don't need to manage Docker volumes for persistent data.

However, using Docker also has significant benefits:

1. Isolation: Docker provides a great level of isolation, which means that the Node-RED and its dependencies won't interfere with the system and other applications.

2. Portability: If you ever need to move your application to another system, Docker makes this process straightforward. The application and all its dependencies are in the Docker image, so it will run the same regardless of the host system.

3. Version control and reproducibility: Docker allows for precise control over the environment your application runs in. You can specify versions of Node-RED, Node.js, and any other dependencies. This can make your application more stable and predictable.

4. Microservices architecture: If your project grows to include other services, Docker makes it easy to manage these services independently. This is especially true if you use a tool like Docker Compose.
