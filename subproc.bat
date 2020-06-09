@echo off
rem Copyright (C) 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
rem 2005, 2006 Free Software Foundation, Inc.
rem This file is part of GNU Make.

rem GNU Make is free software; you can redistribute it and/or modify it under
rem the terms of the GNU General Public License as published by the Free
rem Software Foundation; either version 2, or (at your option) any later
rem version.

rem GNU Make is distributed in the hope that it will be useful, but WITHOUT
rem ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
rem FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
rem more details.

rem You should have received a copy of the GNU General Public License along
rem with GNU Make; see the file COPYING.  If not, write to the Free Software
rem Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.

cd w32\subproc
set MAKE=%2
set MAKEFILE=%1
if x%2 == x set MAKE=nmake
%MAKE% /f %MAKEFILE%
cd ..\..
