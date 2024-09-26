import os
import re
import subprocess
import logging
import time

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INTERNET_SPEED = "InternetSpeed"    # should match with bucket defined in InfluxDb 
HOST_IP = "192.168.0.206"

# ************* LOGGING CONFIG **************** #
LOG_FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(filename='internetspeed.log', format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(INTERNET_SPEED)
# ************* LOGGING CONFIG **************** #

"""
# ************* INFLUXDB CONFIG **************** #
load_dotenv()
bucket = INTERNET_SPEED
org = "WhiteSwan"
token = os.getenv("INFLUXDB_TOKEN")
url = f"http://{HOST_IP}:8086"
client = InfluxDBClient(
    url=url, token=token, org=org 
)
write_api = client.write_api(write_options=SYNCHRONOUS)
# ************* INFLUXDB CONFIG **************** #
"""

# while True:
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

print(f"Latency: {latency} ms")
"""
# write to InfluxDb
influx_point = Point("Measurement") \
        .tag("Host", "WhiteSwan") \
        .field("Download", float(download)) \
        .field("Upload", float(upload)) \
        .field("Jitter", float(jitter)) \
        .field("Latency", float(latency))
write_api.write(bucket=bucket, org=org, record=influx_point)

time.sleep(60)
"""
