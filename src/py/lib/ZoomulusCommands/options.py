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
			elif self.recursiveCopy:
				paths.append(ZPaths.LocalDir(arg))
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


class CPOptionsTests(unittest.TestCase):
	def setUp(self):
		self.fArgs = ['/path/to/f1','/path/to/f2']
	def argsTest(self,a):
		strargs = []
		for ent in a:
			strargs.append(str(ent))
		o = CPOptions(strargs)
		self.assertEquals(len(o.sources),len(a)-1)
		for i in xrange(0,len(a)-2):
			self.assertEquals(o.sources[i],a[i])
		self.assertEquals(o.target,a[len(a)-1])
	def argsTestException(self,a):
		ueThrown = False
		try:
			strargs = []
			for ent in a:
				strargs.append(str(ent))
			o = CPOptions(strargs)
		except UsageException:
			ueThrown = True
		self.assertTrue(ueThrown)

	def testOption_a(self):
		o = CPOptions(['-a']+self.fArgs)
		self.assertTrue(o.preserveFileStatistics)
		self.assertTrue(o.recursiveCopy)
		self.assertFalse(o.followSymLinks)
	def testOption_f(self):
		o = CPOptions(['-f']+self.fArgs)
		self.assertEquals('f',o.overwriteMode)
	def testOption_i(self):
		o = CPOptions(['-i']+self.fArgs)
		self.assertEquals('i',o.overwriteMode)
	def testOption_n(self):
		o = CPOptions(['-n']+self.fArgs)
		self.assertEquals('n',o.overwriteMode)
	def testOption_p(self):
		o = CPOptions(['-p']+self.fArgs)
		self.assertTrue(o.preserveFileStatistics)
	def testOption_P(self):
		o = CPOptions(['-P']+self.fArgs)
		self.assertFalse(o.followSymLinks)
	def testOption_R(self):
		o = CPOptions(['-R']+self.fArgs)
		self.assertTrue(o.recursiveCopy)
	def testOption_v(self):
		o = CPOptions(['-v']+self.fArgs)
		self.assertTrue(o.beVerbose)
	def testCopyFileToFile(self):
		self.argsTest([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.LocalFile('../../testdata/test2.txt')])
	def testCopyFileToDir(self):
		self.argsTest([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.LocalDir('../../testdata/testdir1')])
	def testCopyFileToAWSFile(self):
		self.argsTest([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.AWSPath('aws://bucket/test.txt')])
	def testCopyFileToAWSBucket(self):
		self.argsTest([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyDirToFile(self):
		self.argsTestException([ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalFile('../../testdata/test.txt')])
	def testCopyDirToDir(self):
		self.argsTest([ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir2')])
	def testCopyDirToAWSFile(self):
		self.argsTest([ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.AWSPath('aws://bucket/test.txt')])
	def testCopyDirToAWSBucket(self):
		self.argsTest([ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyAWSToFile(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.LocalFile('../../testdata/test.txt')])
	def testCopyAWSToDir(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.LocalDir('../../testdata/testdir1')])
	def testCopyAWSToAWS(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.AWSPath('aws://bucket/test2.txt')])
	def testCopyFileToSelf(self):
		f = ZPaths.LocalFile('../../testdata/test.txt')
		self.argsTestException([f,f])
	def testCopyFileToSame(self):
		self.argsTestException([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.LocalFile('../../testdata/test.txt')])
	def testCopyDirToSelf(self):
		d = ZPaths.LocalDir('../../testdata/testdir1')
		self.argsTestException([d,d])
	def testCopyDirToSame(self):
		self.argsTestException([ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir1')])
	def testCopyAWSToSelf(self):
		c = ZPaths.AWSPath('aws://bucket/test.txt')
		self.argsTestException([c,c])
	def testCopyAWSToSame(self):
		self.argsTestException([ZPaths.AWSPath('aws://bucket/test.txt'),
			ZPaths.AWSPath('aws://bucket/test.txt')])
	def testCopyFilesToFile(self):
		self.argsTestException([ZPaths.LocalFile('../../testdata/testdir1/td1test.txt'),
			ZPaths.LocalFile('../../testdata/testdir2/td2test.txt'),
			ZPaths.LocalFile('../../testdata/test.txt')])
	def testCopyFilesToDir(self):
		self.argsTest([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.LocalFile('../../testdata/testdir1/td1test.txt'),
			ZPaths.LocalDir('../../testdata/testdir2')])
	def testCopyFilesToAWS(self):
		self.argsTest([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.LocalFile('../../testdata/testdir1/td1test.txt'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyDirsToFile(self):
		self.argsTestException([ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir2'),
			ZPaths.LocalFile('../../testdata/test.txt')])
	def testCopyDirsToDir(self):
		self.argsTest([ZPaths.LocalDir('../../testdata'),
			ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir2')])
	def testCopyDirsToAWS(self):
		self.argsTest([ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir2'),
			ZPaths.AWSPath('aws://bucket/')])
	def testCopyAWSsToFile(self):
		self.argsTestException([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.LocalFile('../../testdata/test.txt')])
	def testCopyAWSsToDir(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.LocalDir('../../testdata')])
	def testCopyAWSsToAWS(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.AWSPath('aws://bucket/dir1')])
	def testCopyFilesToDirWithDuplicateSources(self):
		self.argsTest([ZPaths.LocalFile('../../testdata/test.txt'),
			ZPaths.LocalFile('../../testdata/testdir1/td1test.txt'),
			ZPaths.LocalFile('../../testdata/testdir1/td1test.txt'),
			ZPaths.LocalDir('../../testdata/testdir2')])
	def testCopyDirsToSelf(self):
		self.argsTestException([ZPaths.LocalDir('../../testdata'),
			ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir2'),
			ZPaths.LocalDir('../../testdata/testdir2')])
	def testCopyDirsToDirWithDuplicateSources(self):
		self.argsTest([ZPaths.LocalDir('../../testdata'),
			ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir1'),
			ZPaths.LocalDir('../../testdata/testdir2')])
	def testCopyAWSsToDirWithDuplicateSources(self):
		self.argsTest([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.LocalDir('../../testdata')])
	def testCopyAWSsToSelf(self):
		self.argsTestException([ZPaths.AWSPath('aws://bucket/file1'),
			ZPaths.AWSPath('aws://bucket/file2'),
			ZPaths.AWSPath('aws://bucket/file1')])



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
		f = None
		nArgs = 0
		if not args:
			f = [ZPaths.LocalDir(os.getcwd())]
		else:
			nArgs = len(args)
			if nArgs < 1:
				f = [ZPaths.LocalDir(os.getcwd())]
		if f is None:
			f = self.GetPathsFromArgs(args)
			if nArgs > 1:
				self.showFolders = True
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