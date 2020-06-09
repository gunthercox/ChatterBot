/* Running commands on Amiga
Copyright (C) 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
2005, 2006 Free Software Foundation, Inc.
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

#include "make.h"
#include "variable.h"
#include "amiga.h"
#include <assert.h>
#include <exec/memory.h>
#include <dos/dostags.h>
#include <proto/exec.h>
#include <proto/dos.h>

static const char Amiga_version[] = "$VER: Make 3.74.3 (12.05.96) \n"
		    "Amiga Port by A. Digulla (digulla@home.lake.de)";

int
MyExecute (char **argv)
{
    char * buffer, * ptr;
    char ** aptr;
    int len = 0;
    int status;

    for (aptr=argv; *aptr; aptr++)
    {
	len += strlen (*aptr) + 4;
    }

    buffer = AllocMem (len, MEMF_ANY);

    if (!buffer)
      fatal (NILF, "MyExecute: Cannot allocate space for calling a command");

    ptr = buffer;

    for (aptr=argv; *aptr; aptr++)
    {
	if (((*aptr)[0] == ';' && !(*aptr)[1]))
	{
	    *ptr ++ = '"';
	    strcpy (ptr, *aptr);
	    ptr += strlen (ptr);
	    *ptr ++ = '"';
	}
	else if ((*aptr)[0] == '@' && (*aptr)[1] == '@' && !(*aptr)[2])
	{
	    *ptr ++ = '\n';
	    continue;
	}
	else
	{
	    strcpy (ptr, *aptr);
	    ptr += strlen (ptr);
	}
	*ptr ++ = ' ';
	*ptr = 0;
    }

    ptr[-1] = '\n';

    status = SystemTags (buffer,
	SYS_UserShell, TRUE,
	TAG_END);

    FreeMem (buffer, len);

    if (SetSignal(0L,0L) & SIGBREAKF_CTRL_C)
	status = 20;

    /* Warnings don't count */
    if (status == 5)
	status = 0;

    return status;
}

char *
wildcard_expansion (char *wc, char *o)
{
#   define PATH_SIZE	1024
    struct AnchorPath * apath;

    if ( (apath = AllocMem (sizeof (struct AnchorPath) + PATH_SIZE,
	    MEMF_CLEAR))
	)
    {
	apath->ap_Strlen = PATH_SIZE;

	if (MatchFirst (wc, apath) == 0)
	{
	    do
	    {
		o = variable_buffer_output (o, apath->ap_Buf,
			strlen (apath->ap_Buf));
		o = variable_buffer_output (o, " ",1);
	    } while (MatchNext (apath) == 0);
	}

	MatchEnd (apath);
	FreeMem (apath, sizeof (struct AnchorPath) + PATH_SIZE);
    }

    return o;
}

