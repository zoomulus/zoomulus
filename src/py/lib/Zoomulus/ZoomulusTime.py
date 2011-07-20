#!/usr/bin/env python
# encoding: utf-8
"""
ZoomulusTime.py

Created by Matt Ryan on 2011-07-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import time

class ZoomulusTime:
	def __init__(self,now=time.localtime(time.time())):
		self.now = now
	def httpdate(self):
		return time.strftime('%a, %d %b %Y %H:%M:%S GMT',self.now)
