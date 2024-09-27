

# Getting started
This is an example project to monitor internet speed in Raspberry Pi
and send the monitored data to InfluxDb so as to view in dashboard i.e Grafana.
The python script as well as InfluxDb and Grafana are running in docker containers.

## Hardware requirements
A Raspberry Pi. Used Raspberry Pi 4B for development.

## Additional configuration in Pi
    * Set static ip address in Pi so that the device is reachable over known IP address in local network
    * Docker, Docker-Compose should be installed 

## Ports
    * Influxdb: 8086
    * Grafana: 3000

## Development environment 
Setup development environment by running Influxdb and Grafana in docker containers
`docker compose -f docker-compose-dev.yaml up -d`
The environment variables are defined in the ./config/*.env files.

## Continuous internet speed monitoring 
Run docker compose 
`docker compose -f docker-compose.yaml up -d`
The environment variables are defined in the ./config/*.env files.

# Acknowledgments
Inspiration 
    https://pimylifeup.com/raspberry-pi-internet-speed-monitor/
    https://pimylifeup.com/raspberry-pi-docker/

