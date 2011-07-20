#!/usr/bin/env python
# encoding: utf-8
"""
AWSSignature.py

Created by Matt Ryan on 2011-07-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import hmac
import hashlib
import base64

import signature as sig

class AWSSignature(sig.signature):
	def __init__(self,s,aws_secret_key):
		sig.signature.__init__(self,s)
		self.aws_secret_key = aws_secret_key
	def get(self):
		return base64.b64encode(hmac.new(self.aws_secret_key,self.toBeSigned,hashlib.sha1).digest())
		
