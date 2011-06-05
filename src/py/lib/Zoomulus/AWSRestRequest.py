#!/usr/bin/env python
# encoding: utf-8
"""
AWSRestRequest.py

Created by Matt Ryan on 2011-06-04.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import hmac
import hashlib
import base64



class AWSRestRequest:
	def __init__(self,aws_secret_key):
		self.aws_secret_key = aws_secret_key
	def generate_signature(self,s):
		return base64.b64encode(hmac.new(self.aws_secret_key,s,hashlib.sha1).digest())


if __name__ == '__main__':
	unittest.main()