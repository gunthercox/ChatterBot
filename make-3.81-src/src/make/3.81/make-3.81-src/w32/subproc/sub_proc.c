/* Process handling for Windows.
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

#include <stdlib.h>
#include <stdio.h>
#include <process.h>  /* for msvc _beginthreadex, _endthreadex */
#include <signal.h>
#include <windows.h>

#include "sub_proc.h"
#include "proc.h"
#include "w32err.h"
#include "config.h"
#include "debug.h"

static char *make_command_line(char *shell_name, char *exec_path, char **argv);

typedef struct sub_process_t {
	int sv_stdin[2];
	int sv_stdout[2];
	int sv_stderr[2];
	int using_pipes;
	char *inp;
	DWORD incnt;
	char * volatile outp;
	volatile DWORD outcnt;
	char * volatile errp;
	volatile DWORD errcnt;
	int pid;
	int exit_code;
	int signal;
	long last_err;
	long lerrno;
} sub_process;

/* keep track of children so we can implement a waitpid-like routine */
static sub_process *proc_array[MAXIMUM_WAIT_OBJECTS];
static int proc_index = 0;
static int fake_exits_pending = 0;

/*
 * When a process has been waited for, adjust the wait state
 * array so that we don't wait for it again
 */
static void
process_adjust_wait_state(sub_process* pproc)
{
	int i;

	if (!proc_index)
		return;

	for (i = 0; i < proc_index; i++)
		if (proc_array[i]->pid == pproc->pid)
			break;

	if (i < proc_index) {
		proc_index--;
		if (i != proc_index)
			memmove(&proc_array[i], &proc_array[i+1],
				(proc_index-i) * sizeof(sub_process*));
		proc_array[proc_index] = NULL;
	}
}

/*
 * Waits for any of the registered child processes to finish.
 */
static sub_process *
process_wait_for_any_private(void)
{
	HANDLE handles[MAXIMUM_WAIT_OBJECTS];
	DWORD retval, which;
	int i;

	if (!proc_index)
		return NULL;

	/* build array of handles to wait for */
	for (i = 0; i < proc_index; i++) {
		handles[i] = (HANDLE) proc_array[i]->pid;

		if (fake_exits_pending && proc_array[i]->exit_code)
			break;
	}

	/* wait for someone to exit */
	if (!fake_exits_pending) {
		retval = WaitForMultipleObjects(proc_index, handles, FALSE, INFINITE);
		which = retval - WAIT_OBJECT_0;
	} else {
		fake_exits_pending--;
		retval = !WAIT_FAILED;
		which = i;
	}

	/* return pointer to process */
	if (retval != WAIT_FAILED) {
		sub_process* pproc = proc_array[which];
		process_adjust_wait_state(pproc);
		return pproc;
	} else
		return NULL;
}

/*
 * Terminate a process.
 */
BOOL
process_kill(HANDLE proc, int signal)
{
	sub_process* pproc = (sub_process*) proc;
	pproc->signal = signal;
	return (TerminateProcess((HANDLE) pproc->pid, signal));
}

/*
 * Use this function to register processes you wish to wait for by
 * calling process_file_io(NULL) or process_wait_any(). This must be done
 * because it is possible for callers of this library to reuse the same
 * handle for multiple processes launches :-(
 */
void
process_register(HANDLE proc)
{
	if (proc_index < MAXIMUM_WAIT_OBJECTS)
		proc_array[proc_index++] = (sub_process *) proc;
}

/*
 * Return the number of processes that we are still waiting for.
 */
int
process_used_slots(void)
{
	return proc_index;
}

/*
 * Public function which works kind of like waitpid(). Wait for any
 * of the children to die and return results. To call this function,
 * you must do 1 of things:
 *
 * 	x = process_easy(...);
 *
 * or
 *
 *	x = process_init_fd();
 *	process_register(x);
 *
 * or
 *
 *	x = process_init();
 *	process_register(x);
 *
 * You must NOT then call process_pipe_io() because this function is
 * not capable of handling automatic notification of any child
 * death.
 */

HANDLE
process_wait_for_any(void)
{
	sub_process* pproc = process_wait_for_any_private();

	if (!pproc)
		return NULL;
	else {
		/*
		 * Ouch! can't tell caller if this fails directly. Caller
		 * will have to use process_last_err()
                 */
		(void) process_file_io(pproc);
		return ((HANDLE) pproc);
	}
}

long
process_signal(HANDLE proc)
{
        if (proc == INVALID_HANDLE_VALUE) return 0;
        return (((sub_process *)proc)->signal);
}

