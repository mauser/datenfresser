#!/usr/bin/python

# TODO: Installer 1. copy daemon to /usr/sbin
#                 2. init.d scripts
#		  3. rc.d links
#                 4. create /etc/datenfresser.db
#		  5. create rootContainer (if wanted)
#		  6. start daemon	

import os
import sys

import cPickle

from time import time
from time import sleep

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")


import config
from rsync import rsync
from core import metaData
conf=config.config()

	


def loadMetaData():
	# 1. get metaData for this containers
	
	if os.path.isfile(conf.persistentDataPath):
		try:
			FILE = open(conf.persistentDataPath, 'r')
			metaDataDict =  cPickle.load(FILE)
			FILE.close()	
		except Exception:
			metaDataDict = {}
			
	else:
		metaDataDict = {}
	
	return metaDataDict

def saveMetaData(metaData):

	FILE = open(conf.persistentDataPath, 'w')
	cPickle.dump(metaData,FILE)
	FILE.close()
	
	return True



def backup(container,metaDataDict):
	''' calls the underlying backup methods and updates meta data'''
	
	print "performing backup for container " + container.name

	if not metaDataDict.has_key(container.name):
		m = metaData()
		metaDataDict[container.name] = m

	metaDataDict[container.name].lock = True

	#set lock
	saveMetaData(metaDataDict)
	
	if container.method=="rsync":
		rsync(container.localPath,container.remotePath,container.typeData.port,container.typeData.user)

	#Unset lock
	metaDataDict[container.name].lock = False
	


	
def main():

	container = conf.getDataContainer()
	metaDataDict = loadMetaData()

	#main loop
	while 1:
		sleep(1)
		for c in container:

			if c.schedule == "daily" and time() - c.lastBackup > 24*60*60:
				backup(c,metaDataDict)

			if c.schedule == "weekly" and time() - c.lastBackup > 7*24*60*60:
				backup(c,metaDataDict)
	
if __name__ == "__main__":
	main()
	sys.exit(0)
