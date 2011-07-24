import sys
import os

from subprocess import Popen
from subprocess import PIPE

from time import time
from time import sleep
from time import gmtime

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from core import *
from config import config
from config import CliArguments
from db import database
from db import monitorLog
from webserver import datenfresser_webserver
from monitor import datenfresserMonitorServer
from monitor import datenfresserMonitorClient
from helper import *
#
# checkDirs:  make sure that all needed directories are existing
#

def checkDirs( container ):
 
	c = config()
	MAINVOLUME = c.getMainVolume()

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


#
# archiveFolder: the method which does the real work. 
#                creates a backup of a container with the given method.
#

def archiveFolder( container , method , compress ):	
	
	c = config()
	MAINVOLUME = c.getMainVolume()


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




def performBackup( dataID ):
        log("trying to perform backup for dataID " + str( dataID) )
	c = config()
	MAINVOLUME = c.getMainVolume()

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
					notifyByMail("Job for dataID " + str(dataID) + " was succesful: " + str(output)) 
			else:
				#Oh, the backup was not successful. Maybe we should try again later?
				data.finishJob( int(dataID), int(id), "aborted", errorMessage, output, transferredSize )
				notifyByMail("Job for dataID " + str(dataID) + " was not succesful: " + str(error_message)) 
	syncMonitorData()



