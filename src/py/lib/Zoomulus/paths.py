#!/usr/bin/env python
# encoding: utf-8
"""
paths.py

Created by Matt Ryan on 2011-02-17.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os
import urlparse


class InvalidPathException(Exception):
	def __init__(self,path):
		Exception.__init__(self,path + " doesn't seem to be a valid path")



class FileResource:
	def __init__(self,path):
		self.path = path
	def __str__(self):
		return self.path
	def __eq__(self,rhs):
		return str(self)==str(rhs)
	def IsLocalFile(self):
		return self.__class__.__name__ == 'LocalFile'
	def IsLocalDir(self):
		return self.__class__.__name__ == 'LocalDir'
	def IsCloudPath(self):
		rv = False
		for b in self.__class__.__bases__:
			if b.__name__ == 'CloudPath':
				rv = True
				break
		return rv
		

class LocalFile(FileResource):
	def __init__(self,path):
		if os.path.exists(path) and not os.path.isfile(path):
			raise InvalidPathException, path
		dname, self.filename = os.path.split(path)
		FileResource.__init__(self,dname)
	def __str__(self):
		return self.path+'/'+self.filename
				

class LocalDir(FileResource):
	def __init__(self,path):
		if os.path.exists(path) and not os.path.isdir(path):
			raise InvalidPathException, path
		FileResource.__init__(self,path)
		

def IsCloudPath(uri):
	return GetCloudPath(uri) is not None

def GetCloudPath(uri):
	cType = urlparse.urlsplit(uri)[0]
	if cType == 'aws':
		return AWSPath(uri)
	return None

class CloudPath(FileResource):
	def __init__(self,cloudtype,path):
		self.cloudType = cloudtype
		FileResource.__init__(self,path)
				

class AWSPath(CloudPath):
	def __init__(self,path):
		CloudPath.__init__(self,'aws',urlparse.urlsplit(path)[2])
		self.path = self.path.lstrip('/')
		if len(self.path) > 0:
			try:
				self.bucket, self.path = self.path.split('/',1)
				if len(self.path) <= 0:
					self.path = None
			except ValueError:
				self.bucket = self.path
				self.path = None
		else:
			self.bucket = None
			self.path = None
	def __str__(self):
		rv = 'aws://'
		if self.bucket is not None:
			rv += self.bucket + '/'
		if self.path is not None:
			rv += self.path
		return rv
