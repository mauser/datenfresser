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

def createConfig( username , mainVolume_preset ):

	mainVolume=raw_input("main backup volume:  [/var/datenfresser]")
	backupUser=raw_input("backup user: [" + username  +"]")

	if backupUser=="":
		backupUser = username

	if mainVolume=="": 
		mainVolume = mainVolume_preset
		
	if not os.path.isdir( mainVolume ):
		os.mkdir( mainVolume );	


	output = open( CONFIG_FILENAME , "w")
	
	output.write("[main]\n")
	output.write("mainVolume=" + mainVolume + "\n")
	output.write("username=" + backupUser + "\n")
	output.write("db_location=/var/lib/datenfresser\n")
	output.write("automatic_shutdown=0\n")
	output.write("sync_dir=\n")
	output.write("start_delay=0\n")
	output.write("debug=0\n")
	
	output.write("\n#seconds after datenfresser checks if a new job is ready to run\n")
	output.write("poll_interval=60" "\n")
	
	output.write("[webserver]\n")
	output.write("webserver_enabled=True\n")
	output.write("webserver_port=8080\n")

	output.close()
	return ( backupUser , mainVolume )


######################################################################
# Create config file 
######################################################################

user = "" 
volume = ""

if os.path.isfile(CONFIG_FILENAME):
	print "File %s already exists. Do you want to overwrite it? y/n" % CONFIG_FILENAME
	if raw_input()=="y": 
		(user , volume) = createConfig(username,"/var/datenfresser")
else:
	( user,volume) = createConfig(username,"/var/datenfresser")

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

if os.path.isdir( LIB_PATH ):
	#create defined states :)
	shutil.rmtree(LIB_PATH)
os.mkdir( LIB_PATH )
os.mkdir( LIB_PATH + "/" + "modules" )
os.mkdir( LIB_PATH + "/" + "web" )
os.mkdir( LIB_PATH + "/" + "web/cgi-root" )



#copy data to /usr/share/datenfresser
DATA_PATH="/usr/share/datenfresser"
if not os.path.isdir( DATA_PATH ):
	os.mkdir( DATA_PATH )

#database dir
if not os.path.isdir ( "/var/lib/datenfresser" ):
	os.mkdir( "/var/lib/datenfresser" ) 


shutil.copyfile("./modules/db.py",LIB_PATH + "/modules/db.py")
shutil.copyfile("./modules/core.py",LIB_PATH + "/modules/core.py")
shutil.copyfile("./modules/config.py",LIB_PATH + "/modules/config.py")
shutil.copyfile("./modules/webserver.py",LIB_PATH + "/modules/webserver.py")


shutil.copyfile("./web/index.html",LIB_PATH + "/web/index.html")
shutil.copyfile("./web/cgi-root/datenfresser.css",LIB_PATH + "/web/cgi-root/datenfresser.css")
shutil.copyfile("./web/cgi-root/index.py",LIB_PATH + "/web/cgi-root/index.py")
shutil.copyfile("./web/cgi-root/add_container.py",LIB_PATH + "/web/cgi-root/add_container.py")
shutil.copyfile("./web/cgi-root/show_container.py",LIB_PATH + "/web/cgi-root/show_container.py")
shutil.copyfile("./web/cgi-root/show_logs.py",LIB_PATH + "/web/cgi-root/show_logs.py")
shutil.copyfile("./web/cgi-root/delete_container.py",LIB_PATH + "/web/cgi-root/delete_container.py")
shutil.copyfile("./web/cgi-root/webcore.py",LIB_PATH + "/web/cgi-root/webcore.py")

shutil.copytree("./web/cgi-root/images/", LIB_PATH + "/web/cgi-root/images")

#init.d skript
shutil.copyfile("./datenfresser.sh","/etc/init.d/datenfresser")

#our executable
shutil.copyfile("./datenfresser.py","/usr/sbin/datenfresser")


#adjust permissions
os.system("chmod +x /usr/sbin/datenfresser")
os.system("chmod +x /etc/init.d/datenfresser")
os.system("chmod +x " + LIB_PATH + "/web/cgi-root/*.py")

os.system("chown -R " + user + " " + volume)
os.system("chown -R " + user + " " + "/var/lib/datenfresser")

print "Configuration successful"

sys.exit(0)


