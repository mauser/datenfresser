import sys
import os
import cPickle

sys.path.append("/usr/lib/datenfresser/modules")

import config

class storage:

	def __init__(self):
		self.conf = config.config()

	def loadMetaData(self):
		# 1. get metaData for this containers
	
		if os.path.isfile(self.conf.persistentDataPath):
			try:
				FILE = open(self.conf.persistentDataPath, 'r')
				metaDataDict =  cPickle.load(FILE)
				FILE.close()	
			except Exception:
				metaDataDict = {}
				
		else:
			metaDataDict = {}
	
		return metaDataDict

	def saveMetaData(self,metaData):

		FILE = open(self.conf.persistentDataPath, 'w')
		cPickle.dump(metaData,FILE)
		FILE.close()
	
		return True

