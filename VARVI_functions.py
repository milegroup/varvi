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

import threading
from datetime import datetime,timedelta
import sys
import time

class NoBand(Exception):pass

def LinkPolarBand(btDevice,verbose):
	"""Function to link the polar band"""
	try:
		import bluetooth
	except ImportError:
		print "   *** ERROR: bluetooth library not installed in the system"
		sys.exit(0)

	if verbose:
		print "   Looking for bluetooth devices..."
	devs = bluetooth.discover_devices(lookup_names=True)
	if verbose:
		print "   Number of bluetooth devices found: %d" % len(devs)
	dev = [s for s in devs if s[0]==btDevice]
	if len(dev)==0:
		raise NoBand
	if verbose:
		print "   Trying to conect with device:",dev[0][1]
	socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	socket.connect((dev[0][0],1))
	return socket
	
def GetSettings(filename,verbose):
	import ConfigParser
	options=ConfigParser.SafeConfigParser()
	options.read(filename)

	settings={}
	media=[]
	tags=[]

	if "Main" not in options.sections():
		print "   *** ERROR: [Main] section missing in file %s" % filename
		sys.exit(0)

	MainParams = [x for (x,y) in options.items("Main")]

	if "mode" not in MainParams:
		print "   *** ERROR: 'mode' option missing in file %s" % filename
		sys.exit(0)
	mode = [elem[1] for elem in options.items("Main") if elem[0]=="mode"]

	if mode != ['images'] and mode != ['videos']:
		print "   *** ERROR: legal values for 'mode' option are images|videos"
		sys.exit(0)

	settings["mode"]=mode[0]


	if "random" not in MainParams:
		print "   *** ERROR: 'random' option missing in section [Main]"
		sys.exit(0)

	random = [elem[1] for elem in options.items("Main") if elem[0]=="random"]
	if random == ['0']:
		settings["random"]=False
	elif random ==['1']:
		settings["random"]=True
	else:
		print "   *** ERROR: 'random' option with illegal value in [Main]"
		sys.exit(0)

	if "device" not in MainParams:
		print "   *** ERROR: 'device' option missing in section [Main]"
		sys.exit(0)

	device = [elem[1] for elem in options.items("Main") if elem[0]=="device"]
	settings["device"]=device[0]


	if "gap" in MainParams:
		gap = [elem[1] for elem in options.items("Main") if elem[0]=="gap"]
		try:
			settings["gap"]=float(gap[0])
		except ValueError:
			print "*** ERROR: 'gap' option with illegal value in [Main]"
			sys.exit(0)

	if "duration" in MainParams:
		duration = [elem[1] for elem in options.items("Main") if elem[0]=="duration"]
		try:
			settings["duration"]=float(duration[0])
		except ValueError:
			print "*** ERROR: 'duration' option with illegal value in [Main]"
			sys.exit(0)



	if "nmedia" not in MainParams:
		print "   *** ERROR: 'nmedia' parameter missing in section [Main]"
		sys.exit(0)

	nmedia = [elem[1] for elem in options.items("Main") if elem[0]=="nmedia"]
	try:
		settings["nmedia"]=int(nmedia[0])
	except ValueError:
		print "   *** ERROR: 'nmedia' option with illegal value in [Main]"
		sys.exit(0)


	for n in range(settings["nmedia"]):
		section = 'Media_%02d' % (n+1)
		if section not in options.sections():
			print "   *** ERROR: [%s] section missing in file %s" % (section,filename)
			sys.exit(0)
		SecParams = [x for (x,y) in options.items(section)]
		if "tag" not in SecParams:
			print "   *** ERROR: 'tag' parameter missing in section [%s]" % section
			sys.exit(0)
		if "source" not in SecParams:
			print "   *** ERROR: 'source' parameter missing in section [%s]" % section
			sys.exit(0)

		tag = [elem[1] for elem in options.items(section) if elem[0]=="tag"]
		source = [elem[1] for elem in options.items(section) if elem[0]=="source"]
		tags.append(tag[0])
		media.append(source[0])

	return settings,media,tags


def SaveRRValues(dataRR,fileRR,verbose):
	try:
		# This will create a new file or **overwrite an existing file**.
		f = open(fileRR, "w")
		for time,rr in dataRR:
			f.write(str(rr)+"\n")
		f.close()
	except:
		print "   *** ERROR: problem saving file "+fileRR+" ***"
		sys.exit(0)

	if verbose:
		print "   Saved file %s (%d rr values)" % (fileRR,len(dataRR))
	
		
def SaveTags(dataTags, fileTags, verbose):
	# try:
	if True:
		f = open(fileTags, "w")
		f.write("Init_time\tEvent\tDurat\n")
		for tag,beg,end in dataTags:
			cad = "%s\t%s\t%.3f\n" % (str(timedelta(seconds=beg)),tag,end-beg)
			# f.write(str(beg)+"\t"+tag+"\t"+str(end-beg)+"\n")
			f.write(cad)
		f.close()
	# except:
	# 	print "   *** ERROR: problem saving file "+fileTags+" ***"
	# 	sys.exit(0)

	if verbose:
		print "   Saved file %s (%d episodes)" % (fileTags,len(dataTags))



