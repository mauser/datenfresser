import os
import sys
import subprocess
import select

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from db import database

class XmlHandler:
	
	def logEntryToXml( self, monitorLog ):
		return "<xml><host>example.com</host></xml>"

