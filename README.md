# Getting started
You should install nmap on your computer (nmap.org)

If connected to Shihao's hotspot or at Shihao's house, first search for the device you want:
```
nmap -sn 192.168.1.*
```
and connect to it:
```
ssh dev@ip #subsitute dev with pi or nvidia, and use the ip found above
```
The password for these devices (and most things Shihao has set up) is getmeout
Your prompt should begin with a (cv), if it doesn't, run:
```
source ~/.bashrc
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

