#!/usr/bin/env python
# encoding: utf-8
"""
path.py

Created by Matt Ryan on 2011-04-06.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os
import urlparse

cloudtypes = ['aws']

def abspath(path):
	pass
	
def basename(path):
	pass
	
def cloudtype(path):
	pass
	
def commonprefix(path):
	pass
	
def dirname(path):
	pass
	
def exists(path):
	pass
	
def expandvars(path):
	pass
	
def getatime(path):
	pass
	
def getmtime(path):
	pass
	
def getsize(path):
	pass
	
def isabs(path):
	pass
	
def iscloudfile(path):
	return cloudtypes.count(urlparse.urlsplit(path)[2]) > 0
	
def isclouddir(path):
	return cloudtypes.count(urlparse.urlsplit(path)[2]) > 0
	
def isfile(path):
	pass
	
def isdir(path):
	pass
	
def islink(path):
	pass
	
def ismount(path):
	pass
	
def join(path,*paths):
	pass
	
def normcase(path):
	pass
	
def normpath(path):
	pass
	
def split(path):
	pass
	
def splitdrive(path):
	pass
	
def splitext(path):
	pass
	
def walk(path,func,arg):
	pass

def main():
	pass


if __name__ == '__main__':
	main()

