##What is VARVI?##

**VARVI** (heart rate Variability Analysis in Response to Visual stImuli) is a free software tool developed to perform heart rate variability (HRV) analysis in response to different visual stimuli. The tool was developed after realizing that this type of studies are becoming popular in fields such as psychiatry, psychology and marketing, and taking into account the lack of specific tools for this purpose.

**VARVI** allows the users to obtain Heart Rate (HR) records from subjects who are watching video files or a slideshow of images. Each video file or directory of images will be labelled with a tag, and the HR record will contain information of these tags with their corresponding time intervals. 

##What does VARVI need to work?##

**VARVI** is in a very early stage of development, and at this moment it works with the following restrictions:
* It runs only on GNU Linux operating system.
* It depends on *mplayer* ([http://www.mplayerhq.hu/](http://www.mplayerhq.hu/)) to play the video files. On Debian/Ubuntu based systems, *mplayer* can be installed using: `sudo apt-get install mplayer`
* It depends on *feh* to show the images. On Debian/Ubuntu based systems, *feh* can be installed using: `sudo apt-get install feh`
* *PyBluez* libraries must be installed on the system ([http://pybluez.googlecode.com](http://pybluez.googlecode.com)). On Debian/Ubuntu based systems, this library can be installed using: `sudo apt-get install python-bluez`
* **VARVI** obtains the data from a [Polar Wearlink®+ transmitter with bluetooth®](http://www.polar.com/en/products/accessories/Polar_WearLink_transmitter_with_Bluetooth) band. This band must be linked with the computer where **VARVI** is running. For testing purposes, a simulation mode is available that creates random data. It can be invoked using the *-n* argument when running the program: `python VARVI.py -n configfile.conf outputfile`
