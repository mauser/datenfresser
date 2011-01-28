# -*- coding: utf-8 -*-
class datenfresser_web:
    def print_header( self ):
		print "HTTP/1.0 200 OK"
		print "Content-Type: text/html"
		print
	    	print "<html><head>"
		print "<title>Datenfresser</title>"
		print "<link rel='stylesheet' type='text/css' href='datenfresser.css'>"
		print "<script language='JavaScript'>"
		print """function toggleLayer( whichLayer )
		     {
			  var elem, vis;
			  if( document.getElementById ) // this is the way the standards work
			    elem = document.getElementById( whichLayer );
			  else if( document.all ) // this is the way old msie versions work
			      elem = document.all[whichLayer];
			  else if( document.layers ) // this is the way nn4 works
			    elem = document.layers[whichLayer];
			  vis = elem.style;
			  // if the style.display value is blank we try to figure it out here
			  if(vis.display==''&&elem.offsetWidth!=undefined&&elem.offsetHeight!=undefined)
			    vis.display = (elem.offsetWidth!=0&&elem.offsetHeight!=0)?'block':'none';
			  vis.display = (vis.display==''||vis.display=='block')?'none':'block';
			}"""

		print "</script>"
		print "</head><body>" ;
		print " <div id='banner'><img src='images/small.png'><div id='banner_text'>"
		print "<a href='index.py'>Show container</a>&nbsp;"
		#print "<a href='show_logs.py'>Show logs</a>&nbsp;"


		print "<a href='add_container.py'>Add container</a>&nbsp;"
		print "<a href='monitor.py'>View monitoring status</a>&nbsp;"
		
		print "</div></div><div height='300'>&nbsp;<br /><br /><br /><br /><br /></div>";
    
    def print_error( self , error_message ):
		print "<div id='error'>" + error_message + "</div>";
