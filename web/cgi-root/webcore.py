# -*- coding: utf-8 -*-
class datenfresser_web:
    def print_header( self ):
		print "HTTP/1.0 200 OK"
		print "Content-Type: text/html"
		print
	    	print "<html><head><title>Datenfresser</title><link rel='stylesheet' type='text/css' href='datenfresser.css'></head><body>" ;
		print " <div id='banner'><img src='images/small.png'><div id='banner_text'><a href='index.py'>Show container</a>&nbsp;<a href='show_logs.py'>Show logs</a>&nbsp;<a href='add_container.py'>Add container</a>&nbsp;</div></div><div height='300'>&nbsp;<br /><br /><br /><br /><br /></div>";
    
    def print_error( self , error_message ):
		print "<div id='error'>" + error_message + "</div>";