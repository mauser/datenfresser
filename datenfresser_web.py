#!/usr/bin/python

#system modules
import os
import sys

sys.path.append("./modules")

#web.py module
import web




#our design module
#from design import *


#module to determine mimetypes (used by image function..)
import mimetypes


urls = (
	'/', 'index',
	 '/([a-zA-Z_]+).css','css',
	'/images/([a-zA-Z_]+).png', 'static',
	'/index.html','index'
  )

class index:



	def GET(self):

		get_input = web.input()

		try:
			site=get_input["site"]

		except KeyError:
			#no site is given
			site="index"

		design=lso_design()

		lang="de"

		#check if the demanded site exists
		if p.siteList.has_key(site):
			siteObject=p.siteList[site]
		else:
			#if not, print error page
			#TODO: modify http-header to get 404
			siteObject=p.siteList["404"]


		design.printHeader(lang,p.siteList)
		siteObject.printPage()



class css:
	def GET(self,name):
		web.header("Content-Type","text/css; charset=utf-8")
		fname='css/' + name + '.css'
		if os.path.isfile(fname):
    			print open(fname).read()


def mime_type(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class static:
    def GET(self, static_dir):
        try:
            static_file_name = web.context.path.split('/')[-1]
            web.header('Content-type', mime_type(static_file_name))
            static_file = open('.' + web.context.path, 'rb')
            web.ctx.output = static_file

        except IOError:
            web.notfound()

web.internalerror = web.debugerror

if __name__ == '__main__':
	web.run(urls, web.reloader)
