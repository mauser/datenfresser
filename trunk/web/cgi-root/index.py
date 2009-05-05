#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.append("/usr/lib/datenfresser/modules")
from webcore import datenfresser_web
from db import database

a = datenfresser_web()
a.print_header()

data = database()

#get all data containers
c = ()
c = data.getDataContainer( "" )

if len(c) == 0:
	print "<h3>No container available.</h3>"
	sys.exit(0)


print "<br /><br /><br /><br /><br />"
print "<table><tr><th>Running Jobs</th></tr>"
for job in data.get_running_jobs():
	print "<tr><td>Job \"" +  job.name + "\" is running since  " + job.startTimestamp  + "</td></tr>"
print "</table><br>"


print "<table class=data_table><tr><th>Name</th><th>Remote location</th><th>Comment</th><th></th></tr>"
for container in c:
    	print "<div><tr>"
	print "<td>" + container.name + "</td>"
	print "<td>"+ container.remotePath + "</td>"
	print "<td>"+ container.comment + "</td>"
	print "<td><a href='show_container.py?id=" + str(container.dataID) + "'><img src='images/status.png' width='20' height='20' border='0'></a>"
	print "<a href='show_logs.py?id="+ str(container.dataID) + "'><img src='images/history.png' width='20' height='20' border='0'></a>"
	print "<a href='delete_container.py?id="+ str(container.dataID) + "'><img src='images/warning.png' width='20' height='20' border='0'></a></td>"
	print "</tr></div>"