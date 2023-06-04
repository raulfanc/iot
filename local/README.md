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
    image: influxdb:latest
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

