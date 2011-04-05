#!/usr/bin/env python
# encoding: utf-8
"""
test_Z_LocalDir.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest
import os
import tempfile

import Zoomulus.paths as ZPaths


class test_Z_LocalDir(unittest.TestCase):
	def setUp(self):
		self.d = tempfile.mkdtemp()
	def tearDown(self):
		os.rmdir(self.d)
	def testDir(self):
		ld = ZPaths.LocalDir(self.d)
		self.failUnless(ld.IsLocalDir())
		self.assertEquals(str(ld),self.d)
		self.failUnless(os.path.exists(str(ld)))
		self.failUnless(os.path.isdir(str(ld)))

    
if __name__ == '__main__':
	unittest.main()