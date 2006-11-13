#!/usr/bin/env python
import sqlite

from string import strip

class database:

	def __init__(self):

		self.db = sqlite.connect("meta.db")
		self.cursor = self.db.cursor()


	def install(self):
		'''check if our database is installed properly'''
		self.checkTables()




	def checkTables(self):
		'''check if all tables  exists, create it otherwise'''


		#table rootContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='rootContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'rootContainer' (rootID INTEGER PRIMARY KEY, name TEXT, comment TEXT)"
			self.cursor.execute(sql);
			self.db.commit()



		#table dataContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='dataContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'dataContainer' (dataID INTEGER PRIMARY KEY, rootID INTEGER, name TEXT, comment TEXT)"
			self.cursor.execute(sql);
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

		print self.cursor.execute("SELECT * FROM rootContainer;")
		rows = self.cursor.fetchall()
		print rows



 	def addDataContainer(self,rootContainer,name,comment,dirtype="none"):
		#get rootContainer ID
		sql="SELECT rootID FROM rootContainer WHERE name='%s'" % rootContainer
		self.cursor.execute(sql)
		rootID=self.cursor.fetchall()
		rootID=rootID[0][0]

		sql="INSERT INTO dataContainer VALUES (NULL,'%(rootID)s','%(name)s','%(comment)s','%(type)s" % { 'rootID': rootID, 'name': name, 'comment': comment, 'type': dirtype   }
		self.cursor.execute(sql)
		self.db.commit()

		#Check if theres no dataContainer named "name" in rootContainer



	def addComment(self,container,comment):
		pass

	def updateComment(self,container,comment):
		pass

	def removeComment(self,container,comment):
		pass

if __name__ == "__main__":
	db=database()
	db.install()
	db.addRootContainer("server","my tiny backup server")
	db.addDataContainer("server","backup-data","blabla")
