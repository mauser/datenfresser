#!/usr/bin/env python
import sqlite

import time
from string import strip

class database:

	def __init__(self):

		self.db = sqlite.connect("datenfresser.db")
		self.cursor = self.db.cursor()


	def install(self):
		'''check if our database is installed properly'''
		self.checkTables()

	def tickAction(self):
		#1. get all dataContainer without any log entry
		sql="SELECT dataID FROM 'log'"		
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		print rows

		sql="SELECT dataID FROM 'dataContainer'"		
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		for row in rows:
			print row[0]



		#2. get all entries where schedule="weekly" and timestamp - today > 604800 (7*24*60*60)
		today=time.time()
		
		sql="SELECT dataContainer.dataID FROM 'dataContainer','log' WHERE %s - log.timestamp > 604800 AND dataContainer.dataID = log.dataID"
		dataContainerTuple=self.cursor.fetchall()
		print dataContainerTuple
		







	def checkTables(self):
		'''check if all tables  exists, create it otherwise'''


		#table rootContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='rootContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'rootContainer' (rootID INTEGER PRIMARY KEY, name TEXT, comment TEXT)"
			self.cursor.execute(sql)
			self.db.commit()



		#table dataContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='dataContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'dataContainer' (dataID INTEGER PRIMARY KEY, rootID INTEGER, name TEXT, comment TEXT, origin TEXT,path TEXT,type TEXT,schedule TEXT)"
			self.cursor.execute(sql)
			self.db.commit()

		#table log
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='log'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'log' (logID INTEGER PRIMARY KEY, dataID INTEGER,timestamp TEXT, entry TEXT)"
			self.cursor.execute(sql)
			self.db.commit()



	def addRootContainer(self,name,comment):
		sql="SELECT * FROM 'rootContainer' WHERE name='%s'" % name
		self.cursor.execute(sql)
		row=self.cursor.fetchone()
		if row:
			print "rootContainer %s exists already" % name
			return -1

		sql="INSERT INTO rootContainer VALUES (NULL,'%(name)s','%(comment)s')" % {'name': name, 'comment': comment}
		self.cursor.execute(sql)
		self.db.commit()

		self.cursor.execute("SELECT * FROM rootContainer;")
		rows = self.cursor.fetchall()

	def getRootContainer(self):
		return	 


 	def addDataContainer(self,rootContainer,name,comment,path,dirtype="none",schedule="weekly"):
		#get rootContainer ID
		if schedule!="weekly" and schedule!="daily" and schedule!="monthly":
			schedule="weekly"

		sql="SELECT rootID FROM rootContainer WHERE name='%s'" % rootContainer
		self.cursor.execute(sql)
		rootID=self.cursor.fetchall()
		rootID=rootID[0][0]

		sql="SELECT * FROM dataContainer WHERE name='%s'" % name
		self.cursor.execute(sql)
		if self.cursor.fetchone():
			print "dataContainer %s exists already" % name
			return -1


		sql="INSERT INTO dataContainer VALUES (NULL,'%(rootID)s','%(name)s','%(comment)s','%(origin)s','%(path)s','%(type)s','%(schedule)s')" % { 'rootID': rootID, 'name': name, 'comment': comment,'origin': origin, 'path': path, 'type': dirtype, 'schedule': schedule}
		self.cursor.execute(sql)
		self.db.commit()

		#Check if theres no dataContainer named "name" in rootContainer
		return 0
		

	def addComment(self,container,comment):
		pass

	def updateComment(self,container,comment):
		pass

	def removeComment(self,container,comment):
		pass

if __name__ == "__main__":
	db=database()
	db.install()
	db.addRootContainer("kazan-music.de","my tiny backup server")
	db.addDataContainer("kazan-music.de","backup-data","blabla","kazan-music.de","/var/www/test","normal","weekly")
