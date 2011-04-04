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
		lf = LocalFile(self.f[1])
		self.failUnless(lf.IsLocalFile())
		self.assertEquals(str(lf),self.f[1])
		self.failUnless(os.path.exists(str(lf)))
		self.failUnless(os.path.isfile(str(lf)))
		

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
		ld = LocalDir(self.d)
		self.failUnless(ld.IsLocalDir())
		self.assertEquals(str(ld),self.d)
		self.failUnless(os.path.exists(str(ld)))
		self.failUnless(os.path.isdir(str(ld)))
		

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
			self.failUnless(IsCloudPath(spec[0]))
			cf = GetCloudPath(spec[0])
			self.assertEqual(cf.__class__.__name__,'AWSPath')
			self.failUnless(cf.IsCloudPath())
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