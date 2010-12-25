import os
import sys
import subprocess
import select


import xml.dom.minidom as dom
from xml.dom.minidom import parseString

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from db import database
from db import monitorLog
from core import dataContainer

def getText(nodelist):
    rc = []
    for node in nodelist:
	if node.nodeType == node.TEXT_NODE:
	    rc.append(node.data)
    return ''.join(rc)



class xmlHandler:



	def __init__(self):
		pass

	def createNode( self, document,  nodeName, string):
		node = document.createElement( nodeName )
		node.appendChild(document.createTextNode( str(string) ))
		return node

	def dataContainerToXml(self, host, dataContainer):
		doc = dom.Document()
		root = dom.Element("dataContainer")

		dataContainer.updateChecksum()

		root.appendChild( self.createNode( doc , "host" , host ))
		root.appendChild( self.createNode( doc , "name" , dataContainer.name ))
		root.appendChild( self.createNode( doc , "comment" , dataContainer.comment ))
		root.appendChild( self.createNode( doc , "checksum" , dataContainer.checksum ))
		root.appendChild( self.createNode( doc , "archive" , dataContainer.archive))
		root.appendChild( self.createNode( doc , "archive_method" , dataContainer.archive_method ))
		root.appendChild( self.createNode( doc , "archive_ttl" , dataContainer.archive_ttl))
		root.appendChild( self.createNode( doc , "dataID" , dataContainer.dataID ))
		root.appendChild( self.createNode( doc , "compress" , dataContainer.compress ))
		root.appendChild( self.createNode( doc , "options" , dataContainer.options ))
		root.appendChild( self.createNode( doc , "schedule" , dataContainer.schedule ))
		root.appendChild( self.createNode( doc , "remotePath" , dataContainer.remotePath ))
		
		doc.appendChild(root)
		print doc.toxml()
		return doc.toxml()	

	

	
	def logEntryToXml( self, host, logEntry ):
		#converts a log entry of the client to its xml representation 

		doc = dom.Document()
		root = dom.Element("monitorLogEntry")
	
		root.appendChild( self.createNode( doc , "host" , host ))
		root.appendChild( self.createNode( doc , "rid" , logEntry['logID'] ))
		root.appendChild( self.createNode( doc , "dataId" , logEntry['dataID']))
		root.appendChild( self.createNode( doc , "start_timestamp" , logEntry['start_timestamp'] ))
		root.appendChild( self.createNode( doc , "end_timestamp" , logEntry['end_timestamp'] ))
		root.appendChild( self.createNode( doc , "error" , logEntry['err_msg'] ))
		root.appendChild( self.createNode( doc , "std_out" , logEntry['std_out'] ))
		root.appendChild( self.createNode( doc , "transferredData" , logEntry['transferredData'] ))
		
		doc.appendChild(root)
		return doc.toxml()	


	def parseXml( self, xmlDocument ):

		dom = parseString( xmlDocument.strip() )
	
		#decide if this is #dataContainer or #monitorLogEntry
		monitorLogs = dom.getElementsByTagName("monitorLogEntry")
		container = dom.getElementsByTagName("dataContainer")

		if len(monitorLogs) == 1:
			m = monitorLog()
			for tag in ['host','rid','dataId','start_timestamp','end_timestamp','error','std_out','transferredData']:
				for node in dom.getElementsByTagName(tag):
					text = getText(node.childNodes)	
					if tag == "host": m.setHost( text )
					if tag == "rid": m.setRemoteLogId( text )
					if tag == "dataId": m.setDataId( text )
					if tag == "start_timestamp": m.setStartTimestamp( text )
					if tag == "end_timestamp": m.setEndTimestamp( text )
					if tag == "error": m.setError( text )
					if tag == "std_out": m.setStatus( text )
					if tag == "transferredData": m.setTransferredData( text )

			return m

		if len(container) == 1:
			m = dataContainer('default')
			for tag in ['host','name','comment','checksum','archive','archive_method','archive_ttl','options','compress','schedule','dataID','remotePath']:
				for node in dom.getElementsByTagName(tag):
					text = getText(node.childNodes)
					if tag == "dataID": m.dataID = text
					if tag == "host": m.host = text 
					if tag == "name": m.name = text 
					if tag == "comment": m.comment = text 
					if tag == "checksum": m.checksum = text
					if tag == "archive": m.archive = text
					if tag == "archive_method": m.archive_method = text
					if tag == "archive_ttl": m.archive_ttl = text
					if tag == "options": m.options = text
					if tag == "compress": m.compress = text
					if tag == "schedule": m.schedule = text
					if tag == "remotePath": m.remotePath = text


			return m



