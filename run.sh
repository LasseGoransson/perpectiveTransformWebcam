#!/usr/bin/env bash

# Create video device 2
sudo modprobe v4l2loopback video_nr=2 exclusive_caps=1

python transform.py
