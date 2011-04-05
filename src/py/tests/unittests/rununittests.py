#!/usr/bin/env python
# encoding: utf-8
"""
rununittests.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os

class TestFailedException(Exception):
	def init(self,f):
		self.msg = 'Test failed (script: '+f+')'

def RunTestsIn(directory):
	for f in os.listdir(directory):
		if os.path.isdir(f):
			RunTestsIn(f)
		elif os.path.isfile(f) and f.startswith('test_') and f.endswith('.py'):
			print '\nRunning test script',f,':'
			if 0 != os.system('python ' + f):
				raise TestFailedException,f

def main():
	RunTestsIn(os.getcwd())
	print '\nALL TESTS PASSED'


if __name__ == '__main__':
	main()

