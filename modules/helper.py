
import sys
sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from db import database

import os


def executeCommand( command ):
	#excute command 
	#return returnValue: 0 if everything went ok, 1 in case that something went wrong..
		
	p = Popen( command.split(" "), bufsize=4024 ,stderr=PIPE,stdout=PIPE,close_fds=True)	
	(child_stderr) = ( p.stderr)
	(child_stdout) = ( p.stdout)

	output = child_stdout.readlines()
	errorMessage =  child_stderr.readlines()
	x = p.wait()
	errorMessage =  errorMessage + child_stderr.readlines()
	output = output + child_stdout.readlines()
	
	#convert "wait"-style exitcode to normal, shell-like exitcode
	exitcode = (x >> 8) & 0xFF
	return exitcode , errorMessage , output


def syncMonitorData():
	c = config()
	if c.getMonitorClientEnabled() == "False":
		return	
	
	#push changes to the monitoring server
	log( "trying monitorSync " + str(c.getMonitorClientEnabled()))
	try:
		monitorClient = datenfresserMonitorClient()
		monitorClient.sync()
	except Exception, e:
		traceback.print_exc(file=sys.stdout)
		log( str( sys.exc_info()[0] ) )
		log("Exception during monitor sync: " + str(e) )



def getDirectorySize(directory):
    #taken from http://roopindersingh.com/2008/04/22/calculating-directory-sizes-in-python/
    # returns the size of a directory ( in kilobytes a 1024 bits )
    class TotalSize:
        def __init__(self):
            self.total = 0

    def visit(totalSize, dirname, names):
        for name in names:
            absFilename = os.path.join(dirname, name)
            if os.path.isfile(absFilename):
                totalSize.total += os.path.getsize(absFilename)

    totalSize = TotalSize()
    os.path.walk(directory, visit, totalSize)
    return totalSize.total / 1024	   

def checkSyncDirs():
	c = config()
	d = database()
	container = d.getDataContainer("")	
	
	dir = c.getSyncDir()
	if dir != "" and dir[-1] == "/": dir = dir[:-1]	

	if dir != "" and os.path.isdir( dir ): 
		for con in container:
			if os.path.isdir( dir + "/" + con.name ) and con.name != "" and con.name !="." and os.listdir(dir + "/" + con.name) != [] :
				dest_path = MAINVOLUME + "/" + con.name + "/cur/"
				os.system("mv " + dir + "/" + con.name + "/* " +  dest_path )


