#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# datenfresser is a backup software written by Sebastian Moors under GPL
# implemented features:
#  - daily/weekly rsync-backup 




#
# You can configure datenfresser with /etc/datenfresser.conf .
# Persistent metadata is stored with Pickle (default: /var/datenfresser/pickledData)
#

#Todo: backup archiving (when? (weekly, daily,startup),how long archived?)

# directory structure:
# $backupdir/container/          : represents a backup entity
# $backupdir/container/cur       : current data
# $backupdir/container/archived  : contains compressed versioned of "cur"


import os
import sys
import subprocess
import select

from time import time
from time import sleep
from time import gmtime

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from db import database
from webserver import datenfresser_webserver

c = config()
MAINVOLUME = c.getMainVolume()

def archiveFolder( container , method , compress ):
	localPath = MAINVOLUME + "/" + container.localPath	

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

	    print tar_cmd
	    subprocess.Popen(tar_cmd,shell=True, stdout=subprocess.PIPE).wait()
	
	if method == "btrfs snapshot":
	    cmd = "btrfsctl -s " + localPath + "snapshots/" + container.name + "_" + dateString + " " + localPath + "cur/"

	    print cmd
	    subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).wait()	    
	 
	   


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

def performBackup( dataID ):
	data = database()
	container = data.getDataContainer( dataID )[0]
	if( container.type == "rsync" ):
		if container.options == "":
		
			checkDirs( container )
			rsync_cmd = "rsync -avz " + container.remotePath + " " + MAINVOLUME + "/" + container.localPath + "/cur/"
			
			
			id = 0
			id = data.startJob( "rsync" , int(dataID))

			print rsync_cmd
			print "return: " + str(os.system( rsync_cmd ))
			data.finishJob(int(dataID), int(id), "finished");
			
			archive , method , compress,ttl =  data.getArchiveInfo( int(dataID) )

			if archive != "disabled":
			    id = data.startJob( "archive" , int(dataID))
			    archiveFolder( container , method , compress )
			    data.finishJob( int(dataID),int(id), "finished");
def checkSyncDirs():
	c = config()
	d = database()
	container = d.getDataContainer("")	
	
	dir = c.getSyncDir()
	if dir[-1] == "/": dir = dir[:-1]	

	if dir != "" and os.path.isdir( dir ): 
		for con in container:
			if os.path.isdir( dir + "/" + con.name ) and con.name != "" and con.name !="." and os.listdir(dir + "/" + con.name) != [] :
				dest_path = MAINVOLUME + "/" + con.name + "/cur/"
				os.system("mv " + dir + "/" + con.name + "/* " +  dest_path )

def shutdown():
	cmd = "shutdown -h now"
	subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).wait()

def main():
	c = config()
	webserver = c.getWebserverEnabled()
	webserver_port =  c.getWebserverPort()
	auto_shutdown = c.getAutomaticShutdown()
	
	# if automatic shutdown is enabled, we ask the user to hit the "enter" key to 
	# disable automatic shutdown at startup

	if int(auto_shutdown) > 0:
		print "Press 'enter' to disable automatic shutdown"
		rfds, wfds, efds = select.select( [sys.stdin], [], [], 5)
		if rfds != []:
			auto_shutdown == 0


	try: 
		pid = os.fork() 
		if pid > 0:
		    return
	except OSError, e: 
		print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
		sys.exit(1) 


	if webserver == "True":
	    #start our own webserver to serve the webinterface
	    web = datenfresser_webserver( webserver_port )
	    web.startServer()
	
	d = database()
	d.cleanupZombieJobs()

	#current time
	cur_time = time()

	#main loop
	while 1:
		checkSyncDirs()
		for id in d.tickAction():
			performBackup( id )
		
		#wait till we look for new ready-to-run jobs
		sleep( float( c.getPollInterval() ) )
		
		if (int(cur_time) + int (auto_shutdown)) - time() < 0:
			#shutdown()
			print "shutdown!!!"
		
	
if __name__ == "__main__":
	main()
	sys.exit(0)
