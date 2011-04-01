#!/usr/bin/env python
# encoding: utf-8
"""
paths.py

Created by Matt Ryan on 2011-02-17.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os
import unittest
import tempfile
import urlparse


class InvalidPathException(Exception):
	def __init__(self,path):
		Exception.__init__(self,path + " doesn't seem to be a valid path")



class FileResource:
	def GetFile(uri):
		fragments = urlparse.urlsplit(uri)
		scheme = fragments[0]
		path = fragments[2]
		
		if scheme == 'aws':
			return AWSPath(path)
			
		if len(scheme):
			path = scheme + ':' + path
			
		if os.path.isfile(path):
			return LocalFile(path)
		elif os.path.isdir(path):
			return LocalDir(path)
		raise InvalidPathException, path
	GetFile = staticmethod(GetFile)
		
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
		
class FileResourceTests(unittest.TestCase):
	def setUp(self):
		pass
		

class LocalFile(FileResource):
	def __init__(self,path):
		if os.path.exists(path) and not os.path.isfile(path):
			raise InvalidPathException, path
		dname, self.filename = os.path.split(path)
		FileResource.__init__(self,dname)
	def __str__(self):
		return self.path+'/'+self.filename
		
class LocalFileTests(unittest.TestCase):
	def setUp(self):
		self.f = tempfile.mkstemp()
		os.close(self.f[0])
	def tearDown(self):
		os.unlink(self.f[1])
	def testFile(self):
		lf = FileResource.GetFile(self.f[1])
		self.assertEqual(lf.__class__.__name__,'LocalFile')
		

class LocalDir(FileResource):
	def __init__(self,path):
		if os.path.exists(path) and not os.path.isdir(path):
			raise InvalidPathException, path
		FileResource.__init__(self,path)
		
class LocalFolderTests(unittest.TestCase):
	def setUp(self):
		self.d = tempfile.mkdtemp()
	def tearDown(self):
		os.rmdir(self.d)
	def testDir(self):
		ld = FileResource.GetFile(self.d)
		self.assertEqual(ld.__class__.__name__,'LocalDir')
		

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
		
class CloudPathTests(unittest.TestCase):
	def setUp(self):
		pass
		

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
		
class AWSPathTests(unittest.TestCase):
	def setUp(self):
		self.s3Files = []
		self.s3Files.append(('aws://','aws',None,None,'aws://'))
		self.s3Files.append(('aws://bucketname','aws','bucketname',None,'aws://bucketname/'))
		self.s3Files.append(('aws://bucketname/','aws','bucketname',None,'aws://bucketname/'))
		self.s3Files.append(('aws://bucketname/file','aws','bucketname','file','aws://bucketname/file'))
		self.s3Files.append(('aws://bucketname/path/to/file','aws','bucketname','path/to/file','aws://bucketname/path/to/file'))
	def testS3Files(self):
		for spec in self.s3Files:
			cf = FileResource.GetFile(spec[0])
			self.assertEqual(cf.__class__.__name__,'AWSPath')
			self.assertEqual(cf.cloudType,spec[1])
			self.assertEqual(cf.bucket,spec[2])
			self.assertEqual(cf.path,spec[3])
			self.assertEqual(str(cf),spec[4])
	def testToStr(self):
		path = 'aws://bucketname/path/to/file.txt'
		f = AWSPath(path)
		self.assertEquals(str(f),path)
		



if __name__ == '__main__':
	unittest.main()