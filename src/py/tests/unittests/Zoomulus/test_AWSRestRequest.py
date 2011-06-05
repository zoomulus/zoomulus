#!/usr/bin/env python
# encoding: utf-8
"""
test_AWSRestRequest.py

Created by Matt Ryan on 2011-06-04.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest

import Zoomulus.AWSRestRequest as awsreq


class test_AWSRestRequest(unittest.TestCase):
	def setUp(self):
		pass
	def test_generate_signature(self):
		req = awsreq.AWSRestRequest('MySecretKey')
		self.assertEquals(req.generate_signature('FakeRequestDescription'),'wZs+py3LaQiMBOmpy0zSYD5nHC0=')

    
if __name__ == '__main__':
	unittest.main()