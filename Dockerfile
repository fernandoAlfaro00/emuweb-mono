FROM ubuntu:24.04
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG=en_US.utf8

RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
apt-get install -y --no-install-recommends \
libssl-dev libasound2-dev libgtk-3-0 libxtst6 \
libsm6 libpulse0 librtmp1 avahi-utils \
wget \
unzip \
retroarch \
xvfb \
pipewire \
pipewire-pulse \
ffmpeg \
wireplumber \
pulseaudio-utils \
libportaudio2 \
pipewire-audio-client-libraries \
alsa-utils \
ca-certificates \
dbus-x11 \
curl \
rtkit \
&& apt-get clean && rm -rf /var/lib/apt/lists/ 
# && useradd -m user -G video,audio \

RUN wget -O /tmp/nestopia_libretro.so.zip \
https://buildbot.libretro.com/nightly/linux/x86_64/latest/nestopia_libretro.so.zip \
&& unzip /tmp/nestopia_libretro.so.zip -d /usr/lib/x86_64-linux-gnu/libretro

ARG src="./retroarch/.config/autoconfig"
ARG target=".config/retroarch/autoconfig/udev"

ENV DBUS_FATAL_WARNINGS=0 
ENV DISPLAY=:99
ENV DISABLE_RTKIT=y
ENV XDG_RUNTIME_DIR=/tmp
ENV PIPEWIRE_RUNTIME_DIR=/tmp
ENV PULSE_RUNTIME_DIR=/tmp
ENV ROM=""

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /run/dbus /dev/snd
RUN dbus-daemon --system --fork

COPY ./webrtc/bin/webrtc-streamer /usr/local/bin/
COPY ./webrtc/share/webrtc-streamer/ /usr/local/share/webrtc-streamer/

# USER user
# WORKDIR /home/user
WORKDIR /root

# Carpeta para las ROMs y configuración
RUN mkdir -p roms config .config/retroarch
COPY ./retroarch/.config/retroarch.cfg .config/retroarch/retroarch.cfg

RUN mkdir -p .config/retroarch/autoconfig/udev
COPY ${src} ${target}

EXPOSE 8000

CMD ["/entrypoint.sh"]