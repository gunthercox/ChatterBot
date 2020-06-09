# Test if the system uses DOS-style pathnames (drive specs and backslashes)
# By Paul Smith <psmith@gnu.org>.  Based on dos.m4 by Jim Meyering.

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

AC_DEFUN([pds_AC_DOS_PATHS],
  [
    AC_CACHE_CHECK([whether system uses MSDOS-style paths], [ac_cv_dos_paths],
      [
        AC_COMPILE_IFELSE([
#if !defined _WIN32 && !defined __WIN32__ && !defined __MSDOS__ && !defined __EMX__ && !defined __MSYS__
neither MSDOS nor Windows nor OS2
#endif
],
        [ac_cv_dos_paths=yes],
        [ac_cv_dos_paths=no])
      ])

    if test x"$ac_cv_dos_paths" = xyes; then
      AC_DEFINE_UNQUOTED([HAVE_DOS_PATHS], 1,
                         [Define if the system uses DOS-style pathnames.])
    fi
  ])
