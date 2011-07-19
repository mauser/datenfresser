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

from time import time
from time import sleep
from time import gmtime
from subprocess import Popen
from subprocess import PIPE


sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from config import CliArguments
from db import database
from db import monitorLog
from webserver import datenfresser_webserver
from monitor import datenfresserMonitorServer
from monitor import datenfresserMonitorClient
from core import *
from helper import *
from backupOperations import *

c = config()
MAINVOLUME = c.getMainVolume()



def sendMail( fromAdress, toAdress, body, user, password,  servername, port):
	c = config()
	server = smtplib.SMTP( servername )
	
	if c.getDebug():
		server.set_debuglevel(1)
	
	server.login( user , password );
	server.sendmail(fromAdress, toAdress, body)
	server.quit()



def notifyByMail( body ):

	c = config()
	if c.getNotifyByMailEnabled() == "False":
		return	

	from_addr = c.getSmtpUser() + "@" + c.getSmtpServer()
	to_addr = c.getMailRecipient()
	port = c.getSmtpPort()
	server = c.getSmtpServer()
	password = c.getSmtpPassword()

	sendMail( from_addr, to_addr, body , from_addr, password, server , port);


def setupUdevListener():
	
	if sys.platform != "linux2" and sys.platform != "linux3":
		log("Dbus is not supported on your platform.")
		return

	#code taken from http://stackoverflow.com/questions/5109879/usb-devices-udev-and-d-bus 

	import gobject
	from dbus.mainloop.glib import DBusGMainLoop

	def device_added_callback(device):
	    print 'Device %s was added' % (device)

	def device_changed_callback(device):
	    print 'Device %s was changed' % (device)

	#must be done before connecting to DBus
	DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	proxy = bus.get_object("org.freedesktop.UDisks", 
			       "/org/freedesktop/UDisks")
	iface = dbus.Interface(proxy, "org.freedesktop.UDisks")

	devices = iface.get_dbus_method('EnumerateDevices')()

	print '%s' % (devices)

	#addes two signal listeners
	iface.connect_to_signal('DeviceAdded', device_added_callback)
	iface.connect_to_signal('DeviceChanged', device_changed_callback)

	#start the main loop
	mainloop = gobject.MainLoop()
	mainloop.run()

	


				
				
def shutdown():
	cmd = "shutdown -h now"
	subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).wait()

def main( cliArguments ):

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
			
	
			checkSyncDirs()
			for id in d.tickAction():
				performBackup( id )
		
			#wait till we look for new ready-to-run jobs
			sleep( float( c.getPollInterval() ) )
		
			if int(auto_shutdown) > 0 and  (int(cur_time) + int (auto_shutdown)) - time() < 0:
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