long
process_last_err(HANDLE proc)
{
        if (proc == INVALID_HANDLE_VALUE) return ERROR_INVALID_HANDLE;
	return (((sub_process *)proc)->last_err);
}

long
process_exit_code(HANDLE proc)
{
        if (proc == INVALID_HANDLE_VALUE) return EXIT_FAILURE;
	return (((sub_process *)proc)->exit_code);
}

/*
2006-02:
All the following functions are currently unused.
All of them would crash gmake if called with argument INVALID_HANDLE_VALUE.
Hence whoever wants to use one of this functions must invent and implement
a reasonable error handling for this function.

char *
process_outbuf(HANDLE proc)
{
	return (((sub_process *)proc)->outp);
}

char *
process_errbuf(HANDLE proc)
{
	return (((sub_process *)proc)->errp);
}

int
process_outcnt(HANDLE proc)
{
	return (((sub_process *)proc)->outcnt);
}

int
process_errcnt(HANDLE proc)
{
	return (((sub_process *)proc)->errcnt);
}

void
process_pipes(HANDLE proc, int pipes[3])
{
	pipes[0] = ((sub_process *)proc)->sv_stdin[0];
	pipes[1] = ((sub_process *)proc)->sv_stdout[0];
	pipes[2] = ((sub_process *)proc)->sv_stderr[0];
	return;
}
*/

	HANDLE
process_init()
{
	sub_process *pproc;
	/*
	 * open file descriptors for attaching stdin/stdout/sterr
	 */
	HANDLE stdin_pipes[2];
	HANDLE stdout_pipes[2];
	HANDLE stderr_pipes[2];
	SECURITY_ATTRIBUTES inherit;
	BYTE sd[SECURITY_DESCRIPTOR_MIN_LENGTH];

	pproc = malloc(sizeof(*pproc));
	memset(pproc, 0, sizeof(*pproc));

	/* We can't use NULL for lpSecurityDescriptor because that
	   uses the default security descriptor of the calling process.
	   Instead we use a security descriptor with no DACL.  This
	   allows nonrestricted access to the associated objects. */

	if (!InitializeSecurityDescriptor((PSECURITY_DESCRIPTOR)(&sd),
					  SECURITY_DESCRIPTOR_REVISION)) {
		pproc->last_err = GetLastError();
		pproc->lerrno = E_SCALL;
		return((HANDLE)pproc);
	}

	inherit.nLength = sizeof(inherit);
	inherit.lpSecurityDescriptor = (PSECURITY_DESCRIPTOR)(&sd);
	inherit.bInheritHandle = TRUE;

	// By convention, parent gets pipe[0], and child gets pipe[1]
	// This means the READ side of stdin pipe goes into pipe[1]
	// and the WRITE side of the stdout and stderr pipes go into pipe[1]
	if (CreatePipe( &stdin_pipes[1], &stdin_pipes[0], &inherit, 0) == FALSE ||
	CreatePipe( &stdout_pipes[0], &stdout_pipes[1], &inherit, 0) == FALSE ||
	CreatePipe( &stderr_pipes[0], &stderr_pipes[1], &inherit, 0) == FALSE) {

		pproc->last_err = GetLastError();
		pproc->lerrno = E_SCALL;
		return((HANDLE)pproc);
	}

	//
	// Mark the parent sides of the pipes as non-inheritable
	//
	if (SetHandleInformation(stdin_pipes[0],
				HANDLE_FLAG_INHERIT, 0) == FALSE ||
		SetHandleInformation(stdout_pipes[0],
				HANDLE_FLAG_INHERIT, 0) == FALSE ||
		SetHandleInformation(stderr_pipes[0],
				HANDLE_FLAG_INHERIT, 0) == FALSE) {

		pproc->last_err = GetLastError();
		pproc->lerrno = E_SCALL;
		return((HANDLE)pproc);
	}
	pproc->sv_stdin[0]  = (int) stdin_pipes[0];
	pproc->sv_stdin[1]  = (int) stdin_pipes[1];
	pproc->sv_stdout[0] = (int) stdout_pipes[0];
	pproc->sv_stdout[1] = (int) stdout_pipes[1];
	pproc->sv_stderr[0] = (int) stderr_pipes[0];
	pproc->sv_stderr[1] = (int) stderr_pipes[1];

	pproc->using_pipes = 1;

	pproc->lerrno = 0;

	return((HANDLE)pproc);
}


	HANDLE
