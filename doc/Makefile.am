# -*-Makefile-*-, or close enough
# Copyright (C) 2000, 2001, 2002, 2003, 2004, 2005, 2006 Free Software
# Foundation, Inc.
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

TEXI2HTML = texi2html
TEXI2HTML_FLAGS = -split_chapter

info_TEXINFOS =	make.texi
make_TEXINFOS = fdl.texi make-stds.texi

CLEANFILES = make*.html

## ----------------------------- ##
## Other documentation formats.  ##
## ----------------------------- ##

html: make_1.html

make_1.html: $(info_TEXINFOS) $(make_TEXINFOS)
	$(TEXI2HTML) $(TEXI2HTML_FLAGS) $(srcdir)/make.texi

.PHONY: html
