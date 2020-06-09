#!/bin/sh
# Shell script to build GNU Make in the absence of any `make' program.
# build.sh.  Generated from build.sh.in by configure.

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

# See Makefile.in for comments describing these variables.

srcdir='../make-3.81-src'
CC='gcc'
CFLAGS=' -Wall -O3 -fms-extensions -mms-bitfields -fno-exceptions -fomit-frame-pointer -march=i386 -ffast-math  '
CPPFLAGS='       -ID:/Progra~1/GnuWin32/include    '
LDFLAGS=' -Wl,-s -Wl,--force-exe-suffix -Wl,--enable-auto-import -Wl,--enable-runtime-pseudo-reloc -Wl,--allow-multiple-definition -Wl,--enable-stdcall-fixup -LD:/Progra~1/GnuWin32/lib   '
ALLOCA=''
LOADLIBES=' -Wl,-s  -LD:/Progra~1/GnuWin32/lib  -lintl -lwsock32 -lole32 -luuid -lmsvcp60   -lintl'
eval extras=\' getloadavg$U.o\'
REMOTE='stub'
GLOBLIB='glob/libglob.a'
PATH_SEPARATOR=':'
OBJEXT='o'
EXEEXT='.exe'

# Common prefix for machine-independent installed files.
prefix='c:/progra~1/Make'
# Common prefix for machine-dependent installed files.
exec_prefix=`eval echo c:/progra~1/Make`
# Directory to find libraries in for `-lXXX'.
libdir=${exec_prefix}/lib
# Directory to search by default for included makefiles.
includedir=${prefix}/include

localedir=${prefix}/share/locale
aliaspath=${localedir}${PATH_SEPARATOR}.

defines="-DALIASPATH=\"${aliaspath}\" -DLOCALEDIR=\"${localedir}\" -DLIBDIR=\"${libdir}\" -DINCLUDEDIR=\"${includedir}\""' -DHAVE_CONFIG_H'

# Exit as soon as any command fails.
set -e

# These are all the objects we need to link together.
objs="ar.${OBJEXT} arscan.${OBJEXT} commands.${OBJEXT} default.${OBJEXT} dir.${OBJEXT} expand.${OBJEXT} file.${OBJEXT} function.${OBJEXT} getopt.${OBJEXT} getopt1.${OBJEXT} implicit.${OBJEXT} job.${OBJEXT} main.${OBJEXT} misc.${OBJEXT} read.${OBJEXT} remake.${OBJEXT} rule.${OBJEXT} signame.${OBJEXT} strcache.${OBJEXT} variable.${OBJEXT} version.${OBJEXT} vpath.${OBJEXT} hash.${OBJEXT} remote-${REMOTE}.${OBJEXT} ${extras} ${ALLOCA}"

if [ x"$GLOBLIB" != x ]; then
  objs="$objs glob/fnmatch.${OBJEXT} glob/glob.${OBJEXT}"
  globinc=-I${srcdir}/glob
fi

# Compile the source files into those objects.
for file in `echo ${objs} | sed 's/\.'${OBJEXT}'/.c/g'`; do
  echo compiling ${file}...
  $CC $defines $CPPFLAGS $CFLAGS \
      -c -I. -I${srcdir} ${globinc} ${srcdir}/$file
done

# The object files were actually all put in the current directory.
# Remove the source directory names from the list.
srcobjs="$objs"
objs=
for obj in $srcobjs; do
  objs="$objs `basename $obj`"
done

# Link all the objects together.
echo linking make...
$CC $CFLAGS $LDFLAGS $objs $LOADLIBES -o makenew${EXEEXT}
echo done
mv -f makenew${EXEEXT} make${EXEEXT}
