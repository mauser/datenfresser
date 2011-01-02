#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.append("/usr/lib/datenfresser/modules")
from webcore import datenfresser_web
import cgi
import cgitb
from db import database
import datetime


def uniq(alist):    # Fastest without order preserving
    set = {}
    map(set.__setitem__, alist, [])
    return set.keys()

cgitb.enable()

a = datenfresser_web()
a.print_header()

form = cgi.FieldStorage()

print "<br /><br />"
print "<h3>Monitoring status</h3>"

data = database()
containerList = data.getRemoteDataContainer( "" )

hosts = []
hostContainer = {}


for container in containerList:
	hosts.append(container.host)
	if container.host in hostContainer.keys():
		hostContainer[container.host].append(container)
	else:
		hostContainer[container.host] = [ container ]


i = 0
for host in uniq(hosts):
	print "<h4><a href=\"javascript:toggleLayer('" + host + "');\" title='View all entries'>" + host + "</a></h4>"
	
	if i == 0:
		print "<div id='" + host + "'>"
	else:
		print "<div style='display: none;' id='" + host + "'>"

	for container in hostContainer[host]:
		print "<table>"
		print "<tr><td><b>" + container.name + "</b></td></tr>"
		logs =  data.getMonitorLogs( host, container.dataID )
		for log in logs:
			a = datetime.datetime.fromtimestamp( float(log.getStartTimestamp()) ) 
			print "<tr><td>" + a.ctime() + "</td></tr>"
		print "</table><br /><br />"
	print "</div>"
	i = i + 1


#if form.has_key("id"): 
#    id = form["id"].value
#    print "<table>"
#    for container in containerList:
#	print "<h3>Showing container '" + container.name + "':</h3>" 
#	for var in container.__dict__.keys():
#	    print "<tr><td>" + var + "</td><td>" + str(container.__dict__[var]) + "</td>";
#    print "</table>"
#else:
#    print "Error:  no valid id"
#    sys.exit(0)
