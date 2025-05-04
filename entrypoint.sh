#!/bin/bash
set -e

rm -f /tmp/.X99-lock

export  XDG_RUNTIME_DIR=/tmp
export  PIPEWIRE_RUNTIME_DIR=/tmp
export  PULSE_RUNTIME_DIR=/tmp

echo "Starting Xvfb..."
Xvfb $DISPLAY -screen 0 1280x720x24 &

echo "Starting PipeWire..."
pipewire &
echo "Starting wireplumber..."
wireplumber &
echo "Starting pulse..."
pipewire-pulse &

sleep 2
echo "Starting set default audios interfaces..."
pactl load-module module-virtual-sink sink_name=v1
pactl set-default-sink input.v1
pactl set-default-source input.v1.monitor

sleep 2
echo "Starting retroarch..."
retroarch --verbose -c /root/.config/retroarch/retroarch.cfg -L /usr/lib/x86_64-linux-gnu/libretro/nestopia_libretro.so /root/roms/$ROM &

echo "Starting capturing..."
ffmpeg -f x11grab -video_size 1280x720 -i $DISPLAY -f v4l2 /dev/video1 &

echo "Running Server webRTC..."
sed "s|__ENDPOINT_WS__|${ENDPOINT_WS}|g" /usr/local/share/webrtc-streamer/html/env.template.js > /usr/local/share/webrtc-streamer/html/env.js
webrtc-streamer -w /usr/local/share/webrtc-streamer/html -C /usr/local/share/webrtc-streamer/config.json &


tail -f /dev/null 