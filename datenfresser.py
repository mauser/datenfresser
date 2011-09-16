#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################
# datenfresser is a backup daemon written by Sebastian Moors		   #	
# It is licensed under the GPL v2.  					   #
############################################################################


# You can configure datenfresser with /etc/datenfresser.conf .            

# directory structure:
# $backupdir/container/          : represents a backup entity
# $backupdir/container/cur       : holds current data
# $backupdir/container/archived  : contains compressed or somehow archived versioned of "cur"


import os
import sys
import subprocess
import select
import getopt
import traceback
import smtplib
import signal

from threading import Lock

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from config import CliArguments
from db import database
from db import monitorLog
from webserver import datenfresser_webserver
from core import *
from helper import *
from backupOperations import *
from monitor import datenfresserMonitorServer
from monitor import datenfresserMonitorClient


udevNotificationLock = Lock()
udevNotificationList = [] 


def pushUdevNotification( notification ):
	print "enter push"
	#udevNotificationLock.acquire()
	udevNotificationList.append( notification )
	#udevNotificationLock.release()
	print "leave push"

def getNextUdevNotification():
	print "calling getNextUdev"
	element = []
	#udevNotificationLock.acquire()
	if len(udevNotificationList) > 0:
		element = udevNotificationList.pop( )
	#udevNotificationLock.release()
	print "after get"
	return [element]





class UdevListener():
	
	def run(self):

		main_pid = os.getpid()

		pid = os.fork()
		if pid > 0:
			return
		else:
			print "dbus process has pid: " + str(os.getpid())	
			#code taken from http://stackoverflow.com/questions/5109879/usb-devices-udev-and-d-bus 
			import dbus
			import gobject
			from dbus.mainloop.glib import DBusGMainLoop


			#ignore our own signal
			signal.signal(signal.SIGUSR1, signal.SIG_IGN)

			def device_added_callback(device):
			    print 'Device %s was added' % (device)
			    print "sending to %s " % main_pid
			    #os.kill( main_pid , signal.SIGUSR1 ) 
			    #pushUdevNotification(device)
			
			    bus = dbus.SystemBus()
			    ud_manager_obj = bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
			    ud_manager = dbus.Interface(ud_manager_obj, 'org.freedesktop.UDisks')

			    for dev in ud_manager.EnumerateDevices():
				
				device_obj = bus.get_object("org.freedesktop.UDisks", dev)
				device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
				
				interface = device_props.Get('org.freedesktop.UDisks.Device', "DriveConnectionInterface")
				if interface == "usb" or interface == "firewire":
					print "usb found"
					device_file = device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile")
					device_file = device_file[device_file.rfind("/")+1:]
					device = device[device.rfind("/")+1:]
					if device == device_file:
						
						#let the udev mount it..
						sleep(1)
						print device_props.Get('org.freedesktop.UDisks.Device', "DeviceMountPaths")


			def device_changed_callback(device):
				pass
				
			#must be done before connecting to DBus
			DBusGMainLoop(set_as_default=True)

			bus = dbus.SystemBus()

			proxy = bus.get_object("org.freedesktop.UDisks", 
					       "/org/freedesktop/UDisks")
			iface = dbus.Interface(proxy, "org.freedesktop.UDisks")

			devices = iface.get_dbus_method('EnumerateDevices')()
			
			


			#print '%s' % (devices)

			#addes two signal listeners
			iface.connect_to_signal('DeviceAdded', device_added_callback)
			iface.connect_to_signal('DeviceChanged', device_changed_callback)

			#start the main loop
			mainloop = gobject.MainLoop()
			mainloop.run()
			
		
def handler(signum, frame):
    	print 'Signal handler called with signal', signum
	print os.getpid()



				
				
def shutdown():
	cmd = "shutdown -h now"
	subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).wait()

def main( cliArguments ):
	# Set the signal handler and a 5-second alarm
	signal.signal(signal.SIGUSR1, handler)
	
	log("Starting datenfresser server")

	if cliArguments.daemon == True:
		createDaemon()	

	c = config()
	
	webserver = c.getWebserverEnabled()
	webserver_port =  c.getWebserverPort()
	
	monitor = c.getMonitorServerEnabled()
	if cliArguments.monitor: monitor = "True"


	auto_shutdown = c.getAutomaticShutdown()
	start_delay = c.getStartDelay()
	debug = c.getDebug()	

	udev = UdevListener()
	udev.run()

	# if automatic shutdown is enabled, we ask the user to hit the "enter" key to 
	# disable automatic shutdown at startup

	if int(auto_shutdown) > 0:
		print "Press 'enter' to disable automatic shutdown"
		rfds, wfds, efds = select.select( [sys.stdin], [], [], 5)
		if rfds != []:
			auto_shutdown = 0



	if webserver == "True":
	    log("Starting builtin webserver on port " + str(webserver_port))
	    #start our own webserver to serve the webinterface
	    web = datenfresser_webserver( webserver_port )
	    web.startServer()
	
	d = database()
	d.cleanupZombieJobs()

	
	#current time
	cur_time = time()

	if int(start_delay) > 0:
		sleep( float ( start_delay ) )

	syncMonitorData()

	print os.getpid()

	if monitor == "True" or monitor == "true":
	    #start our own monitor 
	    log("Trying to start monitor service..")
	    monitorServer = datenfresserMonitorServer ()
	    monitorServer.startServer()
    	else:
		log("Not starting monitor")
		pidFileName = "/var/lib/datenfresser/datenfresser.pid"
		if os.path.isfile( pidFileName ):	
			pidFile = open( pidFileName )
			tmp = pidFile.readline() 
			if len(tmp) == 0:
				pid = int( pidFile.readline() )
				try:
					os.getpgid( pid )
					log("Another instance of datenfresser is already running. Quitting now..")
					sys.exit( 0 )
				except OSError, e:
					pass
		
		pidFile = open( pidFileName , "w" )
		pidFile.write( str( os.getpid() ) ) 
		pidFile.close()
	

		while 1:
			print getNextUdevNotification()	
			#checkSyncDirs()
			for id in d.tickAction():
				performBackup( id )
		
			print "before sleep"
			#wait till we look for new ready-to-run jobs
			#sleep( float( c.getPollInterval() ) )
			sleep( 5 )
			print "after sleep"

			if int(auto_shutdown) > 0 and  (int(cur_time) + int (auto_shutdown)) - time() < 0:
				print "shutdown"
				shutdown()
		
	
if __name__ == "__main__":


	cliArguments = CliArguments()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hmvd", ["help", "monitor", "verbose","daemon"])
	except getopt.GetoptError, err:
		print str(err) 
		#usage()
		sys.exit(2)

	for o, a in opts:
		if o == "-d":
		    cliArguments.daemon = True
		if o == "-v":
		    cliArguments.verbose = True
		if o == "-m":
		    cliArguments.monitor = True
		elif o in ("-h", "--help"):
		    #usage()
		    sys.exit()

	main( cliArguments )
	sys.exit(0)
