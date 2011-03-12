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

c = config()
MAINVOLUME = c.getMainVolume()


def executeCommand( command ):
	#excute command 
	#return returnValue: 0 if everything went ok, 1 in case that something went wrong..
		
	p = Popen( command.split(" "), bufsize=4024 ,stderr=PIPE,stdout=PIPE,close_fds=True)	
	(child_stderr) = ( p.stderr)
	(child_stdout) = ( p.stdout)

	output = child_stdout.readlines()
	errorMessage =  child_stderr.readlines()
	x = p.wait()
	errorMessage =  errorMessage + child_stderr.readlines()
	output = output + child_stdout.readlines()
	
	#convert "wait"-style exitcode to normal, shell-like exitcode
	exitcode = (x >> 8) & 0xFF
	return exitcode , errorMessage , output




def archiveFolder( container , method , compress ):
	localPath = MAINVOLUME + "/" + container.localPath	

	log("archive folder " + localPath + " with " + method )

	#be sure that the path ends with a "/"
	if localPath[-1] != "/": 
		localPath = localPath + "/"	

	
	dateTupel = gmtime(time())
	dateString = str(dateTupel[0]) + "_" + str(dateTupel[1]) + "_" + str(dateTupel[2]) + "_" + str(dateTupel[3]) + "_" + str(dateTupel[4]) 

	if method == "tar":
	    if compress == "on":
		tar_cmd = "tar -jcf " + localPath + "archived/" + container.name + "_" + dateString + ".tar.bz2 " + localPath + "cur/*"
	    else:
		tar_cmd = "tar -cf " + localPath + "archived/" + container.name + "_" + dateString + ".tar " + localPath + "cur/*"

	    log( tar_cmd , "verbose" )
	    subprocess.Popen(tar_cmd,shell=True, stdout=subprocess.PIPE).wait()
	
	if method == "hardlinks":
		# see http://www.mikerubel.org/computers/rsync_snapshots/

		if sys.platform == "darwin":
			#"gcp" comes with the coreutils package from macports..
			cp_command = "gcp"
		else:
			cp_command = "cp"
 
		cmd = cp_command + " -al "   + localPath + "cur/" + " " + localPath + "snapshots/" + container.name + "_" + dateString
		log( cmd , "verbose" )
		subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).wait()    
	 
	if method == "btrfs snapshot":
	    cmd = "btrfsctl -s " + localPath + "snapshots/" + container.name + "_" + dateString + " " + localPath + "cur/"
	    log( cmd , "verbose" )
	    subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).wait() 
	






def getDirectorySize(directory):
    #taken from http://roopindersingh.com/2008/04/22/calculating-directory-sizes-in-python/
    # returns the size of a directory ( in kilobytes a 1024 bits )
    class TotalSize:
        def __init__(self):
            self.total = 0

    def visit(totalSize, dirname, names):
        for name in names:
            absFilename = os.path.join(dirname, name)
            if os.path.isfile(absFilename):
                totalSize.total += os.path.getsize(absFilename)

    totalSize = TotalSize()
    os.path.walk(directory, visit, totalSize)
    return totalSize.total / 1024	   





def checkDirs( container ):
 	localPath = MAINVOLUME + "/" + container.localPath	
	
	#be sure that the path ends with a "/"
	if localPath[-1] != "/": 
		localPath = localPath + "/"	

	
	if not os.path.isdir( localPath ):   os.mkdir( localPath )
	
	#stores current data ( retrieved with rsync )
	if not os.path.isdir( localPath + "cur/" ):   os.mkdir( localPath + "cur/" )
	
	#holds archives 
	if not os.path.isdir( localPath + "archived/"):   os.mkdir( localPath + "archived/" )
	
	#holds btrfs snapshots
	if not os.path.isdir( localPath + "snapshots/"):   os.mkdir( localPath + "snapshots/" )

def syncMonitorData():
	c = config()
	if c.getMonitorClientEnabled() == "False":
		return	
	#push changes to the monitoring server
	log( "trying monitorSync " + str(c.getMonitorClientEnabled()))
	try:
		monitorClient = datenfresserMonitorClient()
		monitorClient.sync()
	except Exception, e:
		traceback.print_exc(file=sys.stdout)
		log( str( sys.exc_info()[0] ) )
		log("Exception during monitor sync: " + str(e) )




def performBackup( dataID ):
        log("trying to perform backup for dataID " + str( dataID) )
	c = config()
	debug = c.getDebug()	
	data = database()
	container = data.getDataContainer( dataID )[0]

	if( container.type == "rsync" ):
		if container.options == "" or container.options == None:
			checkDirs( container )	
			rsync_cmd = "rsync -avz " + container.remotePath + " " + MAINVOLUME + "/" + container.localPath + "/cur/"
			returnValue = 0
			id  = 0
			#get directory size before backup
			start_size = getDirectorySize(  MAINVOLUME + "/" + container.localPath + "/cur/" )
			log( rsync_cmd )
			id = data.startJob( "rsync" , int(dataID))
			
			returnValue, errorMessage, output = executeCommand( rsync_cmd )
			

			#if len(errorMessage) == 0:
			#	errorMessage = output

			log( "backup command returned: " + str(returnValue ))

			#get directory size after backup
			final_size = getDirectorySize(  MAINVOLUME + "/" + container.localPath + "/cur/" )
			transferredSize = final_size - start_size
			
			log( "transferred " + str(transferredSize) + "kb")

			
			if int(returnValue) == 0:
				data.finishJob(int(dataID), int(id), "finished", errorMessage, output, transferredSize)
				
				#start to archive the backup, if necessary
				archive , method , compress,ttl =  data.getArchiveInfo( int(dataID) )
				if archive != "disabled":
					id = data.startJob( "archive" , int(dataID))
					archiveFolder( container , method , compress )
					data.finishJob( int(dataID),int(id), "finished","","", 0)
			else:
				#Oh, the backup was not successful. Maybe we should try again later?
				data.finishJob( int(dataID), int(id), "aborted", errorMessage, output, transferredSize )
	syncMonitorData()









				
				
def checkSyncDirs():
	c = config()
	d = database()
	container = d.getDataContainer("")	
	
	dir = c.getSyncDir()
	if dir != "" and dir[-1] == "/": dir = dir[:-1]	

	if dir != "" and os.path.isdir( dir ): 
		for con in container:
			if os.path.isdir( dir + "/" + con.name ) and con.name != "" and con.name !="." and os.listdir(dir + "/" + con.name) != [] :
				dest_path = MAINVOLUME + "/" + con.name + "/cur/"
				os.system("mv " + dir + "/" + con.name + "/* " +  dest_path )

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
	    #start our own monitor to serve the webinterface
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
