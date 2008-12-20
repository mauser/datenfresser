#!/usr/bin/python

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

from time import time
from time import sleep
from time import gmtime

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from db import database


def archiveFolder( container , compress ):
	localPath = "/var/datenfresser/" + container.localPath	

	#be sure that the path ends with a "/"
	if localPath[-1] != "/": 
		localPath = localPath + "/"	


	dateTupel = gmtime(time())
	dateString = str(dateTupel[0]) + "_" + str(dateTupel[1]) + "_" + str(dateTupel[2]) + "_" + str(dateTupel[3]) + "_" + str(dateTupel[4]) 

	if compress == "on":
	    tar_cmd = "tar -jcf " + localPath + "archived/" + container.name + "_" + dateString + ".tar.bz2 " + localPath + "cur/*"
	else:
	    tar_cmd = "tar -cf " + localPath + "archived/" + container.name + "_" + dateString + ".tar " + localPath + "cur/*"

	print tar_cmd
	subprocess.Popen(tar_cmd,shell=True, stdout=subprocess.PIPE).wait()


def checkDirs( container ):
 	localPath = "/var/datenfresser/" + container.localPath	
	
	#be sure that the path ends with a "/"
	if localPath[-1] != "/": 
		localPath = localPath + "/"	

	if not os.path.isdir( localPath ):   os.mkdir( localPath)
	if not os.path.isdir( localPath + "cur/" ):   os.mkdir( localPath + "cur/")
	if not os.path.isdir( localPath + "archived/"):   os.mkdir( localPath + "archived/")

def performBackup( dataID ):
	data = database()
	container = data.getDataContainer( dataID );
	if( container.type == "rsync" ):
		if container.options == "":
		
			checkDirs( container )
			rsync_cmd = "rsync -avz " + container.remotePath + " " + "/var/datenfresser/" + container.localPath + "/cur/"
			
			
			id = 0
			id = data.startJob( "rsync" , int(dataID))

			print rsync_cmd
			print "return: " + str(os.system( rsync_cmd ))
			data.finishJob(int(dataID), int(id), "finished");
			
			archive,compress,ttl =  data.getArchiveInfo( int(dataID) )

			if archive != "disabled":
			    id = data.startJob( "archive" , int(dataID))
			    archiveFolder( container , compress )
			    data.finishJob( int(dataID),int(id), "finished");

def main():
	
	d = database()
	d.cleanupZombieJobs()
	#main loop
	while 1:
		sleep(2)
		for id in d.tickAction():
			print id
			performBackup(id)
		
	
if __name__ == "__main__":
	main()
	sys.exit(0)
