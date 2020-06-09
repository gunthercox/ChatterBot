/* GNU Make remote job exportation interface to the Customs daemon.
   THIS CODE IS NOT SUPPORTED BY THE GNU PROJECT.
   Please do not send bug reports or questions about it to
   the Make maintainers.

Copyright (C) 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997,
1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006 Free Software
Foundation, Inc.
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
#include "job.h"
#include "filedef.h"
#include "commands.h"
#include "job.h"
#include "debug.h"

#include <sys/time.h>
#include <netdb.h>

#include "customs.h"

char *remote_description = "Customs";

/* File name of the Customs `export' client command.
   A full path name can be used to avoid some path-searching overhead.  */
#define	EXPORT_COMMAND	"/usr/local/bin/export"

/* ExportPermit gotten by start_remote_job_p, and used by start_remote_job.  */
static ExportPermit permit;

/* Normalized path name of the current directory.  */
static char *normalized_cwd;

/* Call once at startup even if no commands are run.  */

void
remote_setup (void)
{
}

/* Called before exit.  */

void
remote_cleanup (void)
{
}

/* Return nonzero if the next job should be done remotely.  */

int
start_remote_job_p (int first_p)
{
  static int inited = 0;
  int status;
  int njobs;

  if (!inited)
    {
      /* Allow the user to turn off job exportation (useful while he is
         debugging Customs, for example).  */
      if (getenv ("GNU_MAKE_NO_CUSTOMS") != 0)
        {
          inited = -1;
          return 0;
        }

      /* For secure Customs, make is installed setuid root and
	 Customs requires a privileged source port be used.  */
      make_access ();

      if (ISDB (DB_JOBS))
        Rpc_Debug(1);

      /* Ping the daemon once to see if it is there.  */
      inited = Customs_Ping () == RPC_SUCCESS ? 1 : -1;

      /* Return to normal user access.  */
      user_access ();

      if (starting_directory == 0)
	/* main couldn't figure it out.  */
	inited = -1;
      else
	{
	  /* Normalize the current directory path name to something
	     that should work on all machines exported to.  */

	  normalized_cwd = (char *) xmalloc (GET_PATH_MAX);
	  strcpy (normalized_cwd, starting_directory);
	  if (Customs_NormPath (normalized_cwd, GET_PATH_MAX) < 0)
	    /* Path normalization failure means using Customs
	       won't work, but it's not really an error.  */
	    inited = -1;
	}
    }

  if (inited < 0)
    return 0;

  njobs = job_slots_used;
  if (!first_p)
    njobs -= 1;		/* correction for being called from reap_children() */

  /* the first job should run locally, or, if the -l flag is given, we use
     that as clue as to how many local jobs should be scheduled locally */
  if (max_load_average < 0 && njobs == 0 || njobs < max_load_average)
     return 0;

  status = Customs_Host (EXPORT_SAME, &permit);
  if (status != RPC_SUCCESS)
    {
      DB (DB_JOBS, (_("Customs won't export: %s\n"),
                    Rpc_ErrorMessage (status)));
      return 0;
    }

  return !CUSTOMS_FAIL (&permit.addr);
}

/* Start a remote job running the command in ARGV, with environment from
   ENVP.  It gets standard input from STDIN_FD.  On failure, return
   nonzero.  On success, return zero, and set *USED_STDIN to nonzero if it
   will actually use STDIN_FD, zero if not, set *ID_PTR to a unique
   identification, and set *IS_REMOTE to nonzero if the job is remote, zero
   if it is local (meaning *ID_PTR is a process ID).  */

