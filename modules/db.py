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
main_volume = c.getMainVolume()
db_location = c.getDbLocation()

class monitorLog:

	host ="example.org"
	start = 0
	end = 0
	dataId = 0
	remoteId = 0
	status = "no status available"
	error = "no error information available"
	transfered = 0

	def setTransferredData(self, v):
		self.transfered = v
	def getTranserredData(self):
		return self.transfered

	def setHost(self, h):
		self.host = h
	def getHost(self):
		return self.host

	def getDataId(self):
		return self.dataId
	def setDataId(self, v):
		self.dataId = v

	def setStartTimestamp(self, t):
		self.start = t
	def getStartTimestamp(self):
		return self.start

	def setEndTimestamp(self, t):
		self.end = t
	def getEndTimestamp(self):
		return self.end
	
	def setStatus(self, s):
		self.status = s
	def getStatus(self):
		return self.status

	def setError(self, e):
		self.error = e
	def getError(self):
		return self.error

	def setRemoteLogId(self, i):
		self.remoteId = i
	def getRemoteLogId(self):
		return self.remoteId


class database:

	def __init__(self):
		if not os.path.isdir( main_volume ):
			os.mkdir( main_volume )
		
		if not os.path.isdir( db_location ):
			os.mkdir( db_location )



		self.db = sqlite3.connect( db_location + "/datenfresser.db" )
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
		#print actionList


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
		sql="SELECT dataContainer.dataID FROM 'dataContainer','log' WHERE schedule = 'monthly' AND " + str(today) + " - log.end_timestamp > 2419200 AND dataContainer.dataID = log.dataID AND dataContainer.lastJobID = log.logID" 
		self.cursor.execute(sql)
		dataContainerTuple=self.cursor.fetchall()
		#print dataContainerTuple
		for row in dataContainerTuple:
		    actionList.append( str(row[0]) );
			
			
		#it is possible to schedule a backup directly by writing its dataID to /var/lib/datenfresser/immediate
		#no error checking so far ( if id is valid etc. )
		fname = "/var/lib/datenfresser/immediate"
		if os.path.isfile( fname ):
			f = open ( fname )
			ids = f.readlines()
			f.close()
			
			for element in ids:
				# the string contains a "\n" , so we're converting to int before to get rid of that..
				actionList.append( int(element) )
			os.remove( fname )
		#print actionList
		
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
		sql = "INSERT INTO log VALUES ( NULL,'%(typ)s','%(data)i','%(time)s','','running','','','')" % {'typ': typ, 'data' : dataId , 'time' : timestamp }
		ret = self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.lastrowid

	def finishJob( self , dataID , logID , status, errorMessage, stdOut  , transferredSize ):
		
		timestamp = time.time()		

		if status == "aborted":
			# half an hour penalty for a aborted job
			#timestamp = timestamp + 30*60
			pass

		#sql = "UPDATE log SET status='%(status)s', end_timestamp='%(time)s', errorMessage='%(err)s' WHERE logID ='%(id)s' " % { 'err': errorMessage, 'time' : timestamp , 'status': status , 'id': logID}
		#print sql
		#print errorMessage
		#self.cursor.execute(sql)

		self.cursor.execute( """UPDATE log SET status=?, end_timestamp=?, err_msg=?, std_out=?, transferredData=? WHERE logID =?""",  (status,timestamp,''.join( errorMessage ), ''.join( stdOut),  str(transferredSize),logID)) 
		

		
		
		sql = "UPDATE dataContainer SET lastJobID = '%(id)s' WHERE dataID ='%(did)s' " % { 'did': dataID , 'id': logID}
		
		self.cursor.execute(sql)
		self.db.commit()

	def getArchiveInfo( self, dataID ):
		
		sql = "SELECT archive,archive_method,compress,archive_ttl FROM dataContainer WHERE dataID = '%(id)s' " % { 'id': dataID }
		self.cursor.execute(sql)
		return self.cursor.fetchone()


	def checkTables(self):
		'''check if all tables  exists, create it otherwise'''



		#table dataContainer
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='dataContainer'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'dataContainer' (dataID INTEGER PRIMARY KEY, name Text, comment Text, localPath TEXT, remotePath TEXT,type TEXT, options TEXT, schedule TEXT,groupID INTEGER,lastJobID INTEGER, archive TEXT,archive_method TEXT, compress TEXT,archive_ttl TEXT,pre_command TEXT,post_command TEXT)"
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
			sql="CREATE TABLE 'log' (logID INTEGER PRIMARY KEY, type TEXT, dataID INTEGER,start_timestamp TEXT, end_timestamp TEXT, status TEXT,err_msg TEXT, std_out TEXT, transferredData TEXT)"
			self.cursor.execute(sql)
			self.db.commit()
		
		#table monitor-log
		# the table that holds the log entries of all hosts	
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='monitorLog'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'monitorLog' (metaLogID INTEGER PRIMARY KEY, host TEXT , remoteLogID INTEGER,  type TEXT, dataID INTEGER,start_timestamp TEXT, end_timestamp TEXT, status TEXT,err_msg TEXT, std_out TEXT, transferredData TEXT)"
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

		#table files  
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='files'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()
        	
		if not row:
			sql="CREATE TABLE 'files' (groupID INTEGER PRIMARY KEY, path TEXT, hash TEXT )"
			self.cursor.execute(sql)
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

			sql="INSERT INTO volumes VALUES (NULL,'%s','unknown','unknown')" % main_volume
			self.cursor.execute(sql)
			self.db.commit()
	
		#tables rel_volumes_container
		sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='rel_volumes_container'"
        	self.cursor.execute(sql)
        	row = self.cursor.fetchone()

        	if not row:
			sql="CREATE TABLE 'rel_volumes_container' (volumeID INTEGER, containerID INTEGER )"
			self.cursor.execute(sql)
			self.db.commit()

	def addFile( self , path ):
		pass

	def getLogs( self , minID):
		sql = "SELECT * from log WHERE logID > " + str(minID)
		self.cursor.execute(sql)
		
		logList = []

		for c in self.cursor.fetchall():
			tmpDict = {}	

			tmpDict["logID"] = c[0]
			tmpDict["type"] = c[1]
			tmpDict["dataID"] = c[2]
			tmpDict["start_timestamp"] = c[3]
			tmpDict["end_timestamp"] = c[4]
			tmpDict["status"] = c[5]
			tmpDict["err_msg"] = c[6]
			tmpDict["std_out"] = c[7]
			tmpDict["transferredData"] = c[8]

			logList.append( tmpDict )
			
		return logList
	
	def insertMonitorLog( self, monitorLog ):
		#metaLogID INTEGER PRIMARY KEY, 
		#host TEXT , 
		#remoteLogID INTEGER,  
		#type TEXT, 
		#dataID INTEGER,
		#start_timestamp TEXT, 
		#end_timestamp TEXT, status TEXT,err_msg TEXT, std_out TEXT, transferredData TEXT)"

		sql = "INSERT INTO monitorLog VALUES (NULL, '%(hostName)s', '%(rid)s', \
				'rsync', '0', '%(start)s' , '%(end)s' , '%(status)s', \
				'%(error)s','%(std)s','%(data)s')"  %{ 'hostName': monitorLog.getHost(), 'rid' : monitorLog.getRemoteLogId(), 'start' : monitorLog.getStartTimestamp(), 'end': monitorLog.getEndTimestamp(), 'status' : monitorLog.getStatus(), 'error' : monitorLog.getError(), 'std': monitorLog.getStatus(), 'data': monitorLog.getTranserredData()  }
		self.cursor.execute(sql)
		self.db.commit()


	def getAllLogs(self, lastId):
		results = []
		sql = ""

	
	def getLastRemoteLogID(self, host):
		#used at the monitoring server to determine which the highest already transferred logid is
		#(logid is called remoteLogId on the monitoring server)
		sql = "SELECT remoteLogID from monitorLog WHERE host = '%(hostName)s' ORDER BY remoteLogID desc LIMIT 1" % { 'hostName' : host }
		self.cursor.execute(sql)
		result = self.cursor.fetchone()

		if result == None: 
			return -1
		else:
			return result[0]



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
			tmp = logEntry( c[0],c[1],c[2],c[3],c[4],c[5],c[6] );
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

						
					
	
 	def addDataContainer(self,name,comment,path,type,options,schedule,group, volume, archive,archive_method, compress, archive_ttl, pre_command, post_command):
	    
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

		localPath = main_volume + "/" + name + "/";
	
		sql="INSERT INTO dataContainer VALUES (NULL,'%(name)s','%(comment)s','%(name)s', '%(remotePath)s','%(type)s','%(options)s','%(schedule)s','%(group)s', NULL ,'%(archive)s','%(archive_method)s','%(compress)s','%(archive_ttl)s','%(pre_command)s','%(post_command)s')"  %{ 'name': name, 'comment': comment, 'localPath': localPath, 'remotePath': path, "type": type, 'options':options,'schedule': schedule,'group':gid, 'archive': archive, 'archive_method': archive_method,'compress': compress, 'archive_ttl': archive_ttl, 'pre_command': pre_command, 'post_command': post_command }
		#print sql
		self.cursor.execute(sql)
		self.db.commit()

		#if not os.path.isdir(name):
		#	os.mkdir(name);

		#Check if theres no dataContainer named "name" in rootContainer
		return
		
	def deleteContainer( self, dataID ):	
		sql = "DELETE FROM  dataContainer WHERE dataID='" + dataID + "'"
		self.cursor.execute( sql )
		self.db.commit()
		
		return

	def addComment(self,container,comment):
		pass

	def updateComment(self,container,comment):
		pass

	def removeComment(self,container,comment):
		pass
