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
		self.testuri = 'https://s3.amazonaws.com/mybucket/myobject'
		self.accesskey = 'DUMMY_ACCESS_KEY'
		self.secretkey = 'DUMMY_SECRET_KEY'
		
	# Test driver to try to run without having environment variables set properly.
	def run_test_without_key_data(self,keydataname):
		prev_keydata = None
		try:
			prev_keydata = os.environ[keydataname]
			os.environ[keydataname] = ''
		except KeyError:
			pass
		try:
			req = awsreq.AWSRestRequest('GET',self.testuri)
			self.fail()
		except ValueError:
			pass
		except Exception, e:
			self.fail(e)
		finally:
			if prev_keydata is not None:
				os.environ[keydataname] = prev_keydata
	# Ensure that we don't run without AWS_ACCESS_KEY set.
	def test_init_with_no_access_key(self):
		self.run_test_without_key_data('AWS_ACCESS_KEY')
	# Ensure that we don't run without AWS_SECRET_KEY set.
	def test_init_with_no_secret_key(self):
		self.run_test_without_key_data('AWS_SECRET_KEY')
		
	# Test to verify that the supplied URI will be properly fixed.
	def test_fixuri(self):
		req = awsreq.AWSRestRequest('GET',self.testuri,{},self.accesskey,self.secretkey)
		req.fix_uri()
		self.assertEquals(req.uriparts[0],'https')
		self.assertEquals(req.uriparts[1],'s3.amazonaws.com:443')
		req = awsreq.AWSRestRequest('GET',self.testuri,{},self.accesskey,self.secretkey,False)
		req.fix_uri()
		self.assertEquals(req.uriparts[0],'http')
		self.assertEquals(req.uriparts[1],'s3.amazonaws.com:80')
		
	# Test to verify that the parameter signing works properly
	def test_get_query_params(self):
		req = awsreq.AWSRestRequest('GET',self.testuri,{},self.accesskey,self.secretkey)
		before_params = {'XYZ':'uvw','abc':'def','Jkl':'mNo'}
		after_params = req.get_query_params(before_params)
		self.assertEquals(after_params,'p5PCFp/WG3ipt2cIBXlEhdfRhS8=')

    
if __name__ == '__main__':
	unittest.main()