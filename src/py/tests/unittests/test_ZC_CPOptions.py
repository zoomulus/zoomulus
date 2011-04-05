#!/usr/bin/env python
# encoding: utf-8
"""
test_ZC_CPOptions.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest

import ZoomulusCommands.options as ZC
import Zoomulus.paths as ZPaths


class test_ZC_CPOptions(unittest.TestCase):
	def setUp(self):
		self.fArgs = ['/path/to/f1','/path/to/f2']
	def argsTest(self,a):
		strargs = []
		for ent in a:
			strargs.append(str(ent))
		o = ZC.CPOptions(strargs)
		self.assertEquals(len(o.sources),len(a)-1)
		for i in xrange(0,len(a)-2):
			self.assertEquals(o.sources[i],a[i])
		self.assertEquals(o.target,a[len(a)-1])
	def argsTestException(self,a):
		ueThrown = False
		try:
			strargs = []
			for ent in a:
				strargs.append(str(ent))
			o = ZC.CPOptions(strargs)
		except ZC.UsageException:
			ueThrown = True
		self.assertTrue(ueThrown)

	def testOption_a(self):
		o = ZC.CPOptions(['-a','../testdata/testdir1','../testdata/testdir2'])
		self.assertTrue(o.preserveFileStatistics)
		self.assertTrue(o.recursiveCopy)
		self.assertFalse(o.followSymLinks)
	def testOption_f(self):
		o = ZC.CPOptions(['-f']+self.fArgs)
		self.assertEquals('f',o.overwriteMode)
	def testOption_i(self):
		o = ZC.CPOptions(['-i']+self.fArgs)
		self.assertEquals('i',o.overwriteMode)
	def testOption_n(self):
		o = ZC.CPOptions(['-n']+self.fArgs)
		self.assertEquals('n',o.overwriteMode)
	def testOption_p(self):
		o = ZC.CPOptions(['-p']+self.fArgs)
		self.assertTrue(o.preserveFileStatistics)
	def testOption_P(self):
		o = ZC.CPOptions(['-P']+self.fArgs)
		self.assertFalse(o.followSymLinks)
	def testOption_R(self):
		o = ZC.CPOptions(['-R','../testdata/testdir1','../testdata/testdir2'])
		self.assertTrue(o.recursiveCopy)
	def testOption_v(self):
		o = ZC.CPOptions(['-v']+self.fArgs)
		self.assertTrue(o.beVerbose)
	def testCopyFileToFile(self):
		self.argsTest([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.LocalFile('../testdata/test2.txt')])
	def testCopyFileToDir(self):
		self.argsTest([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.LocalDir('../testdata/testdir1')])
	def testCopyFileToAWSFile(self):
		self.argsTest([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.AWSPath('aws://bucket/test.txt')])
	def testCopyFileToAWSBucket(self):
		self.argsTest([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyDirToFile(self):
		self.argsTestException([ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalFile('../testdata/test.txt')])
	def testCopyDirToDir(self):
		self.argsTest([ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir2')])
	def testCopyDirToAWSFile(self):
		self.argsTest([ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.AWSPath('aws://bucket/test.txt')])
	def testCopyDirToAWSBucket(self):
		self.argsTest([ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyAWSToFile(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.LocalFile('../testdata/test.txt')])
	def testCopyAWSToDir(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.LocalDir('../testdata/testdir1')])
	def testCopyAWSToAWS(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.AWSPath('aws://bucket/test2.txt')])
	def testCopyFileToSelf(self):
		f = ZPaths.LocalFile('../testdata/test.txt')
		self.argsTestException([f,f])
	def testCopyFileToSame(self):
		self.argsTestException([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.LocalFile('../testdata/test.txt')])
	def testCopyDirToSelf(self):
		d = ZPaths.LocalDir('../testdata/testdir1')
		self.argsTestException([d,d])
	def testCopyDirToSame(self):
		self.argsTestException([ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir1')])
	def testCopyAWSToSelf(self):
		c = ZPaths.AWSPath('aws://bucket/test.txt')
		self.argsTestException([c,c])
	def testCopyAWSToSame(self):
		self.argsTestException([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.AWSPath('aws://bucket/test.txt')])
	def testCopyFilesToFile(self):
		self.argsTestException([ZPaths.LocalFile('../testdata/testdir1/td1test.txt'),
			ZPaths.LocalFile('../testdata/testdir2/td2test.txt'),
			ZPaths.LocalFile('../testdata/test.txt')])
	def testCopyFilesToDir(self):
		self.argsTest([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.LocalFile('../testdata/testdir1/td1test.txt'),
			ZPaths.LocalDir('../testdata/testdir2')])
	def testCopyFilesToAWS(self):
		self.argsTest([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.LocalFile('../testdata/testdir1/td1test.txt'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyDirsToFile(self):
		self.argsTestException([ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir2'),
			ZPaths.LocalFile('../testdata/test.txt')])
	def testCopyDirsToDir(self):
		self.argsTest([ZPaths.LocalDir('../testdata'),
			ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir2')])
	def testCopyDirsToAWS(self):
		self.argsTest([ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir2'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyAWSsToFile(self):
		self.argsTestException([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.LocalFile('../testdata/test.txt')])
	def testCopyAWSsToDir(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.LocalDir('../testdata')])
	def testCopyAWSsToAWS(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.AWSPath('aws://bucket/dir1')])
	def testCopyFilesToDirWithDuplicateSources(self):
		self.argsTest([ZPaths.LocalFile('../testdata/test.txt'),
			ZPaths.LocalFile('../testdata/testdir1/td1test.txt'),
			ZPaths.LocalFile('../testdata/testdir1/td1test.txt'),
			ZPaths.LocalDir('../testdata/testdir2')])
	def testCopyDirsToSelf(self):
		self.argsTestException([ZPaths.LocalDir('../testdata'),
			ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir2'),
			ZPaths.LocalDir('../testdata/testdir2')])
	def testCopyDirsToDirWithDuplicateSources(self):
		self.argsTest([ZPaths.LocalDir('../testdata'),
			ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir1'),
			ZPaths.LocalDir('../testdata/testdir2')])
	def testCopyAWSsToDirWithDuplicateSources(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.LocalDir('../testdata')])
	def testCopyAWSsToSelf(self):
		self.argsTestException([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.AWSPath('aws://bucket/file1')])

    
if __name__ == '__main__':
	unittest.main()