#!/usr/bin/env python
# encoding: utf-8
"""
test_ZC_CPCommand.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest

from ZoomulusCommands.CPOptions import CPOptions
from ZoomulusCommands.CPCommand import CPCommand


class test_ZC_CPCommand(unittest.TestCase):
	def setUp(self):
		pass
	def test_Construct(self):
		o = CPOptions(['../testdata/test.txt','../testdata/testdir1'])
		self.assertTrue(o is not None)
		cmd = CPCommand(o)
		self.assertTrue(cmd is not None)

    
if __name__ == '__main__':
	unittest.main()