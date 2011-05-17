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
	if iscloudpath(path):
		return path
	return os.path.abspath(path)
	
def basename(path):
	return os.path.basename(path) # works for cloud resources too
	
def cloudtype(path):
	return urlparse.urlsplit(path)[0]
	
def commonprefix(path):
	return os.path.commonprefix(path)
	
def dirname(path):
	return os.path.dirname(path) # works for cloud resources too
	
def exists(path):
	if iscloudpath(path):
		return False
	return os.path.exists(path)
	
def expandvars(path):
	return os.path.expandvars(path)
	
def getatime(path):
	if iscloudpath(path):
		return False
	return os.path.getatime(path)
	
def getmtime(path):
	if iscloudpath(path):
		return False
	return os.path.getmtime(path)
	
def getsize(path):
	if iscloudpath(path):
		return False
	return os.path.getsize(path)
	
def isabs(path):
	if iscloudpath(path):
		return len(basename(path)) > 0
	return os.path.isabs(path)
	
def iscloudpath(path):
	return cloudtypes.count(cloudtype(path)) > 0
	
def iscloudfile(path):
	return iscloudpath(path)
	
def isclouddir(path):
	return iscloudpath(path)
	
def isfile(path):
	if iscloudpath(path):
		return False
	return os.path.isfile(path)
	
def isdir(path):
	if iscloudpath(path):
		return False
	return os.path.isdir(path)
	
def islink(path):
	if iscloudpath(path):
		return False
	return os.path.islink(path)
	
def ismount(path):
	if iscloudpath(path):
		return False
	return os.path.ismount(path)
	
def join(path,*paths):
	ctr = 0
	for p in paths:
		if iscloudpath(p) or p.startswith('/'):
			remainingpaths = paths[ctr:]
			if len(remainingpaths) == 1:
				return remainingpaths[0]
			elif len(remainingpaths) == 2:
				return join(remainingpaths[0],remainingpaths[1])
			elif len(remainingpaths) > 2:
				return join(remainingpaths[0],*remainingpaths[1:])
		else:
			if not path.endswith('/'):
				path = path + '/'
			path = path + p
		ctr = ctr + 1
	return path
	
def normcase(path):
	if iscloudpath(path):
		return path
	return os.path.normcase(path)
	
def normpath(path):
	if iscloudpath(path):
		parts = split(path)
		p = os.path.normpath(join(parts[1],parts[2])).replace('\\','/')
		return parts[0] + ':/' + p
	return os.path.normpath(path)
	
def split(path):
	if iscloudpath(path):
		parts = urlparse.urlsplit(path)
		p = parts[2]
		if p.startswith('//'):
			p = p[1:]
		return (parts[0], dirname(p), basename(p))
	return os.path.split(path)
	
def splitdrive(path):
	return os.path.splitdrive(path) # works with cloud resources too
	
def splitext(path):
	return os.path.splitext(path) # works with cloud resources too
	
def walk(path,func,arg):
	if iscloudpath(path):
		return False
	return os.path.watlk(path,func,arg)

def main():
	pass


if __name__ == '__main__':
	main()

