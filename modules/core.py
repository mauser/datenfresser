#!/usr/bin/python

import os

class datenfresserCore:
	
	rootPath="/var/datenfresser"
	
	def getContainers(self):
		for container in os.listdir(self.rootPath):
			print container
			c=rootContainer(container)
			for entry in os.listdir(self.rootPath + "/" + container):
				print entry + " exists in " + container
				
			
			
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
		