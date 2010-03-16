#!/usr/bin/python
# -*- coding: utf-8 -*-

class datenfresser_web:
    def print_header( self ):
		print "HTTP/1.0 200 OK"
		print "Content-Type: text/html"
		print
	    	print "<html><head><title>Datenfresser 2</title><link rel='stylesheet' type='text/css' href='datenfresser.css'></head><body>" ;
		print " <div id='banner'><img src='images/small.png'><div id='banner_text'><a href='index.py'>Show container</a><a href='add_container.php'>Add container</a><a href='show_volumes.php'>Volumes</a></div></div><div height='300'>&nbsp;<br /><br /><br /><br /><br /></div>";

a = datenfresser_web()
a.print_header()
