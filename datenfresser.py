#!/usr/bin/python

import os
import sys

sys.path.append("./modules")
from db import database

from time import sleep

#check if rsync is installed (local)
if os.system("which rsync > /dev/null") != 0:
	print "rsync not found "

db=database()
db.install()


while 1:
	sleep(1)
	db.tickAction()
	print "alive"	

sys.exit(0)

sshPort=24
serverName="kazan-music.de"

sshCommand="\'ssh -p %s\'" % sshPort

origin="/var/www/test"
destination="/var/datenfresser/mauser/my-data"

rsyncCommand="rsync -avz -e %(sshCmd)s --delete --delete-excluded %(server)s:%(origin)s %(destination)s 2> /dev/null > /dev/null" % {'sshCmd': sshCommand, 'server': serverName,'origin': origin, 'destination': destination}

r=os.system(rsyncCommand)
if r==0:
	print "Backup ok"
else:

	print rsyncCommand

	print r
	r = r >> 8
 

	if(r==127):
		print "rsync not found on host %s" % serverName
	elif(r==23):
		print "%s not found" % origin 
	else:
		print "An error ocurred"

	print r



