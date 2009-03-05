# -*- coding: utf-8 -*-
import ConfigParser
import getopt

import os
import sys

class config:

	__configHash={}

	def __init__(self):
		"""Class for Configuration Managment"""
		config = ConfigParser.ConfigParser()

		config.readfp(open('/etc/datenfresser.conf'))

		self.__username=""
		self.__main_volume=""

		self.__main_volume= config.get("main","mainVolume")


	def getMainVolume( self ):
		return self.__main_volume




