#!/usr/bin/python

import os
from os.path import isdir

class datenfresserCore:

	rootPath="/var/datenfresser/"

	def __init__(self):
		#check if rootPath ends with "/"
		if self.rootPath[-1]!="/": self.rootPath+="/"

		if not isdir(self.rootPath):
			os.mkdir(self.rootPath)


	def getContainers(self):
		for container in os.listdir(self.rootPath):
			print "rootContainer: container"
			c=rootContainer(container)
			for entry in os.listdir(self.rootPath + "/" + container):
				print entry + " exists in " + container



	def addRootContainer(self,cname):
		print self.rootPath + cname
		if not os.path.isdir(self.rootPath + cname):
			os.mkdir(self.rootPath + cname)
			print "created container %s" % cname
		else:
			print "Root Container %s exists already" % cname

	def delRootContainer(self,cname):
		pass

	def addDataContainer(self,rootContainer,cname):
		dname=self.rootPath +  rootContainer + "/" + cname
		if not os.path.isdir(dname):
			os.mkdir(dname)
			print "created dataContainer %s" % dname
		else:
			print "dataContainer %s exists already" % dname

	def delDataContainer(self,cname,rootContainer):
		pass






class rootContainer:
	#represents the outer container
	def __init__(self,name):
		print "i am a rootContainer called " + name
		self.comment=""

class dataContainer:
	#dataContainers containing archived data.
	# for example photos, documents , directories, music
	def __init__(self,name):
		print "i am a dataContainer called " + name
		self.contentType="normal"



if __name__ == "__main__":
	daten=datenfresserCore()
	daten.getContainers()
	daten.addRootContainer("mauser")
	daten.addDataContainer("mauser","my-data")
