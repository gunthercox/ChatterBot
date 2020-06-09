@echo off
rem Copyright (C) 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
rem 2004, 2005, 2006 Free Software Foundation, Inc.
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

echo Configuring MAKE for DJGPP

rem The SmallEnv trick protects against too small environment block,
rem in which case the values will be truncated and the whole thing
rem goes awry.  COMMAND.COM will say "Out of environment space", but
rem many people don't care, so we force them to care by refusing to go.

rem Where is the srcdir?
set XSRC=.
if not "%XSRC%"=="." goto SmallEnv
if "%1%"=="" goto SrcDone
set XSRC=%1
if not "%XSRC%"=="%1" goto SmallEnv

:SrcDone

update %XSRC%/configh.dos ./config.h

rem Do they have Make?
redir -o junk.$$$ -eo make -n -f NUL
rem REDIR will return 1 if it cannot run Make.
rem If it can run Make, it will usually return 2,
rem but 0 is also OK with us.
if errorlevel 2 goto MakeOk
if not errorlevel 1 goto MakeOk
if exist junk.$$$ del junk.$$$
echo No Make program found--use DOSBUILD.BAT to build Make.
goto End

rem They do have Make.	Generate the Makefile.

:MakeOk
del junk.$$$
update %XSRC%/Makefile.DOS ./Makefile
echo Done.
if not "%XSRC%"=="." echo Invoke Make thus: "make srcdir=%XSRC%"
goto End

:SmallEnv
echo Your environment is too small.  Please enlarge it and run me again.

:End
set XRSC=
