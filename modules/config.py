# -*- coding: utf-8 -*-
import ConfigParser
import getopt

import os
import sys

class config:

	__configHash={}

	def __init__(self):
		"""Class for Configuration Managment"""
	
		self.__username = ""
		self.__main_volume = ""
		
		try:
			config = ConfigParser.ConfigParser()
			config.readfp(open('/etc/datenfresser.conf'))
		except Exception, e: 
			return
		
		self.__main_volume = config.get("main","mainVolume")
		self.__db_location = config.get("main","db_location")
		self.__poll_interval = config.get("main","poll_interval")
		self.__automatic_shutdown = config.get("main","automatic_shutdown")
		self.__sync_dir=config.get("main","sync_dir")
		self.__start_delay=config.get("main","start_delay")
		self.__debug=config.get("main","debug")
		self.__username=config.get("main","username")	
		self.__hostname=config.get("main","hostname")	
		
		self.__webserver = config.get("webserver","webserver_enabled")
		self.__webserver_port = config.get("webserver","webserver_port")
		
		#
		# Config settings for the monitor server
		#

		try:
			self.__monitorClientEnabled = config.get("monitoring","monitorClient_enabled")
		except ConfigParser.NoSectionError:
			self.__monitorClientEnabled = "false"
			self.__remoteMonitorPort = 0 
			self.__remoteMonitorUser = ""
			self.__remoteMonitorPassword = ""

		try:
			self.__remoteMonitorServer = config.get("monitoring","remoteMonitorServer")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorServer = ""

		try:
			self.__remoteMonitorPort = config.get("monitoring","remoteMonitorPort")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorPort = 0 

		try:
			self.__remoteMonitorUser = config.get("monitoring","remoteMonitorUser")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorUser = ""
		
		try:
			self.__remoteMonitorPassword = config.get("monitoring","remoteMonitorPassword")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorPassword = ""




		#
		# Config settings for the monitor server
		#

		try:
			self.__monitorServerEnabled = config.get("monitoring","monitorServer_enabled")
		except ConfigParser.NoSectionError:
			self.__monitorServerEnabled = "false"
			self.__localMonitorPort = 0 
			self.__localMonitorUser = ""
			self.__localMonitorPassword = ""

		try:
			self.__localMonitorPort = config.get("monitoring","localMonitorPort")
		except ConfigParser.NoOptionError:
			self.__localMonitorPort = 0 

		try:
			self.__localMonitorUser = config.get("monitoring","localMonitorUser")
		except ConfigParser.NoOptionError:
			self.__localMonitorUser = ""
		
		try:
			self.__localMonitorPassword = config.get("monitoring","localMonitorPassword")
		except ConfigParser.NoOptionError:
			self.__localMonitorPassword = ""


		#
		# Config settings for notifications
		#

		try:
			self.__mailNotificationEnabled = config.get("notification","notify_by_mail")
		except ConfigParser.NoSectionError:
			self.__mailNotificationEnabled = "false"
			self.__smtpPort = 0 
			self.__smtpServer = ""
			self.__smtpPassword = ""
			self.__smtpUser = ""
			self.__mailRecipient = ""


		try:
			self.__smtpPort = config.get("notification","smtp_port")
		except ConfigParser.NoOptionError:
			self.__smtpPort = 25

		try:
			self.__smtpServer = config.get("notification","smtp_server")
		except ConfigParser.NoOptionError:
			self.__smtpServer = "localhost" 

		try:
			self.__smtpPassword = config.get("notification","smtp_password")
		except ConfigParser.NoOptionError:
			self.__smtpPassword = ""
		
		try:
			self.__smtpUser = config.get("notification","smtp_user")
		except ConfigParser.NoOptionError:
			self.__smtpUser = ""

		try:
			self.__mailRecipient = config.get("notification","mail_recipient")
		except ConfigParser.NoOptionError:
			self.__mailRecipient = ""





	def getDebug( self ):
		return self.__debug

	def getUsername( self ):
		return self.__username
	
	def getHostname( self ):
		return self.__hostname


	def getStartDelay( self ):
		return self.__start_delay

	def getMainVolume( self ):
		return self.__main_volume

	def getDbLocation( self ):
		return self.__db_location
	
	def getWebserverEnabled( self ):
		return self.__webserver
		
	def getWebserverPort( self ):
		return self.__webserver_port

	def getMonitorClientEnabled( self ):
		return self.__monitorClientEnabled

	def getMonitorServerEnabled( self ):
		return self.__monitorServerEnabled

	def getRemoteMonitorUser( self ):
		return self.__remoteMonitorUser

	def getRemoteMonitorServer(self):
		return self.__remoteMonitorServer

	def getRemoteMonitorPassword( self ):
		return self.__remoteMonitorPassword
		
	def getRemoteMonitorPort( self ):
		return self.__remoteMonitorPort


	def getMonitorClientEnabled( self ):
		return self.__monitorClientEnabled

	def getLocalMonitorUser( self ):
		return self.__localMonitorUser

	def getLocalMonitorPassword( self ):
		return self.__localMonitorPassword
		
	def getLocalMonitorPort( self ):
		return self.__localMonitorPort

	def getSmtpPort( self ):
		return self.__smtpPort

	def getSmtpUser( self ):
		return self.__smtpUser

	def getSmtpPassword( self ):
		return self.__smtpPassword

	def getSmtpServer( self ):
		return self.__smtpServer

	def getNotifyByMailEnabled( self ):
		return self.__mailNotificationEnabled
	
	def getMailRecipient( self ):
		return self.__mailRecipient
		
	def getPollInterval( self ):
		return self.__poll_interval

	def getAutomaticShutdown( self ):
		return self.__automatic_shutdown
		
	def getSyncDir( self ):
		return self.__sync_dir


class CliArguments:
	def __init__( self ):
		self.monitor = False
		self.verbose = False
		self.daemon = False
		self.forceAll = False



