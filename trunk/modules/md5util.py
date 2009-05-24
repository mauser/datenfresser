#!/usr/bin/env python

# taken from http://www.md5hashing.com/python/
# slightly modified by Sebastian Moors <mauser@smoors.de>


## md5hash
## 2004-01-30
## Nick Vargish
## md5 hash utility for generating md5 checksums of files. 
## usage: md5hash <filename> [..]
## Use '-' as filename to sum standard input.

import md5
import sys

def sumfile( fobj ):
    '''Returns an md5 hash for an object with read() method.'''
    m = md5.new()
    while True:
        d = fobj.read( 8096 )
        if not d:
            break
        m.update(d)
    return m.hexdigest()


def md5sum( fname ):
    '''Returns md5 of a file, or stdin if fname is "-".'''
    if fname == '-':
        ret = sumfile(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile(f)
        f.close()
    return ret

