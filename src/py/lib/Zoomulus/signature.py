#!/usr/bin/env python
# encoding: utf-8
"""
signature.py

Created by Matt Ryan on 2011-07-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

class signature:
	def __init__(self,s):
		self.toBeSigned = s
	def get(self):
		return self.toBeSigned
