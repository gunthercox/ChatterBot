/* Definitions for managing subprocesses in GNU Make.
Copyright (C) 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001,
2002, 2003, 2004, 2005, 2006 Free Software Foundation, Inc.
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

#ifndef SEEN_JOB_H
#define SEEN_JOB_H

#ifdef HAVE_FCNTL_H
# include <fcntl.h>
#else
# include <sys/file.h>
#endif

/* How to set close-on-exec for a file descriptor.  */

#if !defined F_SETFD
# define CLOSE_ON_EXEC(_d)
#else
# ifndef FD_CLOEXEC
#  define FD_CLOEXEC 1
# endif
# define CLOSE_ON_EXEC(_d) (void) fcntl ((_d), F_SETFD, FD_CLOEXEC)
#endif

/* Structure describing a running or dead child process.  */

struct child
  {
    struct child *next;		/* Link in the chain.  */

    struct file *file;		/* File being remade.  */

    char **environment;		/* Environment for commands.  */

    char **command_lines;	/* Array of variable-expanded cmd lines.  */
    unsigned int command_line;	/* Index into above.  */
    char *command_ptr;		/* Ptr into command_lines[command_line].  */

    pid_t pid;			/* Child process's ID number.  */
#ifdef VMS
    int efn;			/* Completion event flag number */
    int cstatus;		/* Completion status */
#endif
    char *sh_batch_file;        /* Script file for shell commands */
    unsigned int remote:1;	/* Nonzero if executing remotely.  */

    unsigned int noerror:1;	/* Nonzero if commands contained a `-'.  */

    unsigned int good_stdin:1;	/* Nonzero if this child has a good stdin.  */
    unsigned int deleted:1;	/* Nonzero if targets have been deleted.  */
    unsigned int dontcare:1;    /* Saved dontcare flag.  */
  };

extern struct child *children;

extern void new_job PARAMS ((struct file *file));
extern void reap_children PARAMS ((int block, int err));
extern void start_waiting_jobs PARAMS ((void));

extern char **construct_command_argv PARAMS ((char *line, char **restp, struct file *file, char** batch_file));
#ifdef VMS
extern int child_execute_job PARAMS ((char *argv, struct child *child));
#elif defined(__EMX__)
extern int child_execute_job PARAMS ((int stdin_fd, int stdout_fd, char **argv, char **envp));
#else
extern void child_execute_job PARAMS ((int stdin_fd, int stdout_fd, char **argv, char **envp));
#endif
#ifdef _AMIGA
extern void exec_command PARAMS ((char **argv));
#elif defined(__EMX__)
extern int exec_command PARAMS ((char **argv, char **envp));
#else
extern void exec_command PARAMS ((char **argv, char **envp));
#endif

extern unsigned int job_slots_used;

extern void block_sigs PARAMS ((void));
#ifdef POSIX
extern void unblock_sigs PARAMS ((void));
#else
#ifdef	HAVE_SIGSETMASK
extern int fatal_signal_mask;
#define	unblock_sigs()	sigsetmask (0)
#else
#define	unblock_sigs()
#endif
#endif

extern unsigned int jobserver_tokens;

#endif /* SEEN_JOB_H */
