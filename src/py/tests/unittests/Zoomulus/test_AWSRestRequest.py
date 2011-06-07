#!/usr/bin/env python
# encoding: utf-8
"""
test_AWSRestRequest.py

Created by Matt Ryan on 2011-06-04.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import os
import unittest

import Zoomulus.AWSRestRequest as awsreq


class test_AWSRestRequest(unittest.TestCase):
	def setUp(self):
		pass
	def run_test_without_key_data(self,keydataname):
		prev_keydata = None
		try:
			prev_keydata = os.environ[keydataname]
			os.environ[keydataname] = ''
		except KeyError:
			pass
		try:
			req = awsreq.AWSRestRequest()
			self.fail()
		except ValueError:
			pass
		except Exception:
			self.fail()
		finally:
			if prev_keydata is not None:
				os.environ[keydataname] = prev_keydata
	def test_init_with_no_access_key(self):
		self.run_test_without_key_data('AWS_ACCESS_KEY')
	def test_init_with_no_secret_key(self):
		self.run_test_without_key_data('AWS_SECRET_KEY')
	def test_generate_signature(self):
		req = awsreq.AWSRestRequest('DummyAccessKey','MySecretKey')
		self.assertEquals(req.generate_signature('FakeRequestDescription'),'wZs+py3LaQiMBOmpy0zSYD5nHC0=')

    
if __name__ == '__main__':
	unittest.main()