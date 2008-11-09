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

def performBackup( dataID ):
	data = database()
	container = data.getDataContainer( dataID );
	if( container.type == "rsync" ):
		if container.options == "":
			print "no options given"
		
	
			

			if not os.path.isdir( container.localPath + "cur/" ):
				os.mkdir( container.localPath + "cur/")

			rsync_cmd = "rsync -avz " + container.remotePath + " " + container.localPath + "dir/"
			print rsync_cmd
			print os.system( rsync_cmd )
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
