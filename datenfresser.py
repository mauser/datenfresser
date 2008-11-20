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


from time import time
from time import sleep

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from db import database


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
	print container.type 
	if( container.type == "rsync" ):
		print "rsync!!"
		if container.options == "":
			print "no options given"
		
			
			
			checkDirs( container )
			rsync_cmd = "rsync -avz " + container.remotePath + " " + "/var/datenfresser/" + container.localPath + "/cur/"
			data.startJob(int(dataID))
			print rsync_cmd
			print "return: " + str(os.system( rsync_cmd ))
			data.backupPerformed( int(dataID), time() , "ok");
	

def main():
	
	d = database();
	#main loop
	while 1:
		sleep(2)
		for id in d.tickAction():
			performBackup(id)
		
	
if __name__ == "__main__":
	main()
	sys.exit(0)
