#!/usr/bin/env python
# encoding: utf-8
"""
AWSRestRequest.py

Created by Matt Ryan on 2011-06-04.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os
import hmac
import hashlib
import base64


class AWSRestRequest:
	def __init__(self,aws_access_key=os.environ.get('AWS_ACCESS_KEY'),aws_secret_key=os.environ.get('AWS_SECRET_KEY'),secure_http=True,time_offset=0):
		self.aws_access_key = aws_access_key
		self.aws_secret_key = aws_secret_key
		self.secure_http = secure_http
		self.time_offset = time_offset
		if not aws_access_key or not len(aws_access_key):
			raise ValueError, 'AWS Access Key required'
		if not aws_secret_key or not len(aws_secret_key):
			raise ValueError, 'AWS Secret Key required'
	def generate_signature(self,s):
		return base64.b64encode(hmac.new(self.aws_secret_key,s,hashlib.sha1).digest())


if __name__ == '__main__':
	unittest.main()