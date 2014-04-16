##What is VARVI?##

**VARVI** (heart rate Variability Analysis in Response to Visual stImuli) is a free software tool developed to perform heart rate variability (HRV) analysis in response to different visual stimuli. The tool was developed after realizing that this type of studies are becoming popular in fields such as psychiatry, psychology and marketing, and taking into account the lack of specific tools for this purpose.

**VARVI** allows the users to obtain Heart Rate (HR) records from subjects who are watching video files or sets of images. In case video files are used, each video file will be labelled with a tag, and the HR record will contain information of these tags with their corresponding time intervals. When using sets of images, users specify directories containing images, and each directory will be associated with a tag. 

##What does VARVI need to work?##

**VARVI** is in a early stage of development, and at this moment it works with the following restrictions:
* It runs on GNU Linux and Windows operating systems.
* It depends on external software to show the video files (see installation procedure).
* Images must be in .jpg format (.jpg and .jpeg extensions)
* It depends on [Python](http://www.python.org) and the [PyGame](http://www.pygame.org/news.html) and [PyBluez](http://pybluez.googlecode.com) libraries.
* **VARVI** obtains the data from a [Polar Wearlink®+ transmitter with bluetooth®](http://www.polar.com/en/products/accessories/Polar_WearLink_transmitter_with_Bluetooth) band. This band must be linked with the computer where VARVI is running.  For testing purposes, a simulation mode (without band) is available that creates random data.
