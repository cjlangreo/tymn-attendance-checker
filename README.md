# README


## Clone the repository
`git clone https://github.com/BirbDoy1221/scrcpy-facial-recognition`


## Create a virtual environment and install required modules
`python3.10 -m venv .venv`

`source .venv/bin/activate`

Check if your pip3 uses the venv by running `which pip3` which returns the pip3 location.

`pip3 install -r requirements.txt`

## Running the recognition test

    Do this to use your phone as a camera
    1. Create a new terminal
    2. Execute `sudo modprobe v4l2loopback`
    3. Navigate to src/webcamera
    4. Pair your device with `adb pair`
    5. Connect your device with `adb connect`
    6. `bash camera.sh`

1. `python3 src/main.py`