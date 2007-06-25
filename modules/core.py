#!/usr/bin/python

import os
from os.path import isdir


class dataContainer:
	#dataContainers containing archived data.
	# for example photos, documents , directories, music
	def __init__(self,localPath,comment,remotePath,type,schedule,group):
		print "i am a dataContainer called " + localPath
		self.localPath=localPath
		self.comment=comment
		self.remotePath=remotePath
		self.type=type
		self.schedule=schedule
		self.group=group

