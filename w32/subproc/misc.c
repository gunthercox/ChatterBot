/* Process handling for Windows
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

#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include "proc.h"


/*
 * Description:  Convert a NULL string terminated UNIX environment block to
 *		an environment block suitable for a windows32 system call
 *
 * Returns:  TRUE= success, FALSE=fail
 *
 * Notes/Dependencies:  the environment block is sorted in case-insensitive
 *	order, is double-null terminated, and is a char *, not a char **
 */
int _cdecl compare(const void *a1, const void *a2)
{
	return _stricoll(*((char**)a1),*((char**)a2));
}
bool_t
arr2envblk(char **arr, char **envblk_out)
{
	char **tmp;
	int size_needed;
	int arrcnt;
	char *ptr;

	arrcnt = 0;
	while (arr[arrcnt]) {
		arrcnt++;
	}

	tmp = (char**) calloc(arrcnt + 1, sizeof(char *));
	if (!tmp) {
		return FALSE;
	}

	arrcnt = 0;
	size_needed = 0;
	while (arr[arrcnt]) {
		tmp[arrcnt] = arr[arrcnt];
		size_needed += strlen(arr[arrcnt]) + 1;
		arrcnt++;
	}
	size_needed++;

	qsort((void *) tmp, (size_t) arrcnt, sizeof (char*), compare);

	ptr = *envblk_out = calloc(size_needed, 1);
	if (!ptr) {
		free(tmp);
		return FALSE;
	}

	arrcnt = 0;
	while (tmp[arrcnt]) {
		strcpy(ptr, tmp[arrcnt]);
		ptr += strlen(tmp[arrcnt]) + 1;
		arrcnt++;
	}

        free(tmp);
	return TRUE;
}
