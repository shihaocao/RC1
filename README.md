# Getting started
You should install nmap on your computer (nmap.org)

If not connected to Shihao's house, it is possible to connect to the nvidia via SSH using Shihao's Home IP Address. This may vary from time to time, so get the IP from a teammate.
Otherwise, if connected to Shihao's hotspot or at Shihao's house, first search for the device you want:
```
nmap -sn 192.168.1.*
```
and connect to it:
```
ssh dev@ip #subsitute dev with pi or nvidia, and use the ip found above
```
The password for these devices (and most things Shihao has set up) is an official oral tradition. Get the password from a teammate.
Your prompt should begin with a (cv), if it doesn't, run:
```
source ~/.bashrc
```
## Testing the Pi
Install MissionPlanner if not already installed. Once installed, plug in the radio telemetry dongle and press connect at the top right of MissionPlanner.
Then connect the Raspberry Pi to the side of the Pixhawk using a USB cable.

Open the FC folder and run mavproxy.py to test the connection:
```
python2 /home/pi/.virtualenvs/cv/bin/mavproxy.py
```
If this is successful, to start the mission run:
```
cd RC1/FC
python2 mission.py
```

## Files and Folders
FC		Flight computer code
nvidia	     	Nvidia Tegra-specific computer vision code
ocr	 	Tesserect optical character recognition code
pi	 	Raspberry Pi- specific computer vision code
vids		Videos used for CV and OCR testing, not synced to the gihub repo
tensorflow	Tests for tensorflow ocr
IMAGEDETECTION	?
Tests		Old CV code
CV computer vision
COMMUNICATION socket communication between Pi and Ground Station
