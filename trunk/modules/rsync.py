import os

class rsyncData:
	def __init__(self,port=22,user="backup"):
		self.port=port
		self.user=user



def rsync(localPath,remotePath,port,user):
	
	sshCommand="\'ssh -l %(user)s  -p %(port)s\'" % {'user': user, 'port': port }
	origin=remotePath
	destination=localPath
	rsyncCommand="rsync -avz -e %(sshCmd)s --delete --delete-excluded %(origin)s %(destination)s 2> /dev/null > /dev/null" % {'sshCmd': sshCommand, 'origin': origin, 'destination': destination}
	print rsyncCommand
	
	r = os.system(rsyncCommand)

	if r == 0:
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
	
