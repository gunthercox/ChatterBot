# -*-Makefile-*-, or close enough
# Copyright (C) 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
# 2003, 2004, 2005, 2006 Free Software Foundation, Inc.
# This file is part of GNU Make.
#
# GNU Make is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2, or (at your option) any later version.
#
# GNU Make is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Make; see the file COPYING.  If not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.

AUTOMAKE_OPTIONS =	foreign

# Only build the library when the system doesn't already have GNU glob.
if USE_LOCAL_GLOB
  noinst_LIBRARIES =	libglob.a
endif

libglob_a_SOURCES =	glob.c glob.h fnmatch.c fnmatch.h


EXTRA_DIST =		COPYING.LIB Makefile.ami SCOPTIONS SMakefile \
			configure.bat