process_init_fd(HANDLE stdinh, HANDLE stdouth, HANDLE stderrh)
{
	sub_process *pproc;

	pproc = malloc(sizeof(*pproc));
	memset(pproc, 0, sizeof(*pproc));

	/*
	 * Just pass the provided file handles to the 'child side' of the
	 * pipe, bypassing pipes altogether.
	 */
	pproc->sv_stdin[1]  = (int) stdinh;
	pproc->sv_stdout[1] = (int) stdouth;
	pproc->sv_stderr[1] = (int) stderrh;

	pproc->last_err = pproc->lerrno = 0;

	return((HANDLE)pproc);
}


static HANDLE
find_file(char *exec_path, LPOFSTRUCT file_info)
{
	HANDLE exec_handle;
	char *fname;
	char *ext;

	fname = malloc(strlen(exec_path) + 5);
	strcpy(fname, exec_path);
	ext = fname + strlen(fname);

	strcpy(ext, ".exe");
	if ((exec_handle = (HANDLE)OpenFile(fname, file_info,
			OF_READ | OF_SHARE_COMPAT)) != (HANDLE)HFILE_ERROR) {
		free(fname);
		return(exec_handle);
	}

	strcpy(ext, ".cmd");
	if ((exec_handle = (HANDLE)OpenFile(fname, file_info,
			OF_READ | OF_SHARE_COMPAT)) != (HANDLE)HFILE_ERROR) {
		free(fname);
		return(exec_handle);
	}

	strcpy(ext, ".bat");
	if ((exec_handle = (HANDLE)OpenFile(fname, file_info,
			OF_READ | OF_SHARE_COMPAT)) != (HANDLE)HFILE_ERROR) {
		free(fname);
		return(exec_handle);
	}

	/* should .com come before this case? */
	if ((exec_handle = (HANDLE)OpenFile(exec_path, file_info,
			OF_READ | OF_SHARE_COMPAT)) != (HANDLE)HFILE_ERROR) {
		free(fname);
		return(exec_handle);
	}

	strcpy(ext, ".com");
	if ((exec_handle = (HANDLE)OpenFile(fname, file_info,
			OF_READ | OF_SHARE_COMPAT)) != (HANDLE)HFILE_ERROR) {
		free(fname);
		return(exec_handle);
	}

	free(fname);
	return(exec_handle);
}


/*
 * Description:   Create the child process to be helped
 *
 * Returns: success <=> 0
 *
 * Notes/Dependencies:
 */
