#!/usr/bin/env python
# encoding: utf-8
"""
test_S3.py

Created by Matt Ryan on 2011-08-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest

import Zoomulus.S3 as S3


class test_S3(unittest.TestCase):
	def setUp(self):
		pass
		
	def test_make_uri(self):
		s3 = S3.S3()
		self.assertEquals('https://s3.amazonaws.com',s3.make_uri())
		self.assertEquals('https://validbucket.s3.amazonaws.com',s3.make_uri('validbucket'))
		self.assertEquals('https://s3.amazonaws.com/invalid_bucket',s3.make_uri('invalid_bucket'))
		self.assertEquals('https://valid.bucket.s3.amazonaws.com/file',s3.make_uri('valid.bucket','file'))
		self.assertEquals('https://s3.amazonaws.com/invalid_bucket/file',s3.make_uri('invalid_bucket','file'))
		self.assertEquals('https://bucket.s3.amazonaws.com?p2=v2&p1=v1',s3.make_uri('bucket','',{'p1':'v1','p2':'v2'}))
		

    
if __name__ == '__main__':
	unittest.main()