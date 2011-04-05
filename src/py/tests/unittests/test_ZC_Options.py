#!/usr/bin/env python
# encoding: utf-8
"""
test_ZC_Options.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import unittest

import ZoomulusCommands.options as ZC


class test_ZC_Options(unittest.TestCase):
	def setUp(self):
		pass
	def testOption_v(self):
		o = ZC.Options('-v')
		self.assertTrue(o.beVerbose)
	def testOption_help(self):
		try:
			o = ZC.Options('--help')
			self.fail()
		except ZC.UsageException:
			pass
		except Exception:
			self.fail()

    
if __name__ == '__main__':
	unittest.main()