long
process_begin(
	HANDLE proc,
	char **argv,
	char **envp,
	char *exec_path,
	char *as_user)
{
	sub_process *pproc = (sub_process *)proc;
	char *shell_name = 0;
	int file_not_found=0;
	HANDLE exec_handle;
	char buf[256];
	DWORD bytes_returned;
	DWORD flags;
	char *command_line;
	STARTUPINFO startInfo;
	PROCESS_INFORMATION procInfo;
	char *envblk=NULL;
	OFSTRUCT file_info;


	/*
	 *  Shell script detection...  if the exec_path starts with #! then
	 *  we want to exec shell-script-name exec-path, not just exec-path
	 *  NT doesn't recognize #!/bin/sh or #!/etc/Tivoli/bin/perl.  We do not
	 *  hard-code the path to the shell or perl or whatever:  Instead, we
	 *  assume it's in the path somewhere (generally, the NT tools
	 *  bin directory)
	 *  We use OpenFile here because it is capable of searching the Path.
	 */

	exec_handle = find_file(exec_path, &file_info);

	/*
	 * If we couldn't open the file, just assume that Windows32 will be able
	 * to find and execute it.
	 */
	if (exec_handle == (HANDLE)HFILE_ERROR) {
		file_not_found++;
	}
	else {
		/* Attempt to read the first line of the file */
		if (ReadFile( exec_handle,
				buf, sizeof(buf) - 1, /* leave room for trailing NULL */
				&bytes_returned, 0) == FALSE || bytes_returned < 2) {

			pproc->last_err = GetLastError();
			pproc->lerrno = E_IO;
			CloseHandle(exec_handle);
			return(-1);
		}
		if (buf[0] == '#' && buf[1] == '!') {
			/*
			 *  This is a shell script...  Change the command line from
			 *	exec_path args to shell_name exec_path args
			 */
			char *p;

			/*  Make sure buf is NULL terminated */
			buf[bytes_returned] = 0;
			/*
			 * Depending on the file system type, etc. the first line
			 * of the shell script may end with newline or newline-carriage-return
			 * Whatever it ends with, cut it off.
			 */
			p= strchr(buf, '\n');
			if (p)
				*p = 0;
			p = strchr(buf, '\r');
			if (p)
				*p = 0;

			/*
			 *  Find base name of shell
			 */
			shell_name = strrchr( buf, '/');
			if (shell_name) {
				shell_name++;
			} else {
				shell_name = &buf[2];/* skipping "#!" */
			}

		}
		CloseHandle(exec_handle);
	}

	flags = 0;

	if (file_not_found)
		command_line = make_command_line( shell_name, exec_path, argv);
	else
		command_line = make_command_line( shell_name, file_info.szPathName,
				 argv);

	if ( command_line == NULL ) {
		pproc->last_err = 0;
		pproc->lerrno = E_NO_MEM;
		return(-1);
	}

	if (envp) {
		if (arr2envblk(envp, &envblk) ==FALSE) {
			pproc->last_err = 0;
			pproc->lerrno = E_NO_MEM;
			free( command_line );
			return(-1);
		}
	}

	if ((shell_name) || (file_not_found)) {
		exec_path = 0;	/* Search for the program in %Path% */
	} else {
		exec_path = file_info.szPathName;
	}

	/*
	 *  Set up inherited stdin, stdout, stderr for child
	 */
	GetStartupInfo(&startInfo);
	startInfo.dwFlags = STARTF_USESTDHANDLES;
	startInfo.lpReserved = 0;
	startInfo.cbReserved2 = 0;
	startInfo.lpReserved2 = 0;
	startInfo.lpTitle = shell_name ? shell_name : exec_path;
	startInfo.hStdInput = (HANDLE)pproc->sv_stdin[1];
	startInfo.hStdOutput = (HANDLE)pproc->sv_stdout[1];
	startInfo.hStdError = (HANDLE)pproc->sv_stderr[1];

	if (as_user) {
		if (envblk) free(envblk);
		return -1;
	} else {
		DB (DB_JOBS, ("CreateProcess(%s,%s,...)\n",
			exec_path ? exec_path : "NULL",
			command_line ? command_line : "NULL"));
		if (CreateProcess(
			exec_path,
			command_line,
			NULL,
			0, /* default security attributes for thread */
			TRUE, /* inherit handles (e.g. helper pipes, oserv socket) */
			flags,
			envblk,
			0, /* default starting directory */
			&startInfo,
			&procInfo) == FALSE) {

			pproc->last_err = GetLastError();
			pproc->lerrno = E_FORK;
			fprintf(stderr, "process_begin: CreateProcess(%s, %s, ...) failed.\n",
                                exec_path ? exec_path : "NULL", command_line);
			if (envblk) free(envblk);
			free( command_line );
			return(-1);
		}
	}

	pproc->pid = (int)procInfo.hProcess;
	/* Close the thread handle -- we'll just watch the process */
	CloseHandle(procInfo.hThread);

	/* Close the halves of the pipes we don't need */
        CloseHandle((HANDLE)pproc->sv_stdin[1]);
        CloseHandle((HANDLE)pproc->sv_stdout[1]);
        CloseHandle((HANDLE)pproc->sv_stderr[1]);
        pproc->sv_stdin[1] = 0;
        pproc->sv_stdout[1] = 0;
        pproc->sv_stderr[1] = 0;

	free( command_line );
	if (envblk) free(envblk);
	pproc->lerrno=0;
	return 0;
}



static DWORD
proc_stdin_thread(sub_process *pproc)
{
	DWORD in_done;
	for (;;) {
		if (WriteFile( (HANDLE) pproc->sv_stdin[0], pproc->inp, pproc->incnt,
					 &in_done, NULL) == FALSE)
			_endthreadex(0);
		// This if should never be true for anonymous pipes, but gives
		// us a chance to change I/O mechanisms later
		if (in_done < pproc->incnt) {
			pproc->incnt -= in_done;
			pproc->inp += in_done;
		} else {
			_endthreadex(0);
		}
	}
	return 0; // for compiler warnings only.. not reached
}

static DWORD
proc_stdout_thread(sub_process *pproc)
{
	DWORD bufsize = 1024;
	char c;
	DWORD nread;
	pproc->outp = malloc(bufsize);
	if (pproc->outp == NULL)
		_endthreadex(0);
	pproc->outcnt = 0;

	for (;;) {
		if (ReadFile( (HANDLE)pproc->sv_stdout[0], &c, 1, &nread, NULL)
					== FALSE) {
/*			map_windows32_error_to_string(GetLastError());*/
			_endthreadex(0);
		}
		if (nread == 0)
			_endthreadex(0);
		if (pproc->outcnt + nread > bufsize) {
			bufsize += nread + 512;
			pproc->outp = realloc(pproc->outp, bufsize);
			if (pproc->outp == NULL) {
				pproc->outcnt = 0;
				_endthreadex(0);
			}
		}
		pproc->outp[pproc->outcnt++] = c;
	}
	return 0;
}

