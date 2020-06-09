$!
$! Makefile.com - builds GNU Make for VMS
$!
$! P1 is non-empty if you want to link with the VAXCRTL library instead
$!    of the shareable executable
$! P2 = DEBUG will build an image with debug information
$! P3 = WALL will enable all warning messages (some are suppressed since
$!      one macro intentionally causes an error condition)
$!
$! In case of problems with the install you might contact me at
$! zinser@decus.de (preferred) or zinser@sysdev.deutsche-boerse.com
$
$! hb
$! But don't ask Martin Zinser about the lines, I added/changed.
$! In case of an error do some cleanup
$ on error then $ goto cleanup
$! in case somebody set up her/his own symbol for cc
$ set symbol/scope=(nolocal,noglobal)
$!
$! Just some general constants...
$!
$ true  = 1
$ false = 0
$ tmpnam = "temp_" + f$getjpi("","pid")
$ tt = tmpnam + ".txt"
$ tc = tmpnam + ".c"
$!
$! Look for the compiler used
$!
$ lval = ""
$ if f$search("SYS$SYSTEM:DECC$COMPILER.EXE").eqs.""
$  then
$   if f$trnlnm("SYS").eqs."" then def/nolog sys sys$library:
$   ccopt = ""
$  else
$   ccopt = "/decc/prefix=(all,except=(globfree,glob))"
$   if f$trnlnm("SYS").eqs.""
$    then
$     if f$trnlnm("DECC$LIBRARY_INCLUDE").nes.""
$      then
$       define sys decc$library_include:
$      else
$       if f$search("SYS$COMMON:[DECC$LIB.REFERENCE]DECC$RTLDEF.DIR").nes."" -
           then lval = "SYS$COMMON:[DECC$LIB.REFERENCE.DECC$RTLDEF],"
$       if f$search("SYS$COMMON:[DECC$LIB.REFERENCE]SYS$STARLET_C.DIR").nes."" -
           then lval = lval+"SYS$COMMON:[DECC$LIB.REFERENCE.SYS$STARLET_C],"
$       lval=lval+"SYS$LIBRARY:"
$       define sys 'lval
$      endif
$   endif
$ endif
$!
$! Should we build a debug image
$!
$ if (p2.eqs."DEBUG")
$  then
$   ccopt = ccopt + "/noopt/debug"
$   lopt = "/debug"
$ else
$   lopt = ""
$ endif
$!
$! Do we want to see all warnings
$!
$ if (p3.nes."WALL")
$ then
$   gosub check_cc_qual
$ endif
$ filelist = "alloca ar arscan commands default dir expand file function " + -
             "hash implicit job main misc read remake remote-stub rule " + -
	     "signame variable version vmsfunctions vmsify vpath " + -
	     "[.glob]glob [.glob]fnmatch getopt1 getopt strcache"
$ copy config.h-vms config.h
$ n=0
$ open/write optf make.opt
$ loop:
$ cfile = f$elem(n," ",filelist)
$ if cfile .eqs. " " then goto linkit
$ write sys$output "Compiling ''cfile'..."
$ call compileit 'cfile' 'p1'
$ n = n + 1
$ goto loop
$ linkit:
$ close optf
$ if p1 .nes. "" then goto link_using_library
$ link/exe=make make.opt/opt'lopt
$ goto cleanup
$
$ link_using_library:
$ link/exe=make make.opt/opt,sys$library:vaxcrtl/lib'lopt
$
$ cleanup:
$ if f$trnlnm("SYS").nes."" then $ deassign sys
$ if f$trnlnm("OPTF").nes."" then $ close optf
$ if f$search("make.opt").nes."" then $ del make.opt;*
$ exit
$!
$!-----------------------------------------------------------------------------
$!
$! Check if this is a define relating to the properties of the C/C++
$! compiler
$!
$CHECK_CC_QUAL:
$ open/write tmpc 'tc
$ ccqual = "/warn=(disable=questcompare)"
$ write tmpc "#include <stdio.h>"
$ write tmpc "unsigned int i = 1;"
$ write tmpc "int main(){"
$ write tmpc "if (i < 0){printf(""Mission impossible\n"");}}"
$ close tmpc
$ gosub cc_qual_check
$ return
$!
$!-----------------------------------------------------------------------------
$!
$! Check for properties of C/C++ compiler
$!
$CC_QUAL_CHECK:
$ cc_qual = false
$ set message/nofac/noident/nosever/notext
$ cc 'ccqual' 'tmpnam'
$ if $status then cc_qual = true
$ set message/fac/ident/sever/text
$ delete/nolog 'tmpnam'.*;*
$ if cc_qual then ccopt = ccopt + ccqual
$ return
$!-----------------------------------------------------------------------------
$!
$ compileit : subroutine
$ ploc = f$locate("]",p1)
$ filnam = p1
$ if ploc .lt. f$length(p1) then filnam=f$extract(ploc+1,100,p1)
$ write optf "''filnam'"
$ cc'ccopt'/include=([],[.glob]) -
  /define=("allocated_variable_expand_for_file=alloc_var_expand_for_file","unlink=remove","HAVE_CONFIG_H","VMS") -
  'p1'
$ exit
$ endsubroutine : compileit
$!
$!-----------------------------------------------------------------------------
$!Copyright (C) 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
$!2006 Free Software Foundation, Inc.
$!This file is part of GNU Make.
$!
$!GNU Make is free software; you can redistribute it and/or modify it under the
$!terms of the GNU General Public License as published by the Free Software
$!Foundation; either version 2, or (at your option) any later version.
$!
$!GNU Make is distributed in the hope that it will be useful, but WITHOUT ANY
$!WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
$!A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
$!
$!You should have received a copy of the GNU General Public License along with
$!GNU Make; see the file COPYING.  If not, write to the Free Software
$!Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
