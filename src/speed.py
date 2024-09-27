import os
import re
import subprocess
import logging
import time

from pathlib import Path
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# ************* LOGGING CONFIG **************** #
log_format = "%(asctime)s %(message)s"
internet_speed = "internetspeed"    
logging.basicConfig(filename=f'{internet_speed}.log', format=log_format, level=logging.INFO)
logger = logging.getLogger(internet_speed)

# ************* INFLUXDB CONFIG **************** #

# Influxdb env variables are loaded when the `monitor` container is running. 
# If the container is not running i.e during development, the env file is read by load_dotenv(). 
if os.getenv("DOCKER_INFLUXDB_INIT_ORG", None) is None:
    influxdb_env_file = Path(__file__).parent.parent.joinpath('config/influxdb.env') 
    load_dotenv(dotenv_path=influxdb_env_file)
    
    monitor_env_file = Path(__file__).parent.parent.joinpath('config/monitor.env') 
    load_dotenv(dotenv_path=monitor_env_file)

bucket = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")
org = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
token = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
ip_address = os.getenv("RASPBERRY_IP")
port = os.getenv("INFLUXDB_PORT")

url = f"http://{ip_address}:{port}"
client = InfluxDBClient(
    url=url, token=token, org=org 
)
write_api = client.write_api(write_options=SYNCHRONOUS)
# ************* INFLUXDB CONFIG **************** #

count = 1
while count < 6:
    count += 1
    response = subprocess.Popen(
        "/usr/bin/speedtest --accept-license --accept-gdpr", shell=True, stdout=subprocess.PIPE).stdout.read()

    decoded = response.decode("utf-8")

    latency_search = re.search(r"Latency:\s+(.*?)\s", decoded, re.MULTILINE)
    download_search = re.search(r"Download:\s+(.*?)\s", decoded, re.MULTILINE)
    upload_search = re.search(r"Upload:\s+(.*?)\s", decoded, re.MULTILINE)
    jitter_search = re.search(r"Latency:.*?jitter:\s+(.*?)ms", decoded, re.MULTILINE)

    latency = latency_search.group(1)
    download = download_search.group(1)
    upload = upload_search.group(1)
    jitter = jitter_search.group(1)

    logger.info(f"Latency: {latency} ms")
    logger.info(f"Download: {download} Mbps")
    logger.info(f"Upload: {upload} Mbps")
    logger.info(f"Jitter: {jitter} ms")

    # write to InfluxDb
    influx_point = Point("Measurement") \
            .tag("Host", "WhiteSwan") \
            .field("Download", float(download)) \
            .field("Upload", float(upload)) \
            .field("Jitter", float(jitter)) \
            .field("Latency", float(latency))

    write_api.write(bucket=bucket, org=org, record=influx_point)

    time.sleep(30)