static DWORD
proc_stderr_thread(sub_process *pproc)
{
	DWORD bufsize = 1024;
	char c;
	DWORD nread;
	pproc->errp = malloc(bufsize);
	if (pproc->errp == NULL)
		_endthreadex(0);
	pproc->errcnt = 0;

	for (;;) {
		if (ReadFile( (HANDLE)pproc->sv_stderr[0], &c, 1, &nread, NULL) == FALSE) {
			map_windows32_error_to_string(GetLastError());
			_endthreadex(0);
		}
		if (nread == 0)
			_endthreadex(0);
		if (pproc->errcnt + nread > bufsize) {
			bufsize += nread + 512;
			pproc->errp = realloc(pproc->errp, bufsize);
			if (pproc->errp == NULL) {
				pproc->errcnt = 0;
				_endthreadex(0);
			}
		}
		pproc->errp[pproc->errcnt++] = c;
	}
	return 0;
}


/*
 * Purpose: collects output from child process and returns results
 *
 * Description:
 *
 * Returns:
 *
 * Notes/Dependencies:
 */
	long
process_pipe_io(
	HANDLE proc,
	char *stdin_data,
	int stdin_data_len)
{
	sub_process *pproc = (sub_process *)proc;
	bool_t stdin_eof = FALSE, stdout_eof = FALSE, stderr_eof = FALSE;
	HANDLE childhand = (HANDLE) pproc->pid;
	HANDLE tStdin = NULL, tStdout = NULL, tStderr = NULL;
	unsigned int dwStdin, dwStdout, dwStderr;
	HANDLE wait_list[4];
	DWORD wait_count;
	DWORD wait_return;
	HANDLE ready_hand;
	bool_t child_dead = FALSE;
	BOOL GetExitCodeResult;

	/*
	 *  Create stdin thread, if needed
	 */
	pproc->inp = stdin_data;
	pproc->incnt = stdin_data_len;
	if (!pproc->inp) {
		stdin_eof = TRUE;
		CloseHandle((HANDLE)pproc->sv_stdin[0]);
		pproc->sv_stdin[0] = 0;
	} else {
		tStdin = (HANDLE) _beginthreadex( 0, 1024,
			(unsigned (__stdcall *) (void *))proc_stdin_thread,
						  pproc, 0, &dwStdin);
		if (tStdin == 0) {
			pproc->last_err = GetLastError();
			pproc->lerrno = E_SCALL;
			goto done;
		}
	}

	/*
	 *   Assume child will produce stdout and stderr
	 */
	tStdout = (HANDLE) _beginthreadex( 0, 1024,
		(unsigned (__stdcall *) (void *))proc_stdout_thread, pproc, 0,
		&dwStdout);
	tStderr = (HANDLE) _beginthreadex( 0, 1024,
		(unsigned (__stdcall *) (void *))proc_stderr_thread, pproc, 0,
		&dwStderr);

	if (tStdout == 0 || tStderr == 0) {

		pproc->last_err = GetLastError();
		pproc->lerrno = E_SCALL;
		goto done;
	}


	/*
	 *  Wait for all I/O to finish and for the child process to exit
	 */

	while (!stdin_eof || !stdout_eof || !stderr_eof || !child_dead) {
		wait_count = 0;
		if (!stdin_eof) {
			wait_list[wait_count++] = tStdin;
		}
		if (!stdout_eof) {
			wait_list[wait_count++] = tStdout;
		}
		if (!stderr_eof) {
			wait_list[wait_count++] = tStderr;
		}
		if (!child_dead) {
			wait_list[wait_count++] = childhand;
		}

		wait_return = WaitForMultipleObjects(wait_count, wait_list,
			 FALSE, /* don't wait for all: one ready will do */
			 child_dead? 1000 :INFINITE); /* after the child dies, subthreads have
			 	one second to collect all remaining output */

		if (wait_return == WAIT_FAILED) {
/*			map_windows32_error_to_string(GetLastError());*/
			pproc->last_err = GetLastError();
			pproc->lerrno = E_SCALL;
			goto done;
		}

		ready_hand = wait_list[wait_return - WAIT_OBJECT_0];

		if (ready_hand == tStdin) {
			CloseHandle((HANDLE)pproc->sv_stdin[0]);
			pproc->sv_stdin[0] = 0;
			CloseHandle(tStdin);
			tStdin = 0;
			stdin_eof = TRUE;

		} else if (ready_hand == tStdout) {

		  	CloseHandle((HANDLE)pproc->sv_stdout[0]);
			pproc->sv_stdout[0] = 0;
			CloseHandle(tStdout);
			tStdout = 0;
		  	stdout_eof = TRUE;

		} else if (ready_hand == tStderr) {

			CloseHandle((HANDLE)pproc->sv_stderr[0]);
			pproc->sv_stderr[0] = 0;
			CloseHandle(tStderr);
			tStderr = 0;
			stderr_eof = TRUE;

		} else if (ready_hand == childhand) {

			DWORD ierr;
			GetExitCodeResult = GetExitCodeProcess(childhand, &ierr);
			if (ierr == CONTROL_C_EXIT) {
				pproc->signal = SIGINT;
			} else {
				pproc->exit_code = ierr;
			}
			if (GetExitCodeResult == FALSE) {
				pproc->last_err = GetLastError();
				pproc->lerrno = E_SCALL;
				goto done;
			}
			child_dead = TRUE;

		} else {

			/* ?? Got back a handle we didn't query ?? */
			pproc->last_err = 0;
			pproc->lerrno = E_FAIL;
			goto done;
		}
	}

 done:
	if (tStdin != 0)
		CloseHandle(tStdin);
	if (tStdout != 0)
		CloseHandle(tStdout);
	if (tStderr != 0)
		CloseHandle(tStderr);

	if (pproc->lerrno)
		return(-1);
	else
		return(0);

}

