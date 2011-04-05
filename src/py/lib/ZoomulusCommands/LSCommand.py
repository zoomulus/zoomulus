#!/usr/bin/env python
# encoding: utf-8
"""
LSCommand.py

Created by Matt Ryan on 2011-04-05.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os

from ZoomulusCommands.command import Command


class LSCommand(Command):
	def __init__(self,options):
		Command.__init__(self,options)
