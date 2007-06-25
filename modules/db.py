#!/usr/bin/env python
import sys

sys.path.append("/usr/lib/datenfresser/modules")

import sqlite

import os
import time


from string import strip
from core import dataContainer

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
		logrows=self.cursor.fetchall()
		

		sql="SELECT * FROM 'dataContainer'"		
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		for row in rows:
			if row[0] not in logrows:
				print "dataID:" +  str(row[0])

		actionList=[]			
		

		
		


		#2. get all entries where schedule="weekly" and timestamp - today > 604800 (7*24*60*60)
		today=time.time()
		
		sql="SELECT dataContainer.dataID FROM 'dataContainer','log' WHERE %s - log.timestamp > 604800 AND dataContainer.dataID = log.dataID"
		dataContainerTuple=self.cursor.fetchall()
		print dataContainerTuple
		







	def checkTables(self):
		'''check if all tables  exists, create it otherwise'''



		#table dataContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='dataContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'dataContainer' (dataID INTEGER PRIMARY KEY,  localPath TEXT, comment TEXT ,remotePath TEXT,type TEXT,schedule TEXT,groupID INTEGER)"
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

		#table groups 
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='groups'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'groups' (groupID INTEGER PRIMARY KEY, name TEXT)"
			self.cursor.execute(sql)
			sql="INSERT INTO groups VALUES (NULL,'*')"
			self.db.commit()





	def getDataContainer(self,name=""):

		if name=="":
			nameCondition=""
		else:
			nameCondition=" WHERE name='%s'" % name
			
		sql="SELECT * FROM dataContainer" + nameCondition
		self.cursor.execute(sql)
		dataContainerList = []
		for c in self.cursor.fetchall():
			tmp = dataContainer(c[1],c[2],c[3],c[4],c[5],c[6]);
			dataContainerList.append(tmp)
		return dataContainerList

						
					

 	def addDataContainer(self,name,comment,path,dirtype="none",schedule="weekly",group="s"):
		if schedule!="weekly" and schedule!="daily" and schedule!="monthly":
			schedule="weekly"


		sql="SELECT * FROM dataContainer WHERE localPath='%s'" % name
		self.cursor.execute(sql)
		if self.cursor.fetchone():
			print "dataContainer %s exists already" % name
			return -1
		
		
		gid=0;
		if group != "":
			sql="SELECT groupID FROM groups WHERE name='%s'" % group
			self.cursor.execute(sql)
			gid=self.cursor.fetchone()

			if gid != None:
				gid=gid[0][0]
			else:
				gid=0;

		sql="INSERT INTO dataContainer VALUES (NULL,'%(name)s','%(comment)s','%(path)s','%(type)s','%(schedule)s','%(group)s')"  %{ 'name': name, 'comment': comment, 'path': path, 'type': dirtype, 'schedule': schedule,'group':gid}
		self.cursor.execute(sql)
		self.db.commit()

		if not os.path.isdir(name):
			os.mkdir(name);

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
	db.addDataContainer("kazan-music.de","backup-data","blabla","kazan-music.de","/var/www/test","normal","weekly")
