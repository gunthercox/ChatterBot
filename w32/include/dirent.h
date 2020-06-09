/* Windows version of dirent.h
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

#ifndef _DIRENT_H
#define _DIRENT_H

#ifdef __MINGW32__
# include <windows.h>
# include_next <dirent.h>
#else

#include <stdlib.h>
#include <windows.h>
#include <limits.h>
#include <sys/types.h>

#ifndef NAME_MAX
#define NAME_MAX 255
#endif

#define __DIRENT_COOKIE 0xfefeabab


struct dirent
{
  ino_t d_ino; 			/* unused - no equivalent on WINDOWS32 */
  char d_name[NAME_MAX+1];
};

typedef struct dir_struct {
	ULONG	dir_ulCookie;
	HANDLE	dir_hDirHandle;
	DWORD	dir_nNumFiles;
	char	dir_pDirectoryName[NAME_MAX+1];
	struct dirent dir_sdReturn;
} DIR;

DIR *opendir(const char *);
struct dirent *readdir(DIR *);
void rewinddir(DIR *);
void closedir(DIR *);
int telldir(DIR *);
void seekdir(DIR *, long);

#endif  /* !__MINGW32__ */
#endif
