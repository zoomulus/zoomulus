#!/usr/bin/env python
# encoding: utf-8
"""
CPOptions.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os

from ZoomulusCommands.options import Options, UsageException
import Zoomulus.paths as ZPaths

class CPOptions(Options):
	def __init__(self,args):
		self.preserveFileStatistics = False
		self.followSymLinks = True
		self.recursiveCopy = False
		self.overwriteMode = None
		Options.__init__(self,args)
	def ShortOptions(self):
		return 'pPRafniv'
	def HandleOption(self,option):
		if option == '-p':
			self.preserveFileStatistics = True
		elif option == '-P':
			self.followSymLinks = False
		elif option == '-R':
			self.recursiveCopy = True
		elif option == '-a':
			self.preserveFileStatistics = True
			self.followSymLinks = False
			self.recursiveCopy = True
		elif option == '-f':
			self.overwriteMode = 'f'
		elif option == '-n':
			self.overwriteMode = 'n'
		elif option == '-i':
			self.overwriteMode = 'i'
		else:
			raise UsageException("Unsupported option: " + option)
	def HandleArgs(self,args):
		if not args:
			raise UsageException("No arguments supplied")
		nArgs = len(args)
		if nArgs < 1:
			raise UsageException("No arguments supplied")
		if nArgs < 2:
			raise UsageException("No destination supplied")
		f = self.GetPathsFromArgs(args)
		self.target = f[nArgs-1]

		# Verify we are not trying to recursive copy to a local file target.
		if self.recursiveCopy and self.target.IsLocalFile():
			s = str(self.target)
			self.target = None
			raise UsageException("Cannot recursive copy to local file "+s)
		self.sources = f[:(nArgs-1)]

		# Verify we are not trying to copy multiple sources to a single local file target,
		# or that we are not trying to copy a local directory to a single local file target.
		if self.target.IsLocalFile():
			if len(self.sources) > 1:
				s = str(self.target)
				self.sources = None
				self.target = None
				raise UsageException("Cannot copy multiple sources to local file "+s)
			elif self.sources[0].IsLocalDir():
				ld = str(self.sources[0])
				lf = str(self.target)
				self.sources = None
				self.target = None
				raise UsageException("Cannot copy local directory "+ld+" to local file "+lf)

		# Verify that we are not trying to a source to a target that is the same as the source.
		for src in self.sources:
			if src == self.target:
				ftype = 'local file'
				if self.target.IsLocalDir():
					ftype = 'local directory'
				elif ZPaths.IsCloudPath(str(self.target)):
					ftype = 'cloud resource'
				raise UsageException("Cannot copy "+ftype+"to itself")
	def GetHelpMessage(self):
		return """
	zcp [options] source_file target_file
	zcp [options] source_file [source_file...] target_directory

Options:
	-a: Archive copy (same as -pPR)
	-f: Force copy over existing files regardless of current permissions
	-i: Inquire before copying over an existing file with the same name
	-n: Do not copy over existing files with the same name
	-p: Preserve file statistics
	-P: Don't follow symbolic links
	-R: Recursively copy an entire directory
	-v: Be verbose
"""
