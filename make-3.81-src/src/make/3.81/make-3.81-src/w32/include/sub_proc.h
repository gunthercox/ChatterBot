/* Definitions for Windows process invocation.
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

#ifndef SUB_PROC_H
#define SUB_PROC_H

/*
 * Component Name:
 *
 * $Date: 2006/02/11 22:16:05 $
 *
 * $Source: /sources/make/make/w32/include/sub_proc.h,v $
 *
 * $Id: sub_proc.h,v 1.8 2006/02/11 22:16:05 psmith Exp $
 */

#define EXTERN_DECL(entry, args) extern entry args
#define VOID_DECL void

EXTERN_DECL(HANDLE process_init, (VOID_DECL));
EXTERN_DECL(HANDLE process_init_fd, (HANDLE stdinh, HANDLE stdouth,
	HANDLE stderrh));
EXTERN_DECL(long process_begin, (HANDLE proc, char **argv, char **envp,
	char *exec_path, char *as_user));
EXTERN_DECL(long process_pipe_io, (HANDLE proc, char *stdin_data,
	int stdin_data_len));
EXTERN_DECL(long process_file_io, (HANDLE proc));
EXTERN_DECL(void process_cleanup, (HANDLE proc));
EXTERN_DECL(HANDLE process_wait_for_any, (VOID_DECL));
EXTERN_DECL(void process_register, (HANDLE proc));
EXTERN_DECL(HANDLE process_easy, (char** argv, char** env));
EXTERN_DECL(BOOL process_kill, (HANDLE proc, int signal));
EXTERN_DECL(int process_used_slots, (VOID_DECL));

/* support routines */
EXTERN_DECL(long process_errno, (HANDLE proc));
EXTERN_DECL(long process_last_err, (HANDLE proc));
EXTERN_DECL(long process_exit_code, (HANDLE proc));
EXTERN_DECL(long process_signal, (HANDLE proc));
EXTERN_DECL(char * process_outbuf, (HANDLE proc));
EXTERN_DECL(char * process_errbuf, (HANDLE proc));
EXTERN_DECL(int process_outcnt, (HANDLE proc));
EXTERN_DECL(int process_errcnt, (HANDLE proc));
EXTERN_DECL(void process_pipes, (HANDLE proc, int pipes[3]));

#endif
