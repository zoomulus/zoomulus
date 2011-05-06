#!/usr/bin/env python
# encoding: utf-8
"""
test_Z_path.py

Created by Matt Ryan on 2011-05-06.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest
import os

import Zoomulus as z


class test_Z_path(unittest.TestCase):
	def setUp(self):
		self.awsFiles=['aws://bucket','aws://bucket/file','aws://bucket/path/to/file']
		
	def test_awsCloudType(self):
		for awsFile in self.awsFiles:
			self.assertEquals('aws',z.path.cloudtype(awsFile))
		self.assertEquals('fake',z.path.cloudtype('fake://cloudfile'))
		self.assertEquals('',z.path.cloudtype(os.getcwd()))
		
	def test_localFileAbsPath(self):
		self.assertEquals(os.getcwd(),z.path.abspath(os.getcwd()))
		
	def test_awsFileAbsPath(self):
		for awsFile in self.awsFiles:
			self.assertEquals(awsFile,z.path.abspath(awsFile))
			
	def test_awsFileBasename(self):
		self.assertEquals('file',z.path.basename(self.awsFiles[1]))
		
	def test_awsFileDirname(self):
		self.assertEquals('aws://bucket',z.path.dirname(self.awsFiles[1]))
		
	def test_localFileIsAbs(self):
		self.assertTrue(z.path.isabs(os.getcwd()))
		
	def test_awsFileIsAbs(self):
		for awsFile in self.awsFiles:
			self.assertTrue(z.path.isabs(awsFile))

	def test_localPathIsNotCloudPath(self):
		self.failIf(z.path.iscloudpath(os.getcwd()))

	def test_awsFileIsCloudPath(self):
		for awsFile in self.awsFiles:
			self.assertTrue(z.path.iscloudpath(awsFile))

	def test_localFileIsNotCloudFile(self):
		self.failIf(z.path.iscloudfile(os.getcwd()))

	def test_awsFileIsCloudFile(self):
		for awsFile in self.awsFiles:
			self.assertTrue(z.path.iscloudfile(awsFile))

	def test_localDirIsNotCloudDir(self):
		self.failIf(z.path.isclouddir(os.getcwd()))

	def test_awsDirIsCloudDir(self):
		for awsFile in self.awsFiles:
			self.assertTrue(z.path.isclouddir(awsFile))
			
	def test_awsFileIsNotFile(self):
		for awsFile in self.awsFiles:
			self.failIf(z.path.isfile(awsFile))
			
	def test_awsDirIsNotDir(self):
		for awsFile in self.awsFiles:
			self.failIf(z.path.isdir(awsFile))
			
	def test_awsFileIsNotLink(self):
		for awsFile in self.awsFiles:
			self.failIf(z.path.islink(awsFile))
			
	def test_awsFileIsNotMount(self):
		for awsFile in self.awsFiles:
			self.failIf(z.path.ismount(awsFile))
			
	def test_localFileSplit(self):
		parts = z.path.split('/td1/td2/td3/test.txt')
		self.assertEquals('/td1/td2/td3',parts[0])
		self.assertEquals('test.txt',parts[1])
		
	def test_awsFileSplit(self):
		parts = z.path.split('aws://bucket/path/to/file')
		self.assertEquals('aws',parts[0])
		self.assertEquals('//bucket/path/to',parts[1])
		self.assertEquals('file',parts[2])
		
	def test_awsFileSplitDrive(self):
		for awsFile in self.awsFiles:
			parts = z.path.splitdrive(awsFile)
			self.assertEquals('',parts[0])
			self.assertEquals(awsFile,parts[1])
			
	def test_awsFileSplitExt(self):
		for awsFile in self.awsFiles:
			parts = z.path.splitext(awsFile)
			self.assertEquals(awsFile,parts[0])
			self.assertEquals('',parts[1])
		parts = z.path.splitext('aws://bucket/path/to/file.txt')
		self.assertEquals('aws://bucket/path/to/file',parts[0])
		self.assertEquals('.txt',parts[1])

    
if __name__ == '__main__':
	unittest.main()