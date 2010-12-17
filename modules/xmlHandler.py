import os
import sys
import subprocess
import select

import xml.dom.minidom as dom

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from db import database
from db import monitorLog

class xmlHandler:

	def __init__(self):
		pass

	def createNode( self, document,  nodeName, string):
		node = document.createElement( nodeName )
		node.appendChild(document.createTextNode( str(string) ))
		return node
	
	def logEntryToXml( self, monitorLog ):

		doc = dom.Document()
		root = dom.Element("datenfresser")
	
		root.appendChild( self.createNode( doc , "host" , monitorLog.getHost() ))
		root.appendChild( self.createNode( doc , "rid" , monitorLog.getRemoteLogId() ))
		root.appendChild( self.createNode( doc , "did" , monitorLog.getDataId() ))
		root.appendChild( self.createNode( doc , "start" , monitorLog.getStartTimestamp() ))
		root.appendChild( self.createNode( doc , "end" , monitorLog.getEndTimestamp() ))
		root.appendChild( self.createNode( doc , "error" , monitorLog.getError() ))
		root.appendChild( self.createNode( doc , "status" , monitorLog.getStatus() ))
		
		doc.appendChild(root)
		return doc.toxml()	


	def parseXml( self, xmlDocument ):
		return monitorLog()