class DataAdquisition(threading.Thread):


	def __init__(self,socketBT,verbose):
		self.MinRR = 550
		self.verbose=verbose
		self.veryverbose = False
		threading.Thread.__init__(self)
		self.socketBT = socketBT
		self.End = False
		self.Ended=False
		self.ErrorInProgram = False
		self.CorrectData = False
		self.StoreData = False
		self.ObtainedData=[]

	def run(self):
		# print "I'm the thread that gets the data from the band"
		import socket as socketLib



		while (True):
		# try:
			try:
				data1 = self.socketBT.recv(1, socketLib.MSG_WAITALL).encode('hex')
				# while data != 'fe':
				# 	data = self.socketBT.recv(1).encode('hex')
				# print "Package header: ",int(data,16)
				data2 = self.socketBT.recv(1, socketLib.MSG_WAITALL).encode('hex')
				ll = int(data2,16)
				# print "Package length:", ll, "bytes"

				data3 = self.socketBT.recv(ll-2, socketLib.MSG_WAITALL).encode('hex')
				chk = int(data3[0:2],16)
				if chk+ll != 255:
					print "*** ERROR: Package not Ok ***"

				seq = int(data3[2:4],16)
				if self.veryverbose:
					print "Package seq:",seq

				status = int(data3[4:6],16)
				if self.veryverbose:
					print "Package status:",status

				hr = int(data3[6:8],16)
				if self.veryverbose:
					print "Heart rate:",hr,"bpm"

				nextbit  = 8

				if self.veryverbose:
					print "Package contains",(ll-6)/2,"beats"

				for i in range((ll-6)/2):  # No. de valores RR por paquete
					rr1 = int(data3[nextbit:nextbit+2],16)
					rr2 = int(data3[nextbit+2:nextbit+4],16)
					rr=(rr1<<8)|rr2
					if self.veryverbose:
						print "    RR:", rr, "mseg."

					if rr>self.MinRR and not self.CorrectData:
						self.CorrectData=True

					if self.StoreData:
						self.ObtainedData.append( ((datetime.now()-self.zerotime).total_seconds(),rr) )

					nextbit = nextbit+4

			except ValueError as e:
				if not self.End:  # Exception only works if BT is still connected
					print "*** Exception ValueError raised: data not Ok ***"
					import traceback, os.path
					top = traceback.extract_stack()[-1]
					print "Program:",os.path.basename(top[0]), " -  Line:", str(top[1])
					print "Data:"
					print data1
					print data2
					print data3
					self.ErrorInProgram = True
				else:
					print "*** Warning: ValueError raised at the end of the adquisition"


			except Exception as e:
				import traceback, os.path
				top = traceback.extract_stack()[-1]
				print "*** Exception:",type(e).__name__," -  Program:",os.path.basename(top[0]), " -  Line:", str(top[1]),"***"
				self.ErrorInProgram = True

			if self.End == True:
				self.Ended = True
				break



	def EndAdquisition(self):
		self.End = True
		if self.verbose:
			print "   End adquisition instant: %fs." % (datetime.now()-self.zerotime).total_seconds()
		return self.ErrorInProgram, self.ObtainedData
		

	def BeginAdquisition(self,zerotime):
		self.StoreData = True
		self.zerotime = zerotime
		if self.verbose:
			print "   Begin adquisition instant: %fs" % (datetime.now()-self.zerotime).total_seconds()

	def DataIsCorrect(self):
		return self.CorrectData

	def EndBTConnection(self):
		self.End=True
		while not self.Ended:
			time.sleep(0.1)
		self.socketBT.close()


# ------------------------------

class DataSimulation(threading.Thread):
	from random import uniform
	def __init__(self,verbose):
		self.verbose=verbose
		self.veryverbose = False
		threading.Thread.__init__(self)
		self.End = False
		self.Ended=False
		self.CorrectData = False
		self.StoreData = False
		self.ObtainedData=[]

	def run(self):
		from random import uniform
		# print "I'm the thread that gets the data from the band"

		while (True):
		# try:
			waitvalue = uniform(800,900)

			time.sleep(waitvalue/1000.0)

			rr = waitvalue

			# print "RR interval: ",waitvalue

			
			if self.veryverbose:
				print "    RR:", rr, "mseg."

			self.CorrectData=True

			if self.StoreData:
				self.ObtainedData.append( ((datetime.now()-self.zerotime).total_seconds(),rr) )

				
			if self.End == True:
				self.Ended = True
				break

	def EndAdquisition(self):
		self.End = True
		if self.verbose:
			print "   End adquisition instant: %fs." % (datetime.now()-self.zerotime).total_seconds()
		return False, self.ObtainedData
		

	def BeginAdquisition(self,zerotime):
		self.StoreData = True
		self.zerotime = zerotime
		if self.verbose:
			print "   Begin adquisition instant: %fs" % (datetime.now()-self.zerotime).total_seconds()

	def DataIsCorrect(self):
		return self.CorrectData



# ------------------------------