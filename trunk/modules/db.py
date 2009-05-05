#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append("/usr/lib/datenfresser/modules")

import sqlite3

import os
import time


from string import strip
from core import *
from config import config

c = config()
MAINVOLUME = c.getMainVolume()

class database:

	def __init__(self):
		if not os.path.isdir( MAINVOLUME ):
			os.mkdir( MAINVOLUME )

		self.db = sqlite3.connect( MAINVOLUME + "/datenfresser.db" )
		self.cursor = self.db.cursor()
		self.checkTables()


	def install(self):
		'''check if our database is installed properly'''
		self.checkTables()

	def tickAction(self):
		#holds dataID's of the container which are scheduled for backup now
		actionList=[]	
	    
		#1. get all dataContainer without any log entry
		sql="SELECT dataID FROM dataContainer WHERE dataID NOT IN ( SELECT dataID from log WHERE NOT status = 'unfinished')"	
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		for row in rows:
			actionList.append( str(row[0]) );
		print actionList


		#get logID of last backup
		#sql = "SELECT log.logID FROM log WHERE dataID = " + dataID + " ORDER BY log.logID DESC LIMIT 1";


		#2. get all entries where schedule="daily" and timestamp - today > (24*60*60)
		today=time.time()
		sql="SELECT dataContainer.dataID FROM 'dataContainer','log' WHERE schedule = 'daily' AND " + str(today) + " - log.end_timestamp > 86400 AND dataContainer.dataID = log.dataID AND dataContainer.lastJobID = log.logID" 
		self.cursor.execute(sql)
		dataContainerTuple=self.cursor.fetchall()
		#print dataContainerTuple
		for row in dataContainerTuple:
		    actionList.append( str(row[0]) );	
		
		

		#3. get all entries where schedule="weekly" and timestamp - today > (7*24*60*60)
		today=time.time()
		sql="SELECT dataContainer.dataID FROM 'dataContainer','log' WHERE schedule = 'weekly' AND " + str(today) + " - log.end_timestamp > 604800 AND dataContainer.dataID = log.dataID AND dataContainer.lastJobID = log.logID" 
		self.cursor.execute(sql)
		dataContainerTuple=self.cursor.fetchall()
		#print dataContainerTuple
		for row in dataContainerTuple:
		    actionList.append( str(row[0]) );	

		#4. get all entries where schedule="monthly" and timestamp - today > (4*7*24*60*60)
		today=time.time()
		sql="SELECT dataContainer.dataID FROM 'dataContainer','log' WHERE schedule = 'hourly' AND " + str(today) + " - log.end_timestamp > 2419200 AND dataContainer.dataID = log.dataID AND dataContainer.lastJobID = log.logID" 
		self.cursor.execute(sql)
		dataContainerTuple=self.cursor.fetchall()
		#print dataContainerTuple
		for row in dataContainerTuple:
		    actionList.append( str(row[0]) );	
		
		print actionList
		
		return actionList;	


	
	def cleanupZombieJobs( self ):
		# called on startup. switches every running job (status="running") to status = "unfinished"
		sql = "SELECT logID FROM log WHERE status='running'"
		self.cursor.execute(sql)
		for c in self.cursor.fetchall():
			print str(c[0]) + " not finished!"
		
		sql = "UPDATE log SET status='unfinished' WHERE status='running'"
		self.cursor.execute(sql)
		self.db.commit()
	

	def startJob(self, typ , dataId ):
		# create a log entry with status "running"
		timestamp = str( int(time.time()) )
		sql = "INSERT INTO log VALUES ( NULL,'%(typ)s','%(data)i','%(time)s','','running')" % {'typ': typ, 'data' : dataId , 'time' : timestamp }
		ret = self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.lastrowid

	def finishJob( self , dataID , logID , status ):
		
		timestamp = time.time()		

		sql = "UPDATE log SET status='%(status)s', end_timestamp='%(time)s' WHERE logID ='%(id)s' " % { 'time' : timestamp , 'status': status , 'id': logID}
		self.cursor.execute(sql)
		
		
		sql = "UPDATE dataContainer SET lastJobID = '%(id)s' WHERE dataID ='%(did)s' " % { 'did': dataID , 'id': logID}
		
		self.cursor.execute(sql)
		self.db.commit()

	def getArchiveInfo( self, dataID ):
		
		sql = "SELECT archive,compress,archive_ttl FROM dataContainer WHERE dataID = '%(id)s' " % { 'id': dataID }
		self.cursor.execute(sql)
		return self.cursor.fetchone()


	def checkTables(self):
		'''check if all tables  exists, create it otherwise'''



		#table dataContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='dataContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'dataContainer' (dataID INTEGER PRIMARY KEY, name Text, comment Text, localPath TEXT, remotePath TEXT,type TEXT, options TEXT, schedule TEXT,groupID INTEGER,lastJobID INTEGER, archive TEXT, compress TEXT,archive_ttl TEXT,pre_command TEXT,post_command TEXT)"
			self.cursor.execute(sql)
			self.db.commit()

		#table overview 
		#contains data about free space, location of the root container (MAINVOLUME by default) etc.
		#sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='overview'"
        	#self.cursor.execute(sql)
        	#row = self.cursor.fetchone()

        	#if not row:
		#	sql="CREATE TABLE 'overview' (rootID INTEGER PRIMARY KEY, path Text, current_job Text, current_job_started TEXT, last_job,type TEXT, options TEXT, schedule TEXT,groupID INTEGER)"
		#	self.cursor.execute(sql)
		#	self.db.commit()


		#table log
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='log'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'log' (logID INTEGER PRIMARY KEY, type TEXT, dataID INTEGER,start_timestamp TEXT, end_timestamp TEXT, status TEXT)"
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

		#table volumes
		
		#
		# volume = place to store backup data
		# the mainVolume is a special volume, it is the default location
		# and keeps the datenfresser database which stores the metadata
		# thus it can't be deleted.
		# 

		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='volumes'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'volumes' (volumeID INTEGER PRIMARY KEY, name TEXT, used_space TEXT,free_space TEXT)"
			self.cursor.execute(sql)

			sql="INSERT INTO volumes VALUES (NULL,'%s','unknown','unknown')" % MAINVOLUME
			self.cursor.execute(sql)
			self.db.commit()
	
		#tables rel_volumes_container
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='rel_volumes_container'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'rel_volumes_container' (containerID INTEGER, volumeID INTEGER )"
			self.cursor.execute(sql)
			self.db.commit()


	def get_running_jobs(self):
		
		jobList = []
		
		sql = "SELECT log.logID , log.start_timestamp , dataContainer.name FROM log,dataContainer WHERE log.status='running' AND log.dataID = dataContainer.dataID "
		self.cursor.execute(sql)
		for c in self.cursor.fetchall():
			tmp = job( c[0],c[1],c[2] );
			jobList.append( tmp )
			
		return jobList
	
	def get_log_entries(self, dataID):
		sql = "SELECT * FROM log WHERE dataID ='%s' ORDER BY start_timestamp desc" % dataID
		self.cursor.execute(sql)
		logList = []
		for c in self.cursor.fetchall():
			tmp = logEntry( c[0],c[1],c[2],c[3],c[4],c[5], );
			logList.append( tmp )
			
		return logList

	def getDataContainer(self,dataId):

		if dataId=="":
			nameCondition=""
		else:
			nameCondition=" WHERE dataId='%s'" % dataId
			
		sql="SELECT * FROM dataContainer" + nameCondition
		self.cursor.execute(sql)
		dataContainerList = []
		for c in self.cursor.fetchall():
			tmp = dataContainer(c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8]);
			if dataId !="": return [ tmp ]
			dataContainerList.append( tmp )
			
		return dataContainerList

						
					
	def add_volume( self, name ):
	    sql = "INSERT INTO volumes VALUES (NULL, '%s', 'unknown', 'unknown')" % name
	    self.cursor.execute(sql)
	    self.db.commit()		


 	def addDataContainer(self,name,comment,path,type,options,schedule,group, volume, archive, compress, archive_ttl, pre_command, post_command):
	    
		if type == "": type = "rsync"
		if schedule == "": schedule = "weekly"
	    
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

		localPath = MAINVOLUME + "/" + name + "/";
	
		#(dataID,name,comment,localPath,remotePath,type,options,schedule,groupID,archive,compress,archive_ttl,pre_command,post_command)
		#(dataID,name,comment,localPath,remotePath,type,options,schedule,groupID,archive,compress,archive_ttl,pre_command,post_command)
		sql="INSERT INTO dataContainer VALUES (NULL,'%(name)s','%(comment)s','%(name)s', '%(remotePath)s','%(type)s','%(options)s','%(schedule)s','%(group)s', NULL ,'%(archive)s','%(compress)s','%(archive_ttl)s','%(pre_command)s','%(post_command)s')"  %{ 'name': name, 'comment': comment, 'localPath': localPath, 'remotePath': path, "type": type, 'options':options,'schedule': schedule,'group':gid, 'archive': archive, 'compress': compress, 'archive_ttl': archive_ttl, 'pre_command': pre_command, 'post_command': post_command }
		print sql
		self.cursor.execute(sql)
		self.db.commit()

		#if not os.path.isdir(name):
		#	os.mkdir(name);

		#Check if theres no dataContainer named "name" in rootContainer
		return
		

	def addComment(self,container,comment):
		pass

	def updateComment(self,container,comment):
		pass

	def removeComment(self,container,comment):
		pass
