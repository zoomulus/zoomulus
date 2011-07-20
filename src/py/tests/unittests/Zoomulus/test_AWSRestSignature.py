#!/usr/bin/env python
# encoding: utf-8
"""
test_AWSRestSignature.py

Created by Matt Ryan on 2011-07-20.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest

import Zoomulus.AWSRestSignature as awssig


class test_AWSRestSignature(unittest.TestCase):
	def setUp(self):
		self.key = 'SomeSecretKey'
		self.basicUri = 'https://s3.amazonaws.com/bucket/object'
		self.queryUri = self.basicUri + '?queryParam=queryValue'
		self.zoomulus_birthdate = (2011,4,5,12,0,0,1,95,0)
		self.headers = {'Content-Type':'text/plain'}
	def test_signEmptyRestGet(self):
		sig = awssig.AWSRestSignature(self.key,'GET',self.basicUri,{},self.zoomulus_birthdate)
		self.assertEquals(sig.get(),'sWUHSbrlXPbmM+aiY3weZYq6g3g=')
	def test_signEmptyRestPut(self):
		sig = awssig.AWSRestSignature(self.key,'PUT',self.basicUri,{},self.zoomulus_birthdate)
		self.assertEquals(sig.get(),'YR9gsEhqhjtGVuwZufA93UXfNro=')
	def test_signRestGetWithHeaders(self):
		sig = awssig.AWSRestSignature(self.key,'GET',self.basicUri,self.headers,self.zoomulus_birthdate)
		self.assertEquals(sig.get(),'76Wg2gCtuMqhbgmV2cIvVY9lfjc=')
	def test_signRestPutWithHeaders(self):
		sig = awssig.AWSRestSignature(self.key,'PUT',self.basicUri,self.headers,self.zoomulus_birthdate)
		self.assertEquals(sig.get(),'z/tJo6Gnj+6lWw6b9dz71K7w0TY=')
	def test_signRestGetWithQuery(self):
		sig = awssig.AWSRestSignature(self.key,'GET',self.queryUri,{},self.zoomulus_birthdate)
		self.assertEquals(sig.get(),'DoWBzEEtdepxvHIvYdiy4dLOu/Y=')
	def test_signRestPutWithQuery(self):
		sig = awssig.AWSRestSignature(self.key,'PUT',self.queryUri,{},self.zoomulus_birthdate)
		self.assertEquals(sig.get(),'REBHDEzyAuLuTRPtqSw8BVt/0Sk=')

    
if __name__ == '__main__':
	unittest.main()