/*
 * Purpose: collects output from child process and returns results
 *
 * Description:
 *
 * Returns:
 *
 * Notes/Dependencies:
 */
	long
process_file_io(
	HANDLE proc)
{
	sub_process *pproc;
	HANDLE childhand;
	DWORD wait_return;
	BOOL GetExitCodeResult;
        DWORD ierr;

	if (proc == NULL)
		pproc = process_wait_for_any_private();
	else
		pproc = (sub_process *)proc;

	/* some sort of internal error */
	if (!pproc)
		return -1;

	childhand = (HANDLE) pproc->pid;

	/*
	 * This function is poorly named, and could also be used just to wait
	 * for child death if you're doing your own pipe I/O.  If that is
	 * the case, close the pipe handles here.
	 */
	if (pproc->sv_stdin[0]) {
		CloseHandle((HANDLE)pproc->sv_stdin[0]);
		pproc->sv_stdin[0] = 0;
	}
	if (pproc->sv_stdout[0]) {
		CloseHandle((HANDLE)pproc->sv_stdout[0]);
		pproc->sv_stdout[0] = 0;
	}
	if (pproc->sv_stderr[0]) {
		CloseHandle((HANDLE)pproc->sv_stderr[0]);
		pproc->sv_stderr[0] = 0;
	}

	/*
	 *  Wait for the child process to exit
	 */

	wait_return = WaitForSingleObject(childhand, INFINITE);

	if (wait_return != WAIT_OBJECT_0) {
/*		map_windows32_error_to_string(GetLastError());*/
		pproc->last_err = GetLastError();
		pproc->lerrno = E_SCALL;
		goto done2;
	}

	GetExitCodeResult = GetExitCodeProcess(childhand, &ierr);
	if (ierr == CONTROL_C_EXIT) {
		pproc->signal = SIGINT;
	} else {
		pproc->exit_code = ierr;
	}
	if (GetExitCodeResult == FALSE) {
		pproc->last_err = GetLastError();
		pproc->lerrno = E_SCALL;
	}

done2:
	if (pproc->lerrno)
		return(-1);
	else
		return(0);

}

/*
 * Description:  Clean up any leftover handles, etc.  It is up to the
 * caller to manage and free the input, ouput, and stderr buffers.
 */
	void
process_cleanup(
	HANDLE proc)
{
	sub_process *pproc = (sub_process *)proc;
	int i;

	if (pproc->using_pipes) {
		for (i= 0; i <= 1; i++) {
			if ((HANDLE)pproc->sv_stdin[i])
				CloseHandle((HANDLE)pproc->sv_stdin[i]);
			if ((HANDLE)pproc->sv_stdout[i])
				CloseHandle((HANDLE)pproc->sv_stdout[i]);
			if ((HANDLE)pproc->sv_stderr[i])
				CloseHandle((HANDLE)pproc->sv_stderr[i]);
		}
	}
	if ((HANDLE)pproc->pid)
		CloseHandle((HANDLE)pproc->pid);

	free(pproc);
}


