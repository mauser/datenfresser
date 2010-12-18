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
	
	def logEntryToXml( self, host, logEntry ):
		#converts a log entry of the client to its xml representation 

		doc = dom.Document()
		root = dom.Element("datenfresser")
	
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
		m = monitorLog()

		for node in dom.getElementsByTagName('host'):
			text = getText(node.childNodes)	
			if text == "host": m.setHost( text )
			if text == "rid": m.setRemoteLogId( text )
			if text == "dataId": m.setDataId( text )
			if text == "start_timestamp": m.setStartTimestamp( text )
			if text == "end_timestamp": m.setEndTimestamp( text )
			if text == "error": m.setError( text )
			if text == "std_out": m.setStatus( text )
			if text == "transferredData": m.setTransferredData( text )


		return m

