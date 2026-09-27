#!/bin/bash
cd /home/carl
python3 -m venv venv_camera
source venv_camera/bin/activate
pip install opencv-python pillow onvif_zeep tk
python3 camera_yoosee.py
