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
import time
import urlparse
import urllib

import AWSSignature

class AWSRestRequest:
	# Initialize an AWS Rest Request object.
	def __init__(self,method,uri,headers={},aws_access_key=os.environ.get('AWS_ACCESS_KEY'),aws_secret_key=os.environ.get('AWS_SECRET_KEY'),secure_http=True,time_offset=0):
		if ['GET','HEAD','PUT','DELETE'].count(method) == 0:
			raise ValueError, 'Method must be one of GET, HEAD, PUT, or DELETE'
		self.method = method
		if len(uri) == 0:
			raise ValueError, 'URI must not be empty'
		self.uriparts = urlparse.urlsplit(uri)
		if len(self.uriparts) != 5:
			raise ValueError, '%s is not a valid URI' % uri
		self.headers = headers
		if not aws_access_key or not len(aws_access_key):
			raise ValueError, 'AWS Access Key required'
		self.aws_access_key = aws_access_key
		if not aws_secret_key or not len(aws_secret_key):
			raise ValueError, 'AWS Secret Key required'
		self.aws_secret_key = aws_secret_key
		self.secure_http = secure_http
		self.time_offset = time_offset
	
	# Adds a single key-value pair to this request's headers.	
	def add_header(self,key,val):
		self.headers[key] = val
		
	# Adds all the key-value pairs in a dictionary to this request's headers.
	def add_headers(self,headers):
		self.headers.update(headers)
			
	# Prepares and sends a Rest request based on the object parameters.		
	def request(self):
		awssig = AWSRestSignature(self.aws_secret_key,self.method,self.uri,self.headers)
		headers['Authorization'] = 'AWS %s:%s' % self.aws_access_key, awssig.get()
		headers['Host'] = self.uriparts[1]
		if self.method == 'PUT':
			headers['Expect'] = '100-continue'
			
		current_uriparts = self.uriparts
		redirects = 0
		while redirects < 5:
			httpconn = self.create_HTTP_connection()
			pdata = data
			if method == 'PUT' and os.path.isfile(data):
				f = os.open(data)
				pdata = f.read()
				f.close()
			httpconn.request(method,urlparse.urlunsplit(current_uriparts),pdata,self.headers)
			response = httpconn.getresponse()
			if response.status == 307:
				# temporary redirect case
				location = response.getheader('location')
				if location is None:
					raise IOError, 'Got 307 temporary redirect but no location'
				current_uriparts = urlparse.urlsplit(location)
				redirects += 1
			elif response.status == 200:
				# response is successful
				return response
			else:
				raise IOError, 'AWS connection error: %s' % response
		if redirects >= 5:
			raise IOError, 'AWS connection error: Max redirects exceeded'
	
	# Prepares and sends a Query request based on the object's parameters.		
	def query(self,query_params):
		query_params['Signature'] = self.get_query_param_signature(query_params)
		querystring = None
		data = None
		if self.method == 'GET':
			querystring = urllib.urlencode(query_params)
		elif self.method == 'POST':
			paramlist = []
			for k,v in query_params.items():
				paramlist = '%s=%s' % (k,v)
			data = '\n'.join(paramlist)
		else:
			raise IOError, 'Unsupported HTTP Query method: %s' % self.method
		fix_uri(querystring)
		
		httpconn = self.create_HTTP_connection()
		httpconn.request(method,urlparse.urlunsplit(self.uriparts),data,self.headers)
		response = httpconn.getresponse()
		if response.status != 200:
			raise IOErrror, 'AWS connection error: %s' % response
		return response
		
	# Creates the correct HTTPConnection object based on the provided URI and security specification.
	def create_HTTP_connection(self):
		if self.secure_http:
			return httplib.HTTPSConnection(self.uriparts[1],443)
		else:
			return httplib.HTTPConnection(self.uriparts[1])
		
	# Updates the provided URI to reflect the provided security specification.
	# Appends the 'querystring' parameter, if any.
	def fix_uri(self,querystring=None):
		if querystring is None:
			querystring = self.uriparts[3]
		scheme = self.uriparts[0]
		host = self.uriparts[1].split(':')
		while len(host) > 1:
			host.pop()
		if self.secure_http:
			scheme = 'https'
			host.append('443')
		else:
			scheme = 'http'
			host.append('80')
		self.uriparts = (scheme, ':'.join(host), self.uriparts[2], querystring, self.uriparts[4])
	
	# Computes the correct query parameters signature for a Query request.		
	def get_query_param_signature(self,query_params):
		sortable_params = []
		for k,v in query_params.items():
			sortable_params.append('%s%s' % (k,v))
		sortable_params.sort(lambda x,y: cmp(x.lower(), y.lower()))
		awssig = AWSSignature.AWSSignature(''.join(sortable_params), self.aws_secret_key)
		return awssig.get()		
		
	# Builds the query params for a Query request.
	def build_query_params(api_ver, sig_ver, aws_access_key, params, indexed_params={}, indexed_start=1):
		built_params = {
			'Version':api_ver,
			'SignatureVersion':sig_ver,
			'AWSAccessKeyId':aws_access_key
		}
		if not params.has_key('Timestamp') and not params.has_key('Expires'):
			params['Timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
		for k,v in params.items():
			if v is not None:
				built_params[k]=v
		for k,v in indexed_params.items():
			index_count = indexed_start
			for ent in v:
				built_params['%s.%d' % k,index_count] = ent
				index_count += 1
		return built_params
	
		


if __name__ == '__main__':
	unittest.main()