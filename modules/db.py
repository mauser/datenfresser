#!/usr/bin/env python
import sys

sys.path.append("/usr/lib/datenfresser/modules")

import sqlite3

import os
import time


from string import strip
from core import dataContainer

class database:

	def __init__(self):

		self.db = sqlite3.connect("/var/datenfresser/datenfresser.db")
		self.cursor = self.db.cursor()


	def install(self):
		'''check if our database is installed properly'''
		self.checkTables()

	def tickAction(self):
		#1. get all dataContainer without any log entry
		sql="SELECT dataID FROM 'log'"		
		self.cursor.execute(sql)
		logrows = self.cursor.fetchall()

		sql = "SELECT * FROM 'dataContainer'"		
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()

		actionList=[]			
		
		for row in rows:
			if row[0] not in logrows:
				print "dataID:" +  str(row[0])
				actionList.append(str(row[0]));	

		

		
		


		#2. get all entries where schedule="weekly" and timestamp - today > 604800 (7*24*60*60)
		today=time.time()
		
		sql="SELECT dataContainer.dataID FROM 'dataContainer','log' WHERE %s - log.timestamp > 604800 AND dataContainer.dataID = log.dataID"
		dataContainerTuple=self.cursor.fetchall()
		#print dataContainerTuple
		return actionList;	




	def checkTables(self):
		'''check if all tables  exists, create it otherwise'''



		#table dataContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='dataContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'dataContainer' (dataID INTEGER PRIMARY KEY, name Text, comment Text, localPath TEXT, remotePath TEXT,type TEXT, options TEXT, schedule TEXT,groupID INTEGER)"
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





	def getDataContainer(self,dataId):

		if dataId=="":
			nameCondition=""
		else:
			nameCondition=" WHERE dataId='%s'" % dataId
			
		sql="SELECT * FROM dataContainer" + nameCondition
		self.cursor.execute(sql)
		dataContainerList = []
		for c in self.cursor.fetchall():
			tmp = dataContainer(c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8]);
			return tmp

						
					

 	def addDataContainer(self,name,comment,path,type="rsync",options="",schedule="weekly",group="ALL"):
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

		localPath = "/var/datenfresser/" + name;

		sql="INSERT INTO dataContainer VALUES (NULL,'%(name)s','%(localPath)s', '%(remotePath)s','%(comment)s','%(type)s','%(options)s','%(schedule)s','%(group)s')"  %{ 'name': name, 'comment': comment, 'localPath': localPath, 'remotePath': path, "type": type, 'options':options,'schedule': schedule,'group':gid}
		print sql
		self.cursor.execute(sql)
		self.db.commit()

		if not os.path.isdir(name):
			os.mkdir(name);

		#Check if theres no dataContainer named "name" in rootContainer
		return
		

	def addComment(self,container,comment):
		pass

	def updateComment(self,container,comment):
		pass

	def removeComment(self,container,comment):
		pass

if __name__ == "__main__":
	db=database()
	db.install()
	db.addDataContainer("kazan","kommentar","smoors.de:/var/www/trac_projects")
