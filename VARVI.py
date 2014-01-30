#!/usr/bin/python
# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------
#    VARVI: heart rate Variability Analysis in Response to Visual stImuli
#    Copyright (C) 2014  Milegroup - Dpt. Informatics
#       University of Vigo - Spain
#       www.milegroup.net

#    Author:
#      - Leandro Rodríguez-Liñares
#      - Arturo Méndez
#      - María José Lado
#      - Xosé Antón Vila
#      - Pedro Cuesta Morales

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# -------------------------------------------------------------------------

import argparse
import sys
import os
import time
from datetime import datetime,timedelta
from VARVI_functions import *

defaultgap = 2.0 # Gap in seconds between videos
delay = 0.5

parser = argparse.ArgumentParser(description='VARVI: heart rate Variability Analysis in Response to Visual stImuli')
parser.add_argument('-v','--verbose', action='store_true', help='verbose mode on', default=False, dest="verbosemode")
parser.add_argument('-d','--dirout', metavar='dir', help='output directory', dest="dirout", required=False, default=".")
parser.add_argument('-n','--no-band', action='store_true', help='no band required', default=False, dest="nobandmode")

parser.add_argument('config_filename', help='file containing the description of the experiment')
parser.add_argument('record_name', help='name of files containing the data (record_name.rr.txt and record_name.tag.txt)')


args = parser.parse_args()

if args.verbosemode:
	print "\nVARVI: heart rate Variability Analysis in Response to Visual stImuli\n"

if sys.platform != "linux2":
	print "   *** ERROR: VARVI must be run on a linux system"
	sys.exit(0)

if not os.path.isfile("/usr/bin/mplayer"):
	print "   *** ERROR: mplayer must be installed on the system"
	sys.exit(0)

if args.verbosemode:
	print "   Processing file:",str(args.config_filename)

settings, videos, tags = GetSettings(args.config_filename,args.verbosemode)

if "gap" not in settings.keys():
	settings["gap"]=defaultgap


for video in videos:
	if not os.path.isfile(video):
		print "   *** ERROR: file %s does not exist" % video
		sys.exit(0)



if args.verbosemode:
	if args.nobandmode:
		print "   No band... simulating data"
	if settings["random"]:
		print "   Random mode"
	else:
		print "   Sequential mode"
	print "   Gap between videos:",str(settings["gap"]),"seconds"
	print "   No. of videos:",str(settings["nvideos"])
	print "   Device:",settings["device"]
	for n in range(settings["nvideos"]):
		print "   Video %02d" % (n+1)
		print "      Tag: %s" % tags[n]
		print "      File: %s" % videos[n]
	
if not args.nobandmode:
	try:
		socketBT=LinkPolarBand(settings["device"],args.verbosemode)
	except NoBand:
		print "   *** ERROR: no bluetooth band was detected"
		sys.exit(0)
	except KeyboardInterrupt:
		print "   *** Program interrupted by user... exiting"
		sys.exit(0)

if settings["random"]:
	from random import shuffle
	indexes=range(len(videos))
	shuffle(indexes)
	videos_tmp = [videos[i] for i in indexes]
	tags_tmp=[tags[i] for i in indexes]
	videos=videos_tmp
	tags=tags_tmp


fileHR = args.dirout+os.sep+args.record_name+".rr.txt"
fileTags = args.dirout+os.sep+args.record_name+".tag.txt"

if args.nobandmode:
	dataThread=DataSimulation(args.verbosemode)
else:
	dataThread=DataAdquisition(socketBT,args.verbosemode)

try:
	dataThread.start()

	# try:
	# 	dataThread=DataAdquisition(socketBT)
	# 	datosThread.start()
	# except:
	# 	print "   *** ERROR: unspecific problem beginning data adquisition"
	# 	sys.exit(0)

	while (True):
		time.sleep(delay)
		if dataThread.DataIsCorrect():
			break;

	zerotime=datetime.now()
	dataThread.BeginAdquisition(zerotime)
	time.sleep(settings["gap"])


	datatags=[]

	for n in range(len(videos)):
		video=videos[n]
		tag=tags[n]
		if args.verbosemode:
			print "   Video %s started" % tag
		
		command = 'mplayer -really-quiet -fs %s  2> /dev/null' % video
		
		beg = (datetime.now()-zerotime).total_seconds()
		if  args.verbosemode:
			print "      Instant: %fs." % beg
		os.system(command)
		end = (datetime.now()-zerotime).total_seconds()

		length=end-beg
		if args.verbosemode:
			print "   Video %s ended (length %f seconds)" % (tag,length)
			print "      Instant: %fs." % end

		datatags.append((tag,beg,end))
		time.sleep(settings["gap"])


	datarr=dataThread.EndAdquisition()
	if not args.nobandmode:
		dataThread.EndBTConnection()

except KeyboardInterrupt:
	print "   *** Program interrupted by user... exiting"
	dataThread.EndBTConnection()
	dataThread.join()
	sys.exit(0)

SaveRRValues(datarr, fileHR, args.verbosemode)
SaveTags(datatags, fileTags, args.verbosemode)

