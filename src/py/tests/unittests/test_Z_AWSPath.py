#!/usr/bin/env python
# encoding: utf-8
"""
test_Z_AWSPath.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest

import Zoomulus.paths as ZPaths


class test_Z_AWSPath(unittest.TestCase):
	def setUp(self):
		self.s3Files = []
		self.s3Files.append(('aws://','aws',None,None,'aws://'))
		self.s3Files.append(('aws://bucketname','aws','bucketname',None,'aws://bucketname/'))
		self.s3Files.append(('aws://bucketname/','aws','bucketname',None,'aws://bucketname/'))
		self.s3Files.append(('aws://bucketname/file','aws','bucketname','file','aws://bucketname/file'))
		self.s3Files.append(('aws://bucketname/path/to/file','aws','bucketname','path/to/file','aws://bucketname/path/to/file'))
	def testS3Files(self):
		for spec in self.s3Files:
			self.failUnless(ZPaths.IsCloudPath(spec[0]))
			cf = ZPaths.GetCloudPath(spec[0])
			self.assertEqual(cf.__class__.__name__,'AWSPath')
			self.failUnless(cf.IsCloudPath())
			self.assertEqual(cf.cloudType,spec[1])
			self.assertEqual(cf.bucket,spec[2])
			self.assertEqual(cf.path,spec[3])
			self.assertEqual(str(cf),spec[4])
	def testToStr(self):
		path = 'aws://bucketname/path/to/file.txt'
		f = ZPaths.AWSPath(path)
		self.assertEquals(str(f),path)

    
if __name__ == '__main__':
	unittest.main()