/*
 * Description:
 *	 Create a command line buffer to pass to CreateProcess
 *
 * Returns:  the buffer or NULL for failure
 *	Shell case:  sh_name a:/full/path/to/script argv[1] argv[2] ...
 *  Otherwise:   argv[0] argv[1] argv[2] ...
 *
 * Notes/Dependencies:
 *   CreateProcess does not take an argv, so this command creates a
 *   command line for the executable.
 */

static char *
make_command_line( char *shell_name, char *full_exec_path, char **argv)
{
	int		argc = 0;
	char**		argvi;
	int*		enclose_in_quotes = NULL;
	int*		enclose_in_quotes_i;
	unsigned int	bytes_required = 0;
	char*		command_line;
	char*		command_line_i;
	int  cygwin_mode = 0; /* HAVE_CYGWIN_SHELL */
	int have_sh = 0; /* HAVE_CYGWIN_SHELL */

#ifdef HAVE_CYGWIN_SHELL
	have_sh = (shell_name != NULL || strstr(full_exec_path, "sh.exe"));
	cygwin_mode = 1;
#endif

	if (shell_name && full_exec_path) {
		bytes_required
		  = strlen(shell_name) + 1 + strlen(full_exec_path);
		/*
		 * Skip argv[0] if any, when shell_name is given.
		 */
		if (*argv) argv++;
		/*
		 * Add one for the intervening space.
		 */
		if (*argv) bytes_required++;
	}

	argvi = argv;
	while (*(argvi++)) argc++;

	if (argc) {
		enclose_in_quotes = (int*) calloc(1, argc * sizeof(int));

		if (!enclose_in_quotes) {
			return NULL;
		}
	}

	/* We have to make one pass through each argv[i] to see if we need
	 * to enclose it in ", so we might as well figure out how much
	 * memory we'll need on the same pass.
	 */

	argvi = argv;
	enclose_in_quotes_i = enclose_in_quotes;
	while(*argvi) {
		char* p = *argvi;
		unsigned int backslash_count = 0;

		/*
		 * We have to enclose empty arguments in ".
		 */
		if (!(*p)) *enclose_in_quotes_i = 1;

		while(*p) {
			switch (*p) {
			case '\"':
				/*
				 * We have to insert a backslash for each "
				 * and each \ that precedes the ".
				 */
				bytes_required += (backslash_count + 1);
				backslash_count = 0;
				break;

#if !defined(HAVE_MKS_SHELL) && !defined(HAVE_CYGWIN_SHELL)
			case '\\':
				backslash_count++;
				break;
#endif
	/*
	 * At one time we set *enclose_in_quotes_i for '*' or '?' to suppress
	 * wildcard expansion in programs linked with MSVC's SETARGV.OBJ so
	 * that argv in always equals argv out. This was removed.  Say you have
	 * such a program named glob.exe.  You enter
	 * glob '*'
	 * at the sh command prompt.  Obviously the intent is to make glob do the
	 * wildcarding instead of sh.  If we set *enclose_in_quotes_i for '*' or '?',
	 * then the command line that glob would see would be
	 * glob "*"
	 * and the _setargv in SETARGV.OBJ would _not_ expand the *.
	 */
			case ' ':
			case '\t':
				*enclose_in_quotes_i = 1;
				/* fall through */

			default:
				backslash_count = 0;
				break;
			}

			/*
			 * Add one for each character in argv[i].
			 */
			bytes_required++;

			p++;
		}

		if (*enclose_in_quotes_i) {
			/*
			 * Add one for each enclosing ",
			 * and one for each \ that precedes the
			 * closing ".
			 */
			bytes_required += (backslash_count + 2);
		}

		/*
		 * Add one for the intervening space.
		 */
		if (*(++argvi)) bytes_required++;
		enclose_in_quotes_i++;
	}

	/*
	 * Add one for the terminating NULL.
	 */
	bytes_required++;

	command_line = (char*) malloc(bytes_required);

	if (!command_line) {
		if (enclose_in_quotes) free(enclose_in_quotes);
		return NULL;
	}

	command_line_i = command_line;

	if (shell_name && full_exec_path) {
		while(*shell_name) {
			*(command_line_i++) = *(shell_name++);
		}

		*(command_line_i++) = ' ';

		while(*full_exec_path) {
			*(command_line_i++) = *(full_exec_path++);
		}

		if (*argv) {
			*(command_line_i++) = ' ';
		}
	}

	argvi = argv;
	enclose_in_quotes_i = enclose_in_quotes;

	while(*argvi) {
		char* p = *argvi;
		unsigned int backslash_count = 0;

		if (*enclose_in_quotes_i) {
			*(command_line_i++) = '\"';
		}

		while(*p) {
			if (*p == '\"') {
				if (cygwin_mode && have_sh) { /* HAVE_CYGWIN_SHELL */
					/* instead of a \", cygwin likes "" */
					*(command_line_i++) = '\"';
				} else {

				/*
				 * We have to insert a backslash for the "
				 * and each \ that precedes the ".
				 */
				backslash_count++;

				while(backslash_count) {
					*(command_line_i++) = '\\';
					backslash_count--;
				};
				}
#if !defined(HAVE_MKS_SHELL) && !defined(HAVE_CYGWIN_SHELL)
			} else if (*p == '\\') {
				backslash_count++;
			} else {
				backslash_count = 0;
#endif
			}

			/*
			 * Copy the character.
			 */
			*(command_line_i++) = *(p++);
		}

		if (*enclose_in_quotes_i) {
#if !defined(HAVE_MKS_SHELL) && !defined(HAVE_CYGWIN_SHELL)
			/*
			 * Add one \ for each \ that precedes the
			 * closing ".
			 */
			while(backslash_count--) {
				*(command_line_i++) = '\\';
			};
#endif
			*(command_line_i++) = '\"';
		}

		/*
		 * Append an intervening space.
		 */
		if (*(++argvi)) {
			*(command_line_i++) = ' ';
		}

		enclose_in_quotes_i++;
	}

	/*
	 * Append the terminating NULL.
	 */
	*command_line_i = '\0';

	if (enclose_in_quotes) free(enclose_in_quotes);
	return command_line;
}

