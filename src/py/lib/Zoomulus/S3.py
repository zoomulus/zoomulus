#!/usr/bin/env python
# encoding: utf-8
"""
S3.py

Created by Matt Ryan on 2011-08-25.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import urlparse
import urllib
import re


class S3:
	def __init__(self,secure_http=True):
		self.secure_http = secure_http
		self.s3_endpoint = 's3.amazonaws.com'
		
	def is_dns(self,host):
		if len(host) > 63 or len(host) < 3:
			return False
		h1 = re.compile(r'^[a-z0-9][a-z0-9.-]+$')
		h2 = re.compile(r'[a-z]')
		if not h1.match(host) or not h2.match(host):
			return False
		p1 = re.compile(r'^-')
		p2 = re.compile(r'-$')
		p3 = re.compile(r'^$')
		for part in host.split('.'):
			if p1.match(part) or p2.match(part) or p3.match(part):
				return False
		return True
		
	def make_uri(self, bucketname='', filename='', params={}):
		scheme = 'http'
		if self.secure_http:
			scheme = 'https'
		host = ''
		path = ''
		if self.is_dns(bucketname):
			host = '%s.%s' % (bucketname, self.s3_endpoint)
		elif len(bucketname):
			host = '%s/%s' % (self.s3_endpoint, urllib.quote(bucketname))
		else:
			host = self.s3_endpoint
		if len(filename):
			path = '/%s' % urllib.quote(filename)
		query = ''
		if len(params):
			query = urllib.urlencode(params)
		return urlparse.urlunsplit((scheme,host,path,query,''))
		
		

	def create_bucket(self,bucketname):
		uri = self.make_uri(bucketname)
		req = AWSRestRequest.AWSRestRequest('PUT',uri)
		req.request()
		return True
		
	def get_buckets(self):
		uri = self.make_uri()
		req = AWSRestRequest.AWSRestRequest('GET',uri)
		response = req.request()
		return True
		
	def delete_bucket(self,bucketname):
		uri = self.make_uri(bucketname)
		req = AWSRestRequest.AWSRestRequest('DELETE',uri)
		req.request()
		return True
		
	def create_file(self):
		pass
		
	def get_file(self):
		pass
		
	def get_file_info(self):
		pass
		
	def get_files(self):
		pass
		
	def delete_file(self):
		pass