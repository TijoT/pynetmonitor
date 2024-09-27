# Official python image based on debian 12
FROM python:3.12.6-slim-bookworm

# working directory in the container
WORKDIR /usr/app

# install apt packages required for speedtest
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt install -y --no-install-recommends apt-transport-https gnupg1 dirmngr lsb-release curl gpg \ 
    && curl -L https://packagecloud.io/ookla/speedtest-cli/gpgkey | gpg --dearmor \
        | tee /usr/share/keyrings/speedtestcli-archive-keyring.gpg >/dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/speedtestcli-archive-keyring.gpg] https://packagecloud.io/ookla/speedtest-cli/debian/ $(lsb_release -cs) main" \
        | tee  /etc/apt/sources.list.d/speedtest.list \
    && apt update -y --no-install-recommends \
    && apt install speedtest -y --no-install-recommends

COPY requirements.txt /usr/app/    

RUN pip install -r requirements.txt

# COPY all files except those defined in .dockerignore
COPY . /usr/app/ 

# Smoke test to verify that the speedtest binary can be started in container
# CMD [ "speedtest",  "--accept-license", "--accept-gdpr"]

# Execute python script
CMD [ "python3",  "speed_monitor.py"]