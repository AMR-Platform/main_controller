#!/usr/bin/env bash

# 1) Configure Ethernet
ip addr flush dev eth0
ip addr add 192.168.198.1/24 dev eth0
ip link set eth0 up

# 2) Allow X11 forwarding for root
export DISPLAY=:0
export XAUTHORITY=/home/navod/.Xauthority
xhost +local:root

# 3) Show splash screen
/usr/local/bin/splash.py &

# 4) Start your container (replace CONTAINER_NAME below)
/usr/bin/docker start -ai CONTAINER_NAME
