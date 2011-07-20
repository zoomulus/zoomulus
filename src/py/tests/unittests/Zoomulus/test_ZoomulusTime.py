#!/usr/bin/env python
# encoding: utf-8
"""
test_ZoomulusTime.py

Created by Matt Ryan on 2011-07-20.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest
import time

import Zoomulus.ZoomulusTime as zt


class test_ZoomulusTime(unittest.TestCase):
	def setUp(self):
		self.zoomulus_birthdate = (2011,4,5,12,0,0,1,95,0)
	def test_HTTPDate(self):
		ztime = zt.ZoomulusTime(self.zoomulus_birthdate)
		self.assertEquals(ztime.httpdate(),"Tue, 05 Apr 2011 12:00:00 GMT")
	def test_HTTPDateNow(self):
		now = time.time()
		ztime = zt.ZoomulusTime()
		parsed_ztime = time.strptime(ztime.httpdate(),'%a, %d %b %Y %H:%M:%S GMT')
		zt_now = time.mktime(parsed_ztime)
		self.assertTrue((zt_now-now) < 5)

    
if __name__ == '__main__':
	unittest.main()