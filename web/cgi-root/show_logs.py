#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.append("/usr/lib/datenfresser/modules")
from webcore import datenfresser_web
import cgi
import cgitb
from db import database
from datetime import datetime

cgitb.enable()

a = datenfresser_web()
a.print_header()

form = cgi.FieldStorage()
if form.has_key("id"): 
    id = form["id"].value
    
    daba = database()
    
    print "<br /><br />"
    print "<br /><table>\n";
    print "<tr><th>Type</th><th>Start</th><th>End</th><th>Status</th></tr>"
    for log in daba.get_log_entries( id ):
		
		if log.startTimestamp == "": 
			startTimestamp = 0
		else:
			startTimestamp = log.startTimestamp
		
		if log.endTimestamp == "": 
			endTimestamp = 0
		else:
			endTimestamp = log.endTimestamp
		
		print "<tr>"
		print "<td>" + log.type +  "</td>"
		print "<td>" + datetime.fromtimestamp( float(startTimestamp) ).ctime() + "</td>"
		print "<td>" + datetime.fromtimestamp( float(endTimestamp) ).ctime() + "</td>"
		print "<td>" + log.status  + "</td>"


		print "</tr>"

	
