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
import glob
from datetime import datetime,timedelta
from VARVI_functions import *

defaultgap = 2.0 # Gap in seconds between videos
defaultduration = 10.0 # Duration in seconds for images
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

sysplat = sys.platform

if sysplat != "linux2" and sysplat != "win32":
	print "   *** ERROR: VARVI must be run on a linux or windows system"
	sys.exit(0)




if args.verbosemode:
	print "   Processing file:",str(args.config_filename)

settings, media, tags = GetSettings(args.config_filename,args.verbosemode)

if "gap" not in settings.keys():
	settings["gap"]=defaultgap

if settings["mode"]=="images":
	if "duration" not in settings.keys():
		settings["duration"]=defaultduration

if settings["mode"]=="videos":
	videos=list(media)
	for video in videos:
		if not os.path.isfile(video):
			print "   *** ERROR: file %s does not exist" % video
			sys.exit(0)

if settings["mode"]=="images":
	images = len(media)*[None]
	imagesDirs = len(media)*[None]
	for i in range(len(media)):
		if not os.path.isdir(media[i]):
			print "   *** ERROR: directory %s does not exist" % media[i]
			sys.exit(0)
		files = insensitive_glob( os.path.join(media[i], '*.jpg') ) + insensitive_glob( os.path.join(media[i], '*.jpeg') ) 
		if len(files)==0:
			print "   *** ERROR: directory %s contains no .jpg or .jpeg files" % media[i]
			sys.exit(0)
		images[i]=files
		imagesDirs[i]=media[i]




if args.verbosemode:
	if args.nobandmode:
		print "   No band... simulating data"
	else:
		print "   Device:",settings["device"]
	if settings["mode"]=='images':
		print "   Media: images"
	else:
		print "   Media: videos"
	if settings["random"]:
		print "   Random mode"
	else:
		print "   Sequential mode"

	if settings["mode"]=='videos':
		print "   Gap between videos:",str(settings["gap"]),"seconds"
		print "   No. of videos:",str(len(videos))
		for n in range(settings["nmedia"]):
			print "   Video %02d" % (n+1)
			print "      Tag: %s" % tags[n]
			print "      File: %s" % videos[n]

	if settings["mode"]=='images':
		print "   Initial and final gap:",str(settings["gap"]),"seconds"
		print "   Duration of images:",str(settings["duration"]),"seconds"
		print "   No. of directories:",str(settings["nmedia"])
	
if settings["mode"]=='videos':

	if sysplat == "linux2":
		sysexecMPlayer = "/usr/bin/mplayer"
		if not os.path.isfile(sysexecMPlayer):
			print "   *** ERROR: mplayer must be installed in the system"
			sys.exit(0)

	if sysplat == "win32":
		import inspect, os
		varvipath=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
		sysexecMPlayer = os.path.abspath(varvipath+"\..\mplayer\mplayer.exe")
		if not os.path.isfile(sysexecMPlayer):
			print "   *** ERROR:",sysexecMPlayer,"not found"
			print "   It seems that mplayer is not installed in the system"
			sys.exit(0)

if settings["mode"]=='images':

	if sysplat == "linux2":
		sysexecViewer = "/usr/bin/feh"
		if not os.path.isfile(sysexecViewer):
			print "   *** ERROR: feh must be installed in the system"
			sys.exit(0)

	if sysplat == "win32":
		import inspect, os
		varvipath=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
		sysexecViewer = os.path.abspath(varvipath+"\..\JPEGView\JPEGView.exe")
		if not os.path.isfile(sysexecViewer):
			print "   *** ERROR:",sysexecViewer,"not found"
			print "   It seems that JPEGView is not installed in the system"
			sys.exit(0)


if not args.nobandmode:
	try:
		socketBT=LinkPolarBand(settings["device"],args.verbosemode)
	except NoBand:
		print "   *** ERROR: no bluetooth band was detected"
		sys.exit(0)
	except KeyboardInterrupt:
		print "   *** Program interrupted by user... exiting"
		sys.exit(0)

if settings["random"]:  # Shuffle data
	from random import shuffle

	if settings["mode"]=='videos':	
		indexes=range(len(videos))
		shuffle(indexes)
		videos_tmp = [videos[i] for i in indexes]
		tags_tmp=[tags[i] for i in indexes]
		videos=videos_tmp
		tags=tags_tmp

	if settings["mode"]=='images':	
		indexes=range(len(images))
		shuffle(indexes)
		images_tmp = [images[i] for i in indexes]
		tags_tmp=[tags[i] for i in indexes]
		images=images_tmp
		tags=tags_tmp
		for group in images:
			shuffle(group)


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

	if settings["mode"]=='videos':

		for n in range(len(videos)):
			video=videos[n]
			tag=tags[n]
			if args.verbosemode:
				print "   Video %s started" % tag

			if sysplat == "linux2":
				command = sysexecMPlayer + ' -really-quiet -fs %s  2> /dev/null' % video

			if sysplat == "win32":
				command = sysexecMPlayer + ' -really-quiet -fs %s' % video
			
			beg = (datetime.now()-zerotime).total_seconds()
			if  args.verbosemode:
				print "      Instant: %fs." % beg

			if sysplat == "linux2":
				os.system(command)

			if sysplat == "win32":
				os.system(command)

			end = (datetime.now()-zerotime).total_seconds()

			length=end-beg
			if args.verbosemode:
				print "   Video %s ended (length %f seconds)" % (tag,length)
				print "      Instant: %fs." % end

			datatags.append((tag,beg,end))
			time.sleep(settings["gap"])


	if settings["mode"]=="images":

		import subprocess
		for n in range(len(images)):
			tag = tags[n]

			if args.verbosemode:
				print "   Images with tag %s started" % tag
			beg = (datetime.now()-zerotime).total_seconds()
			if  args.verbosemode:
				print "      Instant: %fs." % beg

			if sysplat == "linux2":

				command = sysexecViewer+' -D %d --cycle-once -F --zoom max ' % settings["duration"]

				for imagefile in images[n]:
					command = command + imagefile+" "

			if sysplat == "win32":
				command = sysexecViewer+" "+imagesDirs[n]+' /slideshow %d /fullscreen /autoexit ' % settings["duration"]

				# if settings["random"]:
				# 	command = command + " /order Z"


	  		# print command

	  		os.system(command)

			end = (datetime.now()-zerotime).total_seconds()
			length=end-beg
			if args.verbosemode:
				print "   Images with tag %s ended (length %f seconds)" % (tag,length)
				print "      Instant: %fs." % end

			datatags.append((tag,beg,end))
		time.sleep(settings["gap"])


	errorinprogram, datarr=dataThread.EndAdquisition()
	if not args.nobandmode:
		dataThread.EndBTConnection()

except KeyboardInterrupt:
	print "   *** Program interrupted by user... exiting"
	if not args.nobandmode:
		dataThread.EndBTConnection()
	dataThread.join()
	sys.exit(0)

if errorinprogram:
	print "*** ERROR in program... not saving data"
else:
	SaveRRValues(datarr, fileHR, args.verbosemode)
	SaveTags(datatags, fileTags, args.verbosemode)

