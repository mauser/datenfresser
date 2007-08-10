#!/usr/bin/python

#
# datenfresser is a backup software written by Sebastian Moors under GPL
# implemented features:
#  - daily/weekly rsync-backup 




#
# You can configure datenfresser with /etc/datenfresser.conf .
# Persistent metadata is stored with Pickle (default: /var/datenfresser/pickledData)
#



import os
import sys


from time import time
from time import sleep

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")


import config
from rsync import rsync
from core import metaData
from metaStorage import storage

conf=config.config()


def backup(container,metaDataDict):
	''' calls the underlying backup methods and updates meta data'''
	
	s = storage()
	
	print "performing backup for container " + container.name

	if not metaDataDict.has_key(container.name):
		m = metaData()
		metaDataDict[container.name] = m

	metaDataDict[container.name].lock = True

	#set lock
	s.saveMetaData(metaDataDict)
	
	if container.method=="rsync":
		rsync(container.localPath,container.remotePath,container.typeData.port,container.typeData.user)

	#Unset lock
	metaDataDict[container.name].lock = False
	s.saveMetaData(metaDataDict)	


	
def main():

	s=storage()

	container = conf.getDataContainer()
	metaDataDict = s.loadMetaData()

	#main loop
	while 1:
		sleep(20)
		for c in container:

			if c.schedule == "daily" and time() - c.lastBackup > 24*60*60:
				backup(c,metaDataDict)

			if c.schedule == "weekly" and time() - c.lastBackup > 7*24*60*60:
				backup(c,metaDataDict)
	
if __name__ == "__main__":
	main()
	sys.exit(0)
