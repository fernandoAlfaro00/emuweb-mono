#!/bin/bash
set -e
sudo modprobe  v4l2loopback video_nr=1
sudo modprobe uinput
export ENDPOINT_WS=$(hostname -I | awk '{print $1}')
docker compose up -d --build --remove-orphans