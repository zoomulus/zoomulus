#!/usr/bin/env python
# encoding: utf-8
"""
AWSRestSignature.py

Created by Matt Ryan on 2011-07-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import time
import urlparse

import AWSSignature as awssig
import ZoomulusTime as zTime

class AWSRestSignature(awssig.AWSSignature):
	def __init__(self,aws_secret_key,method,uri,headers,time=time.gmtime()):
		ztime = zTime.ZoomulusTime(time)
		if not headers.has_key('Date'):
			headers['Date'] = ztime.httpdate()
		req_desc = []
		req_desc.append(method)
		req_desc.append('')
		req_desc.append('')
		if headers.has_key('Content-MD5'):
			req_desc.append(headers.get('Content-MD5'))
		if headers.has_key('Content-Type'):
			req_desc.append(headers.get('Content-Type'))
		req_desc.append(headers.get('Date'))
		amzhdrs = []
		for k in headers.keys():
			if k.startswith('x-amz-'):
				amzhdrs.append('%s:%s' % k.lower(),v)
		amzhdrs.sort()
		req_desc.extend(amzhdrs)
		uriparts = urlparse.urlsplit(uri)
		uristr = uriparts[2]
		if len(uriparts[3]):
			uristr += "?" + uriparts[3]
		req_desc.append(uristr)
		awssig.AWSSignature.__init__(self,'\n'.join(req_desc),aws_secret_key)
		
