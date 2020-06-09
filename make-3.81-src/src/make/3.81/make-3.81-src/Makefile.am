# This is a -*-Makefile-*-, or close enough
#
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006
# Free Software Foundation, Inc.
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

AUTOMAKE_OPTIONS = 1.8 dist-bzip2 check-news ansi2knr
ACLOCAL_AMFLAGS	=  -I config

MAKE_HOST =	@MAKE_HOST@

# Only process if target is MS-Windows
if WINDOWSENV
  MAYBE_W32 =	w32
  W32INC =	-I $(top_srcdir)/w32/include
  W32LIB =	-Lw32 -lw32
endif

SUBDIRS =	glob config po doc $(MAYBE_W32)

bin_PROGRAMS =	make

if USE_CUSTOMS
  remote =	remote-cstms.c
else
  remote =	remote-stub.c
endif


make_SOURCES =	ar.c arscan.c commands.c default.c dir.c expand.c file.c \
		function.c getopt.c getopt1.c implicit.c job.c main.c \
		misc.c read.c remake.c $(remote) rule.c signame.c \
		strcache.c variable.c version.c vpath.c hash.c

EXTRA_make_SOURCES = vmsjobs.c remote-stub.c remote-cstms.c

noinst_HEADERS = commands.h dep.h filedef.h job.h make.h rule.h variable.h \
		debug.h getopt.h gettext.h hash.h

make_LDADD =	@LIBOBJS@ @ALLOCA@ $(GLOBLIB) @GETLOADAVG_LIBS@ @LIBINTL@
# Only process if target is MS-Windows
if WINDOWSENV
    make_LDADD += $(W32LIB)
endif

man_MANS =	make.1

DEFS =		-DLOCALEDIR=\"$(localedir)\" -DLIBDIR=\"$(libdir)\" -DINCLUDEDIR=\"$(includedir)\" @DEFS@

AM_CPPFLAGS =	$(GLOBINC)
# Only process if target is MS-Windows
if WINDOWSENV
    AM_CPPFLAGS +=	$(W32INC)
endif


# Extra stuff to include in the distribution.

EXTRA_DIST =	README build.sh.in $(man_MANS) \
		README.customs README.OS2 \
		SCOPTIONS SMakefile \
		README.Amiga Makefile.ami config.ami make.lnk amiga.c amiga.h \
		README.DOS Makefile.DOS configure.bat dosbuild.bat configh.dos\
		README.W32 NMakefile config.h.W32 build_w32.bat subproc.bat \
		make_msvc_net2003.sln make_msvc_net2003.vcproj \
		readme.vms makefile.vms makefile.com config.h-vms \
		vmsdir.h vmsfunctions.c vmsify.c

# This is built during configure, but behind configure's back

DISTCLEANFILES = build.sh

# Forward targets

html:
	cd doc && $(MAKE) $(AM_MAKEFLAGS) $@

.PHONY: html

# --------------- Internationalization Section

localedir =	$(datadir)/locale

# --------------- Local INSTALL Section

# If necessary, change the gid of the app and turn on the setgid flag.
#

# Whether or not make needs to be installed setgid.
# The value should be either `true' or `false'.
# On many systems, the getloadavg function (used to implement the `-l'
# switch) will not work unless make is installed setgid kmem.
#
inst_setgid = @NEED_SETGID@

# Install make setgid to this group so it can get the load average.
#
inst_group = @KMEM_GROUP@

install-exec-local:
	@if $(inst_setgid); then \
	   app=$(DESTDIR)$(bindir)/`echo $(bin_PROGRAMS)|sed '$(transform)'`; \
	   if chgrp $(inst_group) $$app && chmod g+s $$app; then \
	     echo "chgrp $(inst_group) $$app && chmod g+s $$app"; \
	   else \
	     echo "$$app needs to be owned by group $(inst_group) and setgid;"; \
	     echo "otherwise the \`-l' option will probably not work."; \
	     echo "You may need special privileges to complete the installation"; \
	     echo "of $$app."; \
	   fi; \
	 else true; fi

# --------------- Local DIST Section

# Install the w32 and tests subdirectories
#
dist-hook:
	(cd $(srcdir); \
	 sub=`find w32 tests -follow \( -name CVS -prune -o -name .cvsignore -o -name work -prune \) -o \( -name \*.orig -o -name \*.rej -o -name \*~ -prune \) -o -type f -print`; \
	 tar chf - $$sub) \
	| (cd $(distdir); tar xfBp -)


# --------------- Local CHECK Section

check-local: check-regression check-loadavg
	@banner=" Regression PASSED: GNU Make $(VERSION) ($(MAKE_HOST)) built with $(CC) "; \
	dashes=`echo "$$banner" | sed s/./=/g`; \
	echo; \
	echo "$$dashes"; \
	echo "$$banner"; \
	echo "$$dashes"; \
	echo

.PHONY: check-loadavg check-regression

check-loadavg: loadavg$(EXEEXT)
	@echo The system uptime program believes the load average to be:
	-uptime
	@echo The GNU load average checking code thinks:
	-./loadavg$(EXEEXT)

# The loadavg function is invoked during "make check" to test getloadavg.
check_PROGRAMS = loadavg
nodist_loadavg_SOURCES = getloadavg.c
loadavg_CPPFLAGS = -DTEST
loadavg_LDADD = @GETLOADAVG_LIBS@

# > check-regression
#
# Look for the make test suite, and run it if found and we can find perl.
# If we're building outside the tree, we use symlinks to make a local copy of
# the test suite.  Unfortunately the test suite itself isn't localizable yet.
#
MAKETESTFLAGS =

check-regression:
	@if test -f "$(srcdir)/tests/run_make_tests"; then \
	  if $(PERL) -v >/dev/null 2>&1; then \
	    case `cd $(srcdir); pwd` in `pwd`) : ;; \
	      *) test -d tests || mkdir tests; \
		 rm -f srctests; \
		 if ln -s "$(srcdir)/tests" srctests; then \
		   for f in run_make_tests run_make_tests.pl test_driver.pl scripts; do \
		     rm -f tests/$$f; ln -s ../srctests/$$f tests; \
		   done; fi ;; \
	    esac; \
	    echo "cd tests && $(PERL) ./run_make_tests.pl -make ../make$(EXEEXT) $(MAKETESTFLAGS)"; \
	    cd tests && $(PERL) ./run_make_tests.pl -make ../make$(EXEEXT) $(MAKETESTFLAGS); \
	  else \
	    echo "Can't find a working Perl ($(PERL)); the test suite requires Perl."; \
	  fi; \
	 else \
	  echo "Can't find the GNU Make test suite ($(srcdir)/tests)."; \
	 fi


# --------------- Maintainer's Section

# Tell automake that I haven't forgotten about this file and it will be
# created before we build a distribution (see maintMakefile in the CVS
# distribution).

README:

@MAINT_MAKEFILE@