/*
 * Description: Given an argv and optional envp, launch the process
 *              using the default stdin, stdout, and stderr handles.
 *              Also, register process so that process_wait_for_any_private()
 *		can be used via process_file_io(NULL) or
 *		process_wait_for_any().
 *
 * Returns:
 *
 * Notes/Dependencies:
 */
HANDLE
process_easy(
	char **argv,
	char **envp)
{
  HANDLE hIn;
  HANDLE hOut;
  HANDLE hErr;
  HANDLE hProcess;

  if (proc_index >= MAXIMUM_WAIT_OBJECTS) {
	DB (DB_JOBS, ("process_easy: All process slots used up\n"));
	return INVALID_HANDLE_VALUE;
  }
  if (DuplicateHandle(GetCurrentProcess(),
                      GetStdHandle(STD_INPUT_HANDLE),
                      GetCurrentProcess(),
                      &hIn,
                      0,
                      TRUE,
                      DUPLICATE_SAME_ACCESS) == FALSE) {
    fprintf(stderr,
            "process_easy: DuplicateHandle(In) failed (e=%ld)\n",
            GetLastError());
    return INVALID_HANDLE_VALUE;
  }
  if (DuplicateHandle(GetCurrentProcess(),
                      GetStdHandle(STD_OUTPUT_HANDLE),
                      GetCurrentProcess(),
                      &hOut,
                      0,
                      TRUE,
                      DUPLICATE_SAME_ACCESS) == FALSE) {
    fprintf(stderr,
           "process_easy: DuplicateHandle(Out) failed (e=%ld)\n",
           GetLastError());
    return INVALID_HANDLE_VALUE;
  }
  if (DuplicateHandle(GetCurrentProcess(),
                      GetStdHandle(STD_ERROR_HANDLE),
                      GetCurrentProcess(),
                      &hErr,
                      0,
                      TRUE,
                      DUPLICATE_SAME_ACCESS) == FALSE) {
    fprintf(stderr,
            "process_easy: DuplicateHandle(Err) failed (e=%ld)\n",
            GetLastError());
    return INVALID_HANDLE_VALUE;
  }

  hProcess = process_init_fd(hIn, hOut, hErr);

  if (process_begin(hProcess, argv, envp, argv[0], NULL)) {
    fake_exits_pending++;
    /* process_begin() failed: make a note of that.  */
    if (!((sub_process*) hProcess)->last_err)
      ((sub_process*) hProcess)->last_err = -1;
    ((sub_process*) hProcess)->exit_code = process_last_err(hProcess);

    /* close up unused handles */
    CloseHandle(hIn);
    CloseHandle(hOut);
    CloseHandle(hErr);
  }

  process_register(hProcess);

  return hProcess;
}
