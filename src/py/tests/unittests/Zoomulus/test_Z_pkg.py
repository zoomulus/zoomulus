#!/usr/bin/env python
# encoding: utf-8
"""
test_Z_pkg.py

Created by Matt Ryan on 2011-04-06.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest
import os
import random
import time

import Zoomulus as z

def randomstring(size):
	random.seed(time.time())
	s=''
	for i in xrange(size):
		s += chr(random.randrange(97,123,1))
	return s
	
def fakefile(path):
	while(True):
		f = os.path.join(path,randomstring(20))
		if not os.path.exists(f):
			return f
			
def clearpath(path):
	if os.path.isdir(path):
		for ent in os.listdir(path):
			clearpath(os.path.join(path,ent))
		os.rmdir(path)
	else:
		os.unlink(path)

class test_Z_pkg(unittest.TestCase):
	def __init__(self,x):
		self.testdir = '../../testdata/td'
		if os.path.exists(self.testdir):
			clearpath(self.testdir)
		os.mkdir(self.testdir)
		unittest.TestCase.__init__(self,x)
	def __del__(self):
		if os.path.exists(self.testdir):
			clearpath(self.testdir)
	def test_accessLocalFile(self):
		p = '../../testdata/test.txt'
		for accesstype in [os.F_OK, os.R_OK, os.W_OK, os.X_OK]:
			zAccess = z.access(p,accesstype)
			osAccess = os.access(p,accesstype)
			self.assertEquals(zAccess,osAccess)
	def test_accessLocalDir(self):
		p = '../../testdata'
		for accesstype in [os.F_OK, os.R_OK, os.W_OK, os.X_OK]:
			zAccess = z.access(p,accesstype)
			osAccess = os.access(p,accesstype)
			self.assertEquals(zAccess,osAccess)
#	def test_accessAWSFile(self):
#		pass
#	def test_accessAWSDir(self):
#		pass
#	def test_accessAWSBucket(self):
#		pass

	def test_createLocalFile(self):
		p = None
		fd = None
		try:
			p = fakefile(self.testdir)
			fd = z.open(p,os.O_RDWR|os.O_CREAT|os.O_EXCL)
		finally:
			try:
				if fd is not None:
					os.close(fd)
			except Exception:
				self.fail()
		self.assertTrue(os.path.exists(p))
		self.assertTrue(os.path.isfile(p))
		clearpath(p)
		self.failIf(os.path.exists(p))
#	def test_createAWSFile(self):
#		pass

	def test_removeLocalFile(self):
		fd = None
		try:
			p = fakefile(self.testdir)
			fd = os.open(p,os.O_RDWR|os.O_CREAT|os.O_EXCL)
		finally:
			try:
				if fd is not None:
					os.close(fd)
			except Exception:
				self.fail()
		self.assertTrue(os.path.exists(p))
		self.assertTrue(os.path.isfile(p))
		try:
			z.remove(p)
		except OSError:
			self.fail()
		self.failIf(os.path.exists(p))
#	def test_removeAWSFile(self):
#		pass

	def test_createLocalDir(self):
		try:
			p = fakefile(self.testdir)
			z.mkdir(p)
		except OSError:
			self.fail()
		self.assertTrue(os.path.exists(p))
		self.assertTrue(os.path.isdir(p))
		clearpath(p)
		self.failIf(os.path.exists(p))
#	def test_createAWSDir(self):
#		pass

	def test_createLocalDirs(self):
		try:
			p1 = fakefile(self.testdir)
			p2 = fakefile(p1)
			p3 = fakefile(p2)
			p4 = fakefile(p3)
			z.makedirs(p4)
		except OSError:
			self.fail()
		self.assertTrue(os.path.exists(p4))
		self.assertTrue(os.path.isdir(p4))
		clearpath(p1)
		self.failIf(os.path.exists(p1))
#	def test_createAWSDirs(self):
#		pass
		
	def test_removeLocalDir(self):
		try:
			p = fakefile(self.testdir)
			os.mkdir(p)
		except OSError:
			self.fail()
		self.assertTrue(os.path.exists(p))
		self.assertTrue(os.path.isdir(p))
		try:
			z.rmdir(p)
		except OSError:
			self.fail()
		direxists = os.path.exists(p)
		if direxists:
			clearpath(p)
		self.failIf(direxists)
		self.failIf(os.path.exists(p))
#	def test_removeAWSDir(self):
#		pass

	def test_removeLocalDirs(self):
		cwd = os.getcwd()
		try:
			os.chdir(self.testdir)
			p1 = fakefile('')
			p2 = fakefile(p1)
			p3 = fakefile(p2)
			p4 = fakefile(p3)
			os.makedirs(p4)
		except OSError:
			self.fail()
		finally:
			os.chdir(cwd)
		os.chdir(self.testdir)
		self.assertTrue(os.path.exists(p4))
		self.assertTrue(os.path.isdir(p4))
		try:
			z.removedirs(p4)
			direxists = os.path.exists(p4)
			if direxists:
				clearpath(p1)
		except OSError:
			self.fail()
		finally:
			os.chdir(cwd)
		self.failIf(direxists)
		self.failIf(os.path.exists(p1))
#	def test_removeAWSDirs(self):
#		pass

	def test_renameLocalFile(self):
		source = fakefile(self.testdir)
		dest = fakefile(self.testdir)
		self.doRenameTest(source,dest,z.rename)
	def test_renamesLocalFile(self):
		source = fakefile(self.testdir)
		dest = fakefile(fakefile(fakefile(self.testdir)))
		self.doRenameTest(source,dest,z.renames)
	def doRenameTest(self,source,dest,f):
		fd = None
		try:
			fd = os.open(source,os.O_RDWR|os.O_CREAT|os.O_EXCL)
		finally:
			try:
				if fd is not None:
					os.close(fd)
			except Exception:
				self.fail()
		self.assertTrue(os.path.exists(source))
		self.assertTrue(os.path.isfile(source))
		try:
			f(source,dest)
		except Exception:
			self.fail()
		self.assertTrue(os.path.exists(dest))
		self.assertTrue(os.path.isfile(dest))
		self.failIf(os.path.exists(source))
#	def test_renameAWSFile(self):
#		pass

	def test_listLocalDir(self):
		files = []
		for i in xrange(1,10):
			p = fakefile(self.testdir)
			fd = None
			try:
				fd = os.open(p,os.O_RDWR|os.O_CREAT|os.O_EXCL)
				files.append(p)
			finally:
				try:
					if fd is not None:
						os.close(fd)
				except Exception:
					self.fail()
		for p in files:
			self.assertTrue(os.path.exists(p))
			self.assertTrue(os.path.isfile(p))
		for f in z.listdir(self.testdir):
			p = os.path.join(self.testdir,f)
			self.assertTrue(files.count(p)==1)
#	def test_listAWSDir(self):
#		pass

if __name__ == '__main__':
	unittest.main()