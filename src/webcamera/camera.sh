#!/bin/bash

sudo ./scrcpy --video-source=camera --camera-size=1920x1080 --camera-facing=back --v4l2-sink=/dev/video0 --no-audio --no-control --no-window