import ConfigParser
import getopt

import os
import sys

CONFIG_FILENAME='/etc/datenfresser.conf'

class config:
	
	def __init__(self):
		"""Class for Configuration Managment"""

		#parse config file
		config = ConfigParser.ConfigParser()
		if not os.path.isfile(CONFIG_FILENAME):
			self.init_configuration();
				


		config.readfp(open(CONFIG_FILENAME))
		self.base_dir="/usr/share/datenfresser"
		try:		
			self.rootContainer=os.path.expanduser(config.get("main","backupDir"))
		except Exception:
			print "FATAL ERROR: Unable to retrieve backupDir from configuration."
			sys.exit(0)	

		#parse command line arguments
		try:
			long_opts=["help","create=","Port=","method=","path=","list"]
        		opts, args = getopt.getopt(sys.argv[1:], "hc:p:m:P:",long_opts )

		except getopt.GetoptError:
        		# wrong options etc.
			# print help information and exit:
        		self.usage()
        		sys.exit(2)

		self.path=""
		self.port=0
		self.method=""
		self.create=0

		for option, argument in opts:
			#if o == "-r":
			#	verbose = True
			if option in ("-h", "--help"):
				self.usage()
				sys.exit()

			if option in ("-p","--path"):
				self.path=argument

			if option in ("-P","--Port"):
				self.port=argument

			if option in ("-m","--method"):
				self.method=method

			if option in ("-c","--create"):
				self.create=argument
				if self.path=="":
					self.usage()
					sys.exit(0)
				
	
			else:
				self.create=0
				
			#if option in ("-p", "--port"):
			#	self.webport=int(argument)
			
	def usage(self):
		"""Print informations about the usage of datenfresser"""
		print "Invalid Option / Argument.\n"
		print "Available Options:"
		print "\t -h,--help		print help"
		print "\t -c,--create dirname	create dataContainer dirname"
		print "\t -p,--path url		path to backup"
		print "\t -m,--method method	wget or rsync "
		print "\t -P,--Port port	SSH port (for rsync)"
