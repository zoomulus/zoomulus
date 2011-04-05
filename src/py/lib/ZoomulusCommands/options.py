#!/usr/bin/env python
# encoding: utf-8
"""
options.py

Created by Matt Ryan on 2011-02-08.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os
import getopt

import Zoomulus.paths as ZPaths

class UsageException(Exception):
	def __init__(self, msg):
		self.msg = msg

class Options:
	def __init__(self,args):
		self.beVerbose = False
		self.ParseOptions(args)
	def GetOptions(argv):
		options = argv[1:]
		if argv[0]=='zls' or argv[0].endswith('/zls'):
			return LSOptions(options)
		elif argv[0]=='zcp' or argv[0].endswith('/zcp'):
			return CPOptions(options)
		else:
			return Options(options)
	GetOptions = staticmethod(GetOptions)
	def ParseOptions(self,options):
		if options==str(options):
			options=[options]
		opts, args = getopt.getopt(options, self.ShortOptions(), self.LongOptions())
		for option, value in opts:
			if option == '--help':
				raise UsageException(self.GetHelpMessage())
			elif option == '-v':
				self.beVerbose = True
			else:
				self.HandleOption(option)
		self.HandleArgs(args)
	def GetPathsFromArgs(self,args):
		paths = []
		for arg in args:
			if ZPaths.IsCloudPath(arg):
				paths.append(ZPaths.GetCloudPath(arg))
			else:
				if os.path.isdir(arg):
					paths.append(ZPaths.LocalDir(arg))
				else:
					paths.append(ZPaths.LocalFile(arg))
		return paths		
	def HandleOption(self,option):
		pass
	def HandleArgs(self,args):
		pass
	def ShortOptions(self):
		return "hv"
	def LongOptions(self):
		return ["help"]
	def GetHelpMessage(self):
		return ""


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
