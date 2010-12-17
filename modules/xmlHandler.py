import os
import sys
import subprocess
import select

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from db import database

class xmlHandler:

	def __init__(self):
		pass
	
	def logEntryToXml( self, monitorLog ):
		return "<xml><host>example.com</host></xml>"

