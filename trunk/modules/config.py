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

		config = ConfigParser.ConfigParser()
		config.readfp(open('/etc/datenfresser.conf'))
		
		self.__main_volume = config.get("main","mainVolume")
		self.__poll_interval = config.get("main","poll_interval")
		self.__automatic_shutdown = config.get("main","automatic_shutdown")
		
		self.__webserver = config.get("webserver","webserver_enabled")
		self.__webserver_port = config.get("webserver","webserver_port")


	def getMainVolume( self ):
		return self.__main_volume
	
	def getWebserverEnabled( self ):
		return self.__webserver
		
	def getWebserverPort( self ):
		return self.__webserver_port
		
	def getPollInterval( self ):
		return self.__poll_interval

	def getAutomaticShutdown( self ):
		return self.__automatic_shutdown
		




