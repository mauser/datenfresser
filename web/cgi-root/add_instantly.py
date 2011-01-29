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

if form.has_key('id'):
	file = open("/var/lib/datenfresser/immediate", "w")
	file.write( form['id'].value + "\n" )
	file.close() 
