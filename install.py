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


######################################################################
# Create config file 
######################################################################

if os.path.isfile(CONFIG_TEMPLATE):

	if os.path.isfile(CONFIG_FILENAME):
		print "File %s already exists. Do you want to overwrite it? y/n" % CONFIG_FILENAME
		if raw_input()!="y":
			self.exit(0)

	shutil.copyfile("./datenfresser.conf.tmpl","/etc/datenfresser.conf")
	print "Config file copied"

	backupDir=raw_input("backupDir:  [/var/datenfresser]")
	backupUser=raw_input("backup User: [backup]")

	if backupUser=="":
		backupUser="backup"

	if backupDir=="":
		backupDir="/var/datenfresser"


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
else:
	print "Configuration-Template ./datenfresser.conf.tmpl can't be found,  \
	aborting."
	sys.exit(0)


###################################################################
#check if user backupUser exists
###################################################################

try:
        pwd_entry=getpwnam(backupUser)
        backupUser_uid=pwd_entry[2]
        backupUser_gid=pwd_entry[3]

        if pwd_entry[6] != "":
                print "WARNING: There is an shell entry for user %s in /etc/passwd. This may be a security problem." %backupUser


except KeyError:

        ShellObj = os.popen('/usr/sbin/useradd %s' % backupUser )
        ShellObj.close()

        try:
                pwd_entry=getpwnam(backupUser)
                kabbit_uid=pwd_entry[2]
                kabbit_gid=pwd_entry[3]

        except KeyError:
                print "Failed to create user '%s'.Aborting." % backupUser
                sys.exit(1)

##################################################################


try:
	import sqlite
except Exception:
	print "python module sqlite is missing. Please install it."
	sys.exit(0)

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



shutil.copyfile("./modules/db.py",LIB_PATH + "/modules/db.py")
#shutil.copyfile("./mysql_db.py","/usr/lib/pyras/mysql_db.py")
#shutil.copyfile("./pyras_config.py","/usr/lib/pyras/pyras_config.py")
#shutil.copyfile("./ID3.py","/usr/lib/pyras/ID3.py")
#shutil.copyfile("./jabber.py","/usr/lib/pyras/jabber.py")
#shutil.copyfile("./debug.py","/usr/lib/pyras/debug.py")
#shutil.copyfile("./xmlstream.py","/usr/lib/pyras/xmlstream.py")
#shutil.copyfile("./filldb.py","/usr/lib/pyras/filldb.py")

#init.d skript
#shutil.copyfile("./datenfresser.sh","/etc/init.d/datenfresser")

#our executable
shutil.copyfile("./datenfresser.py","/usr/sbin/datenfresser")

#Look in our config file for mysql settings
sys.path.append(LIB_PATH)




print "Configuration successful"

sys.exit(0)


