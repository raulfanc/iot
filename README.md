This repository includes the necessary documentation and resources for deploying an IoT project that involves environmental monitoring on both local and cloud.

## Acknowledgments

This project makes use of best practices in IoT and Cloud deployments, including the MQTT protocol for publish/subscribe architecture.

---

## Local Deployment (For Testing)

### System Architecture

The local deployment uses a Raspberry Pi 4 with a 32-bit operating system, and Docker containers hosting Node-RED, InfluxDB, Mosquitto (MQTT broker), and Grafana.

#### Prerequisites

1. Raspberry Pi 4 with 32-bit OS
2. Docker and Docker-Compose installed on the Raspberry Pi
3. Mosquitto (MQTT broker)
4. Node-red (flow control)
5. InfluxDB (light weight DB for IOT)
6. Grafana (visualization to present data)
7. Raspberry Pi connect to home Wi-Fi
8. encrypted remote access to Raspberry Pi (firewall, static IP, VPN, etc.)

![](pictures/Pasted%20image%2020230604234800.png)

![](pictures/Pasted%20image%2020230604234813.png)

#### Deployment Steps

1. Clone the repository to your local Raspberry Pi 4 system.
2. Navigate to the directory where the docker-compose.yml file is located.
3. Run the following command to start the Docker containers: `docker-compose up -d`
4. Access Node-RED, InfluxDB, Mosquitto, and Grafana on their respective ports.

---

## Cloud Deployment

### System Architecture

The cloud deployment involves a Raspberry Pi 4 with a 32-bit operating system sending data to an AWS IoT Core broker. The data is then streamed to DynamoDB through AWS Kinesis, and AWS QuickSight is used for data visualization.

#### Prerequisites

1. Raspberry Pi 4 with 32-bit OS
2. AWS account with access to AWS IoT Core, Kinesis, DynamoDB, and QuickSight
3. Terraform fast provisioning AWS related services above
4. Node-RED and Ti SensorTag dependencies installed on the Raspberry Pi 
5. Internet access for the Raspberry Pi
6. remote access to Raspberry Pi (firewall, static IP, VPN, etc.)

#### Deployment Steps

1. Clone the repository to your local Raspberry Pi 4 system.
2. Set up your AWS IoT Core, Kinesis, DynamoDB, and QuickSight with Terraform.
3. Replace the placeholders in the Node-RED flow for AWS IoT Core with your credentials.
4. Deploy the Node-RED flow.
5. Check the incoming data on AWS IoT Core, and verify if the data is being streamed to DynamoDB and visualized in QuickSight correctly.

---

## Contribution

Contributions are welcome! Please feel free to submit a pull request.

---
## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

---
