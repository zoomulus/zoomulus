#!/usr/bin/env python
# encoding: utf-8
"""
test_Z_LocalFile.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest
import os
import tempfile

import Zoomulus.paths as ZPaths


class test_Z_LocalFile(unittest.TestCase):
	def setUp(self):
		self.f = tempfile.mkstemp()
		os.close(self.f[0])
	def tearDown(self):
		os.unlink(self.f[1])
	def testFile(self):
		lf = ZPaths.LocalFile(self.f[1])
		self.failUnless(lf.IsLocalFile())
		self.assertEquals(str(lf),self.f[1])
		self.failUnless(os.path.exists(str(lf)))
		self.failUnless(os.path.isfile(str(lf)))

    
if __name__ == '__main__':
	unittest.main()