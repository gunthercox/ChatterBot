/* Error handling for Windows
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

#include <windows.h>
#include "w32err.h"

/*
 * Description: the windows32 version of perror()
 *
 * Returns:  a pointer to a static error
 *
 * Notes/Dependencies:  I got this from
 *      comp.os.ms-windows.programmer.win32
 */
char *
map_windows32_error_to_string (DWORD ercode) {
/* __declspec (thread) necessary if you will use multiple threads on MSVC */
#ifdef _MSC_VER
__declspec (thread) static char szMessageBuffer[128];
#else
static char szMessageBuffer[128];
#endif
	/* Fill message buffer with a default message in
	 * case FormatMessage fails
	 */
    wsprintf (szMessageBuffer, "Error %ld\n", ercode);

	/*
	 *  Special code for winsock error handling.
	 */
	if (ercode > WSABASEERR) {
		HMODULE hModule = GetModuleHandle("wsock32");
		if (hModule != NULL) {
			FormatMessage(FORMAT_MESSAGE_FROM_HMODULE,
				hModule,
				ercode,
				LANG_NEUTRAL,
				szMessageBuffer,
				sizeof(szMessageBuffer),
				NULL);
			FreeLibrary(hModule);
		}
	} else {
		/*
		 *  Default system message handling
		 */
    	FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM,
                  NULL,
                  ercode,
                  LANG_NEUTRAL,
                  szMessageBuffer,
                  sizeof(szMessageBuffer),
                  NULL);
	}
    return szMessageBuffer;
}

