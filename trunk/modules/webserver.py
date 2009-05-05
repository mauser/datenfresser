#!/usr/bin/python
# -*- coding: utf-8 -*-

#taken from python-forum.de ( modified )

import CGIHTTPServer, SocketServer
import BaseHTTPServer
import os, sys, socket, webbrowser

class MyRequestHandler( CGIHTTPServer.CGIHTTPRequestHandler ):

    def is_cgi(self):

        base, filename = os.path.split( self.path )

        if ".py" in filename:
            if "?" in filename:
                os.environ["SCRIPT_FILENAME"] = filename.split("?",1)[0]
            else:
                os.environ["SCRIPT_FILENAME"] = filename

            os.environ['DOCUMENT_ROOT']     =  os.getcwd()
            self.cgi_info = base, filename
            return True

class MyThreadingServer( SocketServer.ThreadingTCPServer ):
    allow_reuse_address = 1    # Seems to make sense in testing environment


    def __init__(self, server_address, request_handler, AllowIPs):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, request_handler)
        self.AllowIPs = [mask.split('.') for mask in AllowIPs]

    def server_bind(self):
        """Override server_bind to store the server name. (Parallele Anfragen)"""
        SocketServer.ThreadingTCPServer.server_bind(self)
        host, self.server_port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)

    def verify_request(self, dummy, client_address):
	#check if ip is allowed to use our service
        def check_ip(mask):
            for mask_part, ip_part in zip(mask, ip):
                if mask_part != ip_part and mask_part != '*':
                    return False
            return True

        ip = client_address[0].split('.')

        for mask in self.AllowIPs:
            if check_ip(mask):
                return True

        print "IP [%s] not allowed!" % client_address

        return False


class datenfresser_webserver:

    ListenPort = 80
    AllowIPs    = ('127.0.0.1', '192.168.*.*')
    
    def startServer( self ):
	try: 
		pid = os.fork() 
		if pid > 0:
		    sys.exit(0) 
	except OSError, e: 
		print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
		sys.exit(1) 

	httpd = MyThreadingServer( ("", self.ListenPort), MyRequestHandler, self.AllowIPs )
	httpd.serve_forever()

