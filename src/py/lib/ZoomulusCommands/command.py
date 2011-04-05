#!/usr/bin/env python
# encoding: utf-8
"""
command.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os


class Command:
	def __init__(self,options):
		pass
	def GetCommand(options):
		if options.IsCPOptions():
			return CPCommand(options)
		elif options.IsLSOptions():
			return LSCommand(options)
		else:
			return Command(options)
	GetCommand = staticmethod(GetCommand)

