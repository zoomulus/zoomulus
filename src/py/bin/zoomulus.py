#!/usr/bin/env python
# encoding: utf-8
"""
zoomulus.py

Created by Matt Ryan on 2011-02-08.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import getopt
from ZoomulusCommands.options import Options, UsageException


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			options = Options.GetOptions(argv)
		except getopt.error, msg:
			raise UsageException(msg)
	
	except UsageException, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + " usage: " + str(err.msg)
		print >> sys.stderr, "\t for help use --help\n"
		return 2


if __name__ == "__main__":
	sys.exit(main())
