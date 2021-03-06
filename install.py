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
import getopt

sys.path.append("./modules")

from config import config
from socket import gethostname 

print "Welcome to the datenfresser installer.This is free software,you can distribute it under the terms of the GPL\n";

CONFIG_FILENAME = "/etc/datenfresser.conf"
CONFIG_TEMPLATE = "./datenfresser.conf.tmpl"

#no debug output by default
verbose = False

if os.path.isfile( CONFIG_FILENAME ):
	c = config()
	DEFAULT_MAINVOLUME = c.getMainVolume()
	USERNAME = c.getUsername()	
else:
	DEFAULT_MAINVOLUME = "/var/datenfresser"
	USERNAME  = "datenfresser"
	

def debugPrint( string ):
	if verbose: print string


def getpwnam(name,pwfile='/etc/passwd'):
	debugPrint( "starting to parse " + pwfile)
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

def createConfig( USERNAME , mainVolume_preset ):


	mainVolume = raw_input( "main backup volume:  [%s]" % DEFAULT_MAINVOLUME) 
	backupUser = raw_input( "backup user: [%s]" % USERNAME) 

	if backupUser == "":
		backupUser = USERNAME

	if mainVolume == "": 
		mainVolume = DEFAULT_MAINVOLUME
		
	if not os.path.isdir( mainVolume ):
		try:
			os.mkdir( mainVolume );
		except OSError: 
			print "Creating the directory %s failed." % mainVolume
			sys.exit(1)

	output = open( CONFIG_FILENAME , "w")
	
	output.write("[main]\n")
	output.write("mainVolume=" + mainVolume + "\n")
	output.write("username=" + backupUser + "\n")
	output.write("db_location=/var/lib/datenfresser\n")
	output.write("automatic_shutdown=0\n")
	output.write("sync_dir=\n")
	output.write("start_delay=0\n")
	output.write("debug=0\n")
	output.write("hostname=" + gethostname() + "\n")
	
	output.write("\n#seconds after datenfresser checks if a new job is ready to run\n")
	output.write("poll_interval=60" "\n\n")
	
	output.write("[webserver]\n")
	output.write("webserver_enabled=False\n")
	output.write("webserver_port=8080\n\n")
	
	
	output.write("[notification]\n")
	output.write("notify_by_mail=False\n")
	output.write("mail_recipient=\n")
	output.write("smtp_port=25\n")
	output.write("smtp_server=localhost\n")
	output.write("smtp_user=\n")
	output.write("smtp_password=\n\n")
	
	output.write("[monitoring]\n")
	output.write("monitorServer_enabled=False\n")
	output.write("localMonitorPort=8090\n")
	output.write("localMonitorUser=\n")
	output.write("localMonitorPassword=\n\n")
	
	output.write("monitorClient_enabled=False\n")
	output.write("remoteMonitorServer=\n")
	output.write("remoteMonitorPort=8090\n")

	output.write("remoteMonitorUser=\n")
	output.write("remoteMonitorPassword=\n")

	output.close()
	return ( backupUser , mainVolume )


######################################################################
# Create config file 
######################################################################

user = "" 
volume = ""
overwrite = False

try:
	opts, args = getopt.getopt(sys.argv[1:], "hov", ["help", "overwrite", "verbose"])
except getopt.GetoptError, err:
	print str(err) 
	#usage()
	sys.exit(2)

for o, a in opts:
        if o == "-v":
	    verbose = True
        if o == "-o":
            overwrite = True
        elif o in ("-h", "--help"):
            #usage()
            sys.exit()


c =config()
if os.path.isfile(CONFIG_FILENAME):
	if overwrite == False:
		print "File %s already exists. Do you want to overwrite it? y/n" % CONFIG_FILENAME
		if raw_input()=="y": 
			(user , volume) = createConfig(USERNAME,"/var/datenfresser")
		else:
			user = c.getUsername()
	else:
			user = c.getUsername()

else:
	(user,volume) = createConfig(USERNAME,"/var/datenfresser")

###################################################################
#check if user backupUser exists
###################################################################

debugPrint( "Checking if user already exists.. " )
try:
	if sys.platform != "darwin":
        	pwd_entry=getpwnam( USERNAME )
        	if pwd_entry[6] != "":
                	print "WARNING: There is an shell entry for user %s in /etc/passwd. This may be a security problem." % USERNAME


except KeyError:

	debugPrint( "Calling useradd " + USERNAME ) 	
        ShellObj = os.popen('/usr/sbin/useradd %s' % USERNAME )
        ShellObj.close()

        try:
                pwd_entry=getpwnam( USERNAME )
		debugPrint("Adding user was successful")

        except KeyError:
                print "Failed to create user '%s'.Aborting." % USERNAME
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

if sys.platform == "darwin":
	if not os.path.isdir( "/System/Library/StartupItems/datenfresser" ): 
		os.mkdir( "/System/Library/StartupItems/datenfresser" ) 
	shutil.copyfile("./datenfresser.sh","/System/Library/StartupItems/datenfresser/datenfresser")

if sys.platform == "linux2":
	shutil.copyfile("./datenfresser.sh","/etc/init.d/datenfresser")




for module in os.listdir("./modules"): 
	shutil.copyfile("./modules/" + module, LIB_PATH + "/modules/" + module)


shutil.copyfile("./web/index.html",LIB_PATH + "/web/index.html")

shutil.copyfile("./web/cgi-root/datenfresser.css",LIB_PATH + "/web/cgi-root/datenfresser.css")
shutil.copyfile("./web/cgi-root/index.py",LIB_PATH + "/web/cgi-root/index.py")
shutil.copyfile("./web/cgi-root/add_instantly.py",LIB_PATH + "/web/cgi-root/add_instantly.py")
shutil.copyfile("./web/cgi-root/add_container.py",LIB_PATH + "/web/cgi-root/add_container.py")
shutil.copyfile("./web/cgi-root/show_container.py",LIB_PATH + "/web/cgi-root/show_container.py")
shutil.copyfile("./web/cgi-root/show_logs.py",LIB_PATH + "/web/cgi-root/show_logs.py")
shutil.copyfile("./web/cgi-root/delete_container.py",LIB_PATH + "/web/cgi-root/delete_container.py")
shutil.copyfile("./web/cgi-root/webcore.py",LIB_PATH + "/web/cgi-root/webcore.py")
shutil.copyfile("./web/cgi-root/monitor.py",LIB_PATH + "/web/cgi-root/monitor.py")

shutil.copytree("./web/cgi-root/images/", LIB_PATH + "/web/cgi-root/images")

#init.d skript

#our executable
shutil.copyfile("./datenfresser.py","/usr/sbin/datenfresser")


#adjust permissions
os.system("chmod +x /usr/sbin/datenfresser")

if sys.platform == "darwin":
	os.system("chmod +x /System/Library/StartupItems/datenfresser/datenfresser")
else:
	os.system("chmod +x /etc/init.d/datenfresser")

os.system("chmod +x %s/web/cgi-root/*.py" % LIB_PATH)

os.system("chown -R %s /var/lib/datenfresser" % user)
os.system("touch /var/log/datenfresser.log")
os.system("chown -R %s /var/log/datenfresser.log" % user)

print "Configuration successful"

sys.exit(0)


