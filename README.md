##What is VARVI?##

**VARVI** (heart rate Variability Analysis in Response to Visual stImuli) is a free software tool developed to perform heart rate variability (HRV) analysis in response to different visual stimuli. The tool was developed after realizing that this type of studies are becoming popular in fields such as psychiatry, psychology and marketing, and taking into account the lack of specific tools for this purpose.

**VARVI** allows the users to obtain Heart Rate (HR) records from subjects who are watching video files or sets of images. In case video files are used, each video file will be labelled with a tag, and the HR record will contain information of these tags with their corresponding time intervals. When using sets of images, users specify directories containing images, and each directory will be associated with a tag. 

##What does VARVI need to work?##

**VARVI** is in a early stage of development, and at this moment it works with the following restrictions:
* It runs on GNU Linux and Windows operating systems.
* It depends on external software to show the images and video files (see installation procedure below).
* Images must be in .jpg format (.jpg and .jpeg extensions)
* It depends on [Python](http://www.python.org) and the [PyBluez](http://pybluez.googlecode.com) libraries.
* **VARVI** obtains the data from a [Polar Wearlink®+ transmitter with bluetooth®](http://www.polar.com/en/products/accessories/Polar_WearLink_transmitter_with_Bluetooth) band. This band must be linked with the computer where VARVI is running.  For testing purposes, a simulation mode (without band) is available that creates random data.

##Installation on GNU Linux systems##

* Download the **zip** file containing the software and uncompress it.
* **VARVI** depends on [mplayer](http://www.mplayerhq.hu) to play the video files and on [feh](http://feh.finalrewind.org/) viewer to show the image files. Besides, [PyBluez](http://pybluez.googlecode.com) libraries must be installed on the system. On Debian/Ubuntu based systems, theses dependencies can be installed using the following command in a terminal: `sudo apt-get install mplayer feh python-bluez`

##Installation on Windows systems##

* Download the **zip** file containing the software and uncompress it.
* Install [Python](http://www.python.org/) and the [PyBluez](http://pybluez.googlecode.com) libraries on the system.
* **VARVI** depends on [mplayer](http://www.mplayerhq.hu) to play the video files and on [JPEGView](http://sourceforge.net/projects/jpegview/) viewer to show the image files. Download and umcompress both programs. **VARVI** requires the structure of directories to be as shown in the figure:

![Alt text](./directories.png)

where
+ **Varvi** folder must contain the **VARVI.py** and **VARVI_functions.py** files.
+ The folder containing the **mplayer.exe** file must be renamed to **mplayer**
+ The folder containing the **JPEGView.exe** file must be renamed to **JPEGView**
* The **JPEGView/JPEGView.ini** file must be opened with a file editor and the **WrapAroundFolder** option must be set to **false** for the image viewer to work properly.

