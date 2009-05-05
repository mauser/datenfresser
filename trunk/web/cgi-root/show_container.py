#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.append("/usr/lib/datenfresser/modules")
from webcore import datenfresser_web
import cgi
import cgitb
from db import database


cgitb.enable()

a = datenfresser_web()
a.print_header()

form = cgi.FieldStorage()

print "<br /><br />"


if form.has_key("id"): 
    id = form["id"].value
    data = database()
    containerList = data.getDataContainer( id )
    print "<table>"
    for container in containerList:
	print "<h3>Showing container '" + container.name + "':</h3>" 
	for var in container.__dict__.keys():
	    print "<tr><td>" + var + "</td><td>" + str(container.__dict__[var]) + "</td>";
    print "</table>"
else:
    print "Error:  no valid id"
    sys.exit(0)