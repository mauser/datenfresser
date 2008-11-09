#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# The datenfresser Installer - Sebastian Moors, 20.12.2006
#
#
#


import sys
import os
import shutil

import fileinput
import string
from os.path import join

import os
import time

print "Welcome to the datenfresser installer.This is free software,you can distribute it under the terms of the GPL\n";

CONFIG_FILENAME="/etc/datenfresser.conf"
CONFIG_TEMPLATE="./datenfresser.conf.tmpl"


username  = "datenfresser"



def getpwnam(name,pwfile='/etc/passwd'):
	f = open(pwfile);
	while 1:
		line = f.readline()
		if not line:
			f.close()
			raise KeyError, name
		entry =  tuple(line.strip().split(':',6))
		if entry[0] == name:
			f.close
			return entry

def createConfig( username , backupdir ):

	shutil.copyfile("./datenfresser.conf.tmpl","/etc/datenfresser.conf")
	print "Config file copied"

	backupDir=raw_input("backupDir:  [/var/datenfresser]")
	backupUser=raw_input("backup User: [" + username  +"]")

	if backupUser=="":
		backupUser = username
		username = backupUser

	if backupDir=="":
		backupDir = backupdir
		if not os.path.isdir( backupDir ):
			os.mkdir( backupDir );	


	search_dict={}
	search_dict["@@backupDir@@"]=backupDir
	search_dict["@@backupUser@@"]=backupUser

	input = open(CONFIG_FILENAME)
	tmp=CONFIG_FILENAME + "~"
	output = open(tmp,'w')
	for s in input:
		for search_string in search_dict:
			s=s.replace(search_string,search_dict[search_string])
			output.write(s)
	output.close()
	input.close()
	shutil.move(tmp,CONFIG_FILENAME)

######################################################################
# Create config file 
######################################################################

if os.path.isfile(CONFIG_TEMPLATE):
	print "IN CONFIG TEMPL"
	if os.path.isfile(CONFIG_FILENAME):
		print "File %s already exists. Do you want to overwrite it? y/n" % CONFIG_FILENAME
		if raw_input()=="y": 
			createConfig(username,"/var/datenfresser")
	else:
		createConfig(username,"/var/datenfresser")

###################################################################
#check if user backupUser exists
###################################################################


try:
        pwd_entry=getpwnam( username )

        if pwd_entry[6] != "":
                print "WARNING: There is an shell entry for user %s in /etc/passwd. This may be a security problem." % username


except KeyError:

        ShellObj = os.popen('/usr/sbin/useradd %s' % username )
        ShellObj.close()

        try:
                pwd_entry=getpwnam( username )

        except KeyError:
                print "Failed to create user '%s'.Aborting." % username
                sys.exit(1)

##################################################################



#copy our own modules to /usr/lib/datenfresser
LIB_PATH="/usr/lib/datenfresser"

if os.path.isdir(LIB_PATH):
	#create defined states :)
	shutil.rmtree(LIB_PATH)
os.mkdir(LIB_PATH)
os.mkdir(LIB_PATH + "/" + "modules")



#copy data to /usr/share/datenfresser
DATA_PATH="/usr/share/datenfresser"
if not os.path.isdir(DATA_PATH):
		os.mkdir(DATA_PATH)



shutil.copyfile("./modules/metaStorage.py",LIB_PATH + "/modules/metaStorage.py")
shutil.copyfile("./modules/core.py",LIB_PATH + "/modules/core.py")
shutil.copyfile("./modules/rsync.py",LIB_PATH + "/modules/rsync.py")


shutil.copyfile("./modules/config.py",LIB_PATH + "/modules/config.py")

#init.d skript
shutil.copyfile("./datenfresser.sh","/etc/init.d/datenfresser")

#our executable
shutil.copyfile("./datenfresser.py","/usr/sbin/datenfresser")
shutil.copyfile("./datenfresserLCD.py","/usr/sbin/datenfresserLCD")



os.system("chmod +x /usr/sbin/datenfresser")
os.system("chmod +x /usr/sbin/datenfresserLCD")
os.system("chmod +x /etc/init.d/datenfresser")


#Look in our config file for mysql settings
sys.path.append(LIB_PATH)




print "Configuration successful"

sys.exit(0)


