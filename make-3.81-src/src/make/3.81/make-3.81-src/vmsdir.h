/* dirent.h for vms
Copyright (C) 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
2006 Free Software Foundation, Inc.
This file is part of GNU Make.

GNU Make is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 2, or (at your option) any later version.

GNU Make is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
GNU Make; see the file COPYING.  If not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.  */

#ifndef VMSDIR_H
#define VMSDIR_H

#include <rms.h>

#define	MAXNAMLEN	255

#ifndef __DECC
#if !defined (__GNUC__) && !defined (__ALPHA)
typedef unsigned long u_long;
typedef unsigned short u_short;
#endif
#endif

struct direct
{
  off_t d_off;
  u_long d_fileno;
  u_short d_reclen;
  u_short d_namlen;
  char d_name[MAXNAMLEN + 1];
};

#undef DIRSIZ
#define DIRSIZ(dp)		\
  (((sizeof (struct direct)	\
     - (MAXNAMLEN+1)		\
     + ((dp)->d_namlen+1))	\
    + 3) & ~3)

#define d_ino	d_fileno		/* compatability */


/*
 * Definitions for library routines operating on directories.
 */

typedef struct DIR
{
  struct direct dir;
  char d_result[MAXNAMLEN + 1];
#if defined (__ALPHA) || defined (__DECC)
  struct FAB fab;
#else
  struct fabdef fab;
#endif
} DIR;

#ifndef NULL
#define NULL 0
#endif

extern	DIR *opendir PARAMS (());
extern	struct direct *readdir PARAMS ((DIR *dfd));
#define rewinddir(dirp)	seekdir((dirp), (long)0)
extern	int closedir PARAMS ((DIR *dfd));
extern char *vmsify PARAMS ((char *name, int type));

#endif /* VMSDIR_H */
