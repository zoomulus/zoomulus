#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py for Zoomulus package.

Created by Matt Ryan on 2011-03-12.
Copyright (c) 2011 zoomulus.org. All rights reserved.
"""

import sys
import os

import path as zpath

def access(path,mode):
	if not zpath.iscloudpath(path):
		return os.access(path,mode)
	return None
	
def chdir(path):
	pass
	
def chmod(path,mode):
	pass
	
def getcwd():
	pass
	
def listdir(path):
	if not zpath.iscloudpath(path):
		return os.listdir(path)
	return None
	
def makedirs(path,mode=0777):
	if not zpath.iscloudpath(path):
		return os.makedirs(path,mode)
	return None
	
def mkdir(path,mode=0777):
	if not zpath.iscloudpath(path):
		return os.mkdir(path,mode)
	return None
	
def remove(path):
	if not zpath.iscloudpath(path):
		return os.remove(path)
	return None
	
def unlink(path):
	return remove(path)
	
def removedirs(path):
	if not zpath.iscloudpath(path):
		return os.removedirs(path)
	return None
	
def rmdir(path):
	if not zpath.iscloudpath(path):
		return os.rmdir(path)
	return None
	
def rename(source,dest):
	if not zpath.iscloudfile(source) and not zpath.isclouddir(source) \
		and not zpath.iscloudfile(dest) and not zpath.isclouddir(dest):
		return os.rename(source,dest)
	return None
	
def renames(source,dest):
	if not zpath.iscloudfile(source) and not zpath.isclouddir(source) \
		and not zpath.iscloudfile(dest) and not zpath.isclouddir(dest):
		return os.renames(source,dest)
	return None
	
def stat(path):
	pass
	
def utime(path,times=None):
	pass
	
#File descriptor methods
def close(fd):
	pass

def dup(fd):
	pass
	
def dup2(fd,fd2):
	pass
	
def fdopen(fd,mode='r',bufsize=-1):
	pass
	
def fstat(fd):
	pass
	
def lseek(fd,pos,how):
	pass
	
def open(path,flags,mode=0777):
	if not zpath.iscloudpath(path):
		return os.open(path,flags,mode)
	return None
	
def pipe():
	pass
	
def read(fd,n):
	pass
	
def write(fd,str):
	pass

def main():
	pass


if __name__ == '__main__':
	main()

