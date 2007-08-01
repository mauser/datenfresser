#!/usr/bin/python

import sys

sys.path.append("/usr/lib/datenfresser/modules")

from metaStorage import storage

s=storage()
metaDict = s.loadMetaData()
for key in metaDict:
	if metaDict[key].lock:
		print "Backup: " + key

