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

#name = form.getvalue( "name" )

if  not form.has_key('name'):
    print '''
    <h3>Create new container</h3>
    <form action="add_container.py" method="post">
    <table>
	    <tr><td>Name:</td><td><input type="text" name="name"></td></tr>
	    <tr><td>Remote path:</td><td><input type="text" name="rpath"></td></tr>
	    <tr><td>Rsync options:</td><td><input type="text" name="options"></td></tr>
	    <tr><td>Volume:</td><td><select name="volume">
	    <?
		    $volumes = $core->get_volumes();
		    foreach( $volumes as $volume){
			    print "<option>$volume</option>";
		    }
	    ?>
	    </td></tr>	
	    <tr><td>Comment:</td><td><input type="text" name="comment"></td></tr>
	    <tr><td>Schedule:</td><td>
					    <select name="schedule">
						    <option>daily</option>
						    <option>weekly</option>
						    <option>monthly</option>
					    </select>
				    </td></tr>
	    
	    <tr><td>Archive schedule:</td><td>
					    <select name="archive_schedule">
						    <option>disabled</option>
						    <option>daily</option>
						    <option>weekly</option>
						    <option>monthly</option>
					    </select>
				    </td></tr>
	    <tr><td>Archive method:</td><td>
			    <select name="archive_method">
				    <option>tar</option>
				    <option>btrfs snapshot</option>
					<option>hardlinks</option>
			    </select>
		    </td></tr>		   
	    <tr><td>Compress:</td><td><input type="checkbox" name="compress"></td></tr>
	    <tr><td>Keep archives:</td><td><input type="text" name="archive_ttl"> days</td></tr>
	    <tr><td>pre-command:</td><td><input type="text" name="pre_command"> days</td></tr>
	    <tr><td>post-command:</td><td><input type="text" name="post_command"> days</td></tr>
	    


	    <tr><td colspan="2"><input type="submit"></td></tr>
    </table>
    </form>'''
else:

    print "<br>"
    values = {}
    data = database()
    

    if not form.has_key("rpath"):
	print "Error: please fill in a remote path!"
	sys.exit(0)
    
    for element in  ['name', 'comment', 'rpath', 'type', 'options', 'volume', 'schedule','archive_schedule','archive_method', 'compress','archive_ttl','pre_command','post_command' ]:
	if not form.has_key( element ):
	    values[ element ] = ""
	else:
	    values[ element ] = form[ element ].value
	
    group = "ALL"
    clean_name = values['name'].replace("/","-") 
    data.addDataContainer(clean_name,values['comment'],values['rpath'],values['type'],values['options'],values['schedule'],group, values['volume'], values['archive_schedule'], values['archive_method'],values['compress'], values['archive_ttl'], values['pre_command'], values['post_command'])
    print "added Container"
