#!/bin/bash
set -e
sudo modprobe  v4l2loopback video_nr=1
sudo modprobe uinput
docker compose up -d --build