from linux_utils import linux_utils
from time import strftime
from time import localtime
class lso_design:

	def __init__(self):
	 	self.lx=linux_utils()

	def printHeader(self,lang,siteList):
		print "<html><head><title>datenfresser</title>"
		print '<link rel="stylesheet" type="text/css" href="red.css" /></head><body>'


		print "<div id='navi'>"


		print "<form action='index.php' method='get'><select name='lang'>"
		print "<option>de</option>"
		print "<option>en</option>"
		print "</select></div>"
		print "<div id='box'></div>"

	def printFooter(self):
		print "</body></html>"



