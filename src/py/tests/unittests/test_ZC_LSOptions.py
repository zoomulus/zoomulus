#!/usr/bin/env python
# encoding: utf-8
"""
test_ZC_LSOptions.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest
import os

import ZoomulusCommands.options as ZC
import Zoomulus.paths as ZPaths


class test_ZC_LSOptions(unittest.TestCase):
	def setUp(self):
		pass
	def testOption_a(self):
		o = ZC.LSOptions('-a')
		self.assertTrue(o.showHiddenFiles)
	def testOption_c(self):
		o = ZC.LSOptions('-c')
		self.assertEqual('c',o.sortBy)
	def testOption_e(self):
		o = ZC.LSOptions('-e')
		self.assertTrue(o.showACLs)
	def testOption_h(self):
		o = ZC.LSOptions('-h')
		self.assertTrue(o.humanReadable)
	def testOption_l(self):
		o = ZC.LSOptions('-l')
		self.assertTrue(o.longListing)
	def testOption_o(self):
		o = ZC.LSOptions('-o')
		self.assertFalse(o.showGroupInfo)
	def testOption_r(self):
		o = ZC.LSOptions('-r')
		self.assertTrue(o.reverseSort)
	def testOption_R(self):
		o = ZC.LSOptions('-R')
		self.assertTrue(o.recursive)
	def testOption_S(self):
		o = ZC.LSOptions('-S')
		self.assertEquals('S',o.sortBy)
	def testOption_t(self):
		o = ZC.LSOptions('-t')
		self.assertEquals('t',o.sortBy)
	def testOption_T(self):
		o = ZC.LSOptions('-T')
		self.assertTrue(o.showTimeInfo)
	def testOption_u(self):
		o = ZC.LSOptions('-u')
		self.assertEquals('u',o.sortBy)
	def testOption_U(self):
		o = ZC.LSOptions('-U')
		self.assertEquals('U',o.sortBy)
	def testNoArgs(self):
		o = ZC.LSOptions(None)
		self.assertEquals(o.targets[0],ZPaths.LocalDir(os.getcwd()))
	def testEmptyArgs(self):
		o = ZC.LSOptions([])
		self.assertEquals(o.targets[0],ZPaths.LocalDir(os.getcwd()))
	def testLSOneFile(self):
		o = ZC.LSOptions('../testdata/test.txt')
		self.assertEquals(o.targets[0],ZPaths.LocalFile('../testdata/test.txt'))
		self.failIf(o.showFolders)
	def testLSMultipleFiles(self):
		o = ZC.LSOptions(['../testdata/testdir1/td1test.txt',
			'../testdata/testdir2/td2test.txt'])
		self.assertEquals(o.targets[0],ZPaths.LocalFile('../testdata/testdir1/td1test.txt'))
		self.assertEquals(o.targets[1],ZPaths.LocalFile('../testdata/testdir2/td2test.txt'))
		self.failIf(o.showFolders)
	def testLSOneDir(self):
		o = ZC.LSOptions('../testdata')
		self.assertEquals(o.targets[0],ZPaths.LocalDir('../testdata'))
		self.failIf(o.showFolders)
	def testLSMultipleDirs(self):
		o = ZC.LSOptions(['../testdata/testdir1','../testdata/testdir2'])
		self.assertEquals(o.targets[0],ZPaths.LocalDir('../testdata/testdir1'))
		self.assertEquals(o.targets[1],ZPaths.LocalDir('../testdata/testdir2'))
		self.failUnless(o.showFolders)
	def testLSOneAWS(self):
		o = ZC.LSOptions('aws://bucket/test.txt')
		self.assertEqual(o.targets[0],ZPaths.AWSPath('aws://bucket/test.txt'))
		self.failIf(o.showFolders)
	def testLSMultipleAWS(self):
		o = ZC.LSOptions(['aws://bucket/file1','aws://bucket/file2'])
		self.assertEqual(o.targets[0],ZPaths.AWSPath('aws://bucket/file1'))
		self.assertEqual(o.targets[1],ZPaths.AWSPath('aws://bucket/file2'))
		self.failIf(o.showFolders)

    
if __name__ == '__main__':
	unittest.main()