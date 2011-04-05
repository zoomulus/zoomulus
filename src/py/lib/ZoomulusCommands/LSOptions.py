#!/usr/bin/env python
# encoding: utf-8
"""
LSOptions.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os

from ZoomulusCommands.options import Options, UsageException
import Zoomulus.paths as ZPaths

class LSOptions(Options):
	def __init__(self,args):
		self.showHiddenFiles = False
		self.sortBy = None
		self.showACLs = False
		self.humanReadable = False
		self.longListing = False
		self.showGroupInfo = True
		self.reverseSort = False
		self.recursive = False
		self.showTimeInfo = False
		self.showFolders = False
		Options.__init__(self,args)
	def ShortOptions(self):
		return 'acehloRrSTtUu'
	def HandleOption(self,option):
		if option == '-a':
			self.showHiddenFiles = True
		elif option == '-c':
			self.sortBy = 'c'
		elif option == '-e':
			self.showACLs = True
		elif option == '-h':
			self.humanReadable = True
		elif option == '-l':
			self.longListing = True
		elif option == '-o':
			self.showGroupInfo = False
		elif option == '-R':
			self.recursive = True
		elif option == '-r':
			self.reverseSort = True
		elif option == '-S':
			self.sortBy = 'S'
		elif option == '-T':
			self.showTimeInfo = True
		elif option == '-t':
			self.sortBy = 't'
		elif option == '-U':
			self.sortBy = 'U'
		elif option == '-u':
			self.sortBy = 'u'
		else:
			raise UsageException("Unsupported option: " + option)
	def HandleArgs(self,args):
		self.targets = None
		nArgs = 0
		if not args:
			self.targets = [ZPaths.LocalDir(os.getcwd())]
		else:
			nArgs = len(args)
			if nArgs < 1:
				self.targets = [ZPaths.LocalDir(os.getcwd())]
		if self.targets is None:
			self.targets = self.GetPathsFromArgs(args)
			if nArgs > 1:
				for t in self.targets:
					if t.IsLocalDir():
						self.showFolders = True
						break
	def GetHelpMessage(self):
		return """
	zls [options] file [file...]
	zls [options] directory

Options:
	-a: Also show hidden entries and current and parent directories
	-c: When combined with -t or -l, sort by last changed time
	-e: When combined with -l, show any ACLs on the file(s)
	-h: When combined with -l, show file sizes in human-readable form
	-l: Show listing in long (i.e. detailed) format
	-o: Show listing in long format but omit group name / gid
	-r: Reverse sort order
	-R: Recursively list directories
	-S: Sort by size, largest first
	-T: When combined with -l, show complete time information
	-t: Sort by time, most recently modified first
	-u: When combined with -t or -l, sort by last access time
	-U: When combined with -t or -l, sort by creation time
"""
