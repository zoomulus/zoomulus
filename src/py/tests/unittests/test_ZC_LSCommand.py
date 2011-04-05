#!/usr/bin/env python
# encoding: utf-8
"""
test_ZC_LSCommand.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest

from ZoomulusCommands.LSOptions import LSOptions
from ZoomulusCommands.LSCommand import LSCommand


class test_ZC_LSCommand(unittest.TestCase):
	def setUp(self):
		pass
	def test_Construct(self):
		o = LSOptions(None)
		self.assertTrue(o is not None)
		cmd = LSCommand(o)
		self.assertTrue(cmd is not None)
		self.assertTrue(cmd.IsLSCommand())

    
if __name__ == '__main__':
	unittest.main()