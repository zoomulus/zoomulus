#!/usr/bin/env python
# encoding: utf-8
"""
test_AWSSignature.py

Created by Matt Ryan on 2011-07-20.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest

import Zoomulus.AWSSignature as awssig


class test_AWSSignature(unittest.TestCase):
	def setUp(self):
		pass
	def test_generateSignature(self):
		key = 'SomeSecretKey'
		s = 'RandomStringToBeSigned'
		sigObj = awssig.AWSSignature(s,key)
		expected = 'U6CjMHXDy5CLeJOdpxEngYd+m5Q='
		self.assertEquals(sigObj.get(),expected)

    
if __name__ == '__main__':
	unittest.main()