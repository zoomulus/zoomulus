#!/usr/bin/env python
# encoding: utf-8
"""
options.py

Created by Matt Ryan on 2011-02-08.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os
import unittest
import getopt

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
	def ShortOptions(self):
		return "hv"
	def LongOptions(self):
		return ["help"]
	def GetHelpMessage(self):
		return ""

class OptionsTests(unittest.TestCase):
	def setUp(self):
		pass
	def testOption_v(self):
		o = Options('-v')
		self.assertTrue(o.beVerbose)
	def testOption_help(self):
		try:
			o = Options('--help')
			self.fail()
		except UsageException:
			pass
		except Exception:
			self.fail()


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


class CPOptionsTests(unittest.TestCase):
	def setUp(self):
		pass
	def testOption_a(self):
		o = CPOptions('-a')
		self.assertTrue(o.preserveFileStatistics)
		self.assertTrue(o.recursiveCopy)
		self.assertFalse(o.followSymLinks)
	def testOption_f(self):
		o = CPOptions('-f')
		self.assertEquals('f',o.overwriteMode)
	def testOption_i(self):
		o = CPOptions('-i')
		self.assertEquals('i',o.overwriteMode)
	def testOption_n(self):
		o = CPOptions('-n')
		self.assertEquals('n',o.overwriteMode)
	def testOption_p(self):
		o = CPOptions('-p')
		self.assertTrue(o.preserveFileStatistics)
	def testOption_P(self):
		o = CPOptions('-P')
		self.assertFalse(o.followSymLinks)
	def testOption_R(self):
		o = CPOptions('-R')
		self.assertTrue(o.recursiveCopy)
	def testOption_v(self):
		o = CPOptions('-v')
		self.assertTrue(o.beVerbose)



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
		

class LSOptionsTests(unittest.TestCase):
	def setUp(self):
		pass
	def testOption_a(self):
		o = LSOptions('-a')
		self.assertTrue(o.showHiddenFiles)
	def testOption_c(self):
		o = LSOptions('-c')
		self.assertEqual('c',o.sortBy)
	def testOption_e(self):
		o = LSOptions('-e')
		self.assertTrue(o.showACLs)
	def testOption_h(self):
		o = LSOptions('-h')
		self.assertTrue(o.humanReadable)
	def testOption_l(self):
		o = LSOptions('-l')
		self.assertTrue(o.longListing)
	def testOption_o(self):
		o = LSOptions('-o')
		self.assertFalse(o.showGroupInfo)
	def testOption_r(self):
		o = LSOptions('-r')
		self.assertTrue(o.reverseSort)
	def testOption_R(self):
		o = LSOptions('-R')
		self.assertTrue(o.recursive)
	def testOption_S(self):
		o = LSOptions('-S')
		self.assertEquals('S',o.sortBy)
	def testOption_t(self):
		o = LSOptions('-t')
		self.assertEquals('t',o.sortBy)
	def testOption_T(self):
		o = LSOptions('-T')
		self.assertTrue(o.showTimeInfo)
	def testOption_u(self):
		o = LSOptions('-u')
		self.assertEquals('u',o.sortBy)
	def testOption_U(self):
		o = LSOptions('-U')
		self.assertEquals('U',o.sortBy)


if __name__ == '__main__':
	unittest.main()