int
start_remote_job (char **argv, char **envp, int stdin_fd,
                  int *is_remote, int *id_ptr, int *used_stdin)
{
  char waybill[MAX_DATA_SIZE], msg[128];
  struct hostent *host;
  struct timeval timeout;
  struct sockaddr_in sin;
  int len;
  int retsock, retport, sock;
  Rpc_Stat status;
  int pid;

  /* Create the return socket.  */
  retsock = Rpc_UdpCreate (True, 0);
  if (retsock < 0)
    {
      error (NILF, "exporting: Couldn't create return socket.");
      return 1;
    }

  /* Get the return socket's port number.  */
  len = sizeof (sin);
  if (getsockname (retsock, (struct sockaddr *) &sin, &len) < 0)
    {
      (void) close (retsock);
      perror_with_name ("exporting: ", "getsockname");
      return 1;
    }
  retport = sin.sin_port;

  /* Create the TCP socket for talking to the remote child.  */
  sock = Rpc_TcpCreate (False, 0);

  /* Create a WayBill to give to the server.  */
  len = Customs_MakeWayBill (&permit, normalized_cwd, argv[0], argv,
			     envp, retport, waybill);

  /* Modify the waybill as if the remote child had done `child_access ()'.  */
  {
    WayBill *wb = (WayBill *) waybill;
    wb->ruid = wb->euid;
    wb->rgid = wb->egid;
  }

  /* Send the request to the server, timing out in 20 seconds.  */
  timeout.tv_usec = 0;
  timeout.tv_sec = 20;
  sin.sin_family = AF_INET;
  sin.sin_port = htons (Customs_Port ());
  sin.sin_addr = permit.addr;
  status = Rpc_Call (sock, &sin, (Rpc_Proc) CUSTOMS_IMPORT,
		     len, (Rpc_Opaque) waybill,
		     sizeof(msg), (Rpc_Opaque) msg,
		     1, &timeout);

  host = gethostbyaddr((char *)&permit.addr, sizeof(permit.addr), AF_INET);

  if (status != RPC_SUCCESS)
    {
      (void) close (retsock);
      (void) close (sock);
      error (NILF, "exporting to %s: %s",
             host ? host->h_name : inet_ntoa (permit.addr),
             Rpc_ErrorMessage (status));
      return 1;
    }
  else if (msg[0] != 'O' || msg[1] != 'k' || msg[2] != '\0')
    {
      (void) close (retsock);
      (void) close (sock);
      error (NILF, "exporting to %s: %s",
             host ? host->h_name : inet_ntoa (permit.addr),
             msg);
      return 1;
    }
  else
    {
      error (NILF, "*** exported to %s (id %u)",
	      host ? host->h_name : inet_ntoa (permit.addr),
	      permit.id);
    }

  fflush (stdout);
  fflush (stderr);

  pid = vfork ();
  if (pid < 0)
    {
      /* The fork failed!  */
      perror_with_name ("vfork", "");
      return 1;
    }
  else if (pid == 0)
    {
      /* Child side.  Run `export' to handle the connection.  */
      static char sock_buf[20], retsock_buf[20], id_buf[20];
      static char *new_argv[6] =
	{ EXPORT_COMMAND, "-id", sock_buf, retsock_buf, id_buf, 0 };

      /* Set up the arguments.  */
      (void) sprintf (sock_buf, "%d", sock);
      (void) sprintf (retsock_buf, "%d", retsock);
      (void) sprintf (id_buf, "%x", permit.id);

      /* Get the right stdin.  */
      if (stdin_fd != 0)
	(void) dup2 (stdin_fd, 0);

      /* Unblock signals in the child.  */
      unblock_sigs ();

      /* Run the command.  */
      exec_command (new_argv, envp);
    }

  /* Parent side.  Return the `export' process's ID.  */
  (void) close (retsock);
  (void) close (sock);
  *is_remote = 0;
  *id_ptr = pid;
  *used_stdin = 1;
  return 0;
}

/* Get the status of a dead remote child.  Block waiting for one to die
   if BLOCK is nonzero.  Set *EXIT_CODE_PTR to the exit status, *SIGNAL_PTR
   to the termination signal or zero if it exited normally, and *COREDUMP_PTR
   nonzero if it dumped core.  Return the ID of the child that died,
   0 if we would have to block and !BLOCK, or < 0 if there were none.  */

int
remote_status (int *exit_code_ptr, int *signal_ptr, int *coredump_ptr,
               int block)
{
  return -1;
}

/* Block asynchronous notification of remote child death.
   If this notification is done by raising the child termination
   signal, do not block that signal.  */
void
block_remote_children (void)
{
  return;
}

/* Restore asynchronous notification of remote child death.
   If this is done by raising the child termination signal,
   do not unblock that signal.  */
void
unblock_remote_children (void)
{
  return;
}

/* Send signal SIG to child ID.  Return 0 if successful, -1 if not.  */
int
remote_kill (int id, int sig)
{
  return -1;
}
