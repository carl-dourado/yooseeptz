#!/bin/bash
cd /home/carl
source venv_camera/bin/activate
export DISPLAY=:0
python3 ptz_floating.py >> /tmp/ptz.log 2>&1
