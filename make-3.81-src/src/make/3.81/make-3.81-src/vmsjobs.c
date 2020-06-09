/* --------------- Moved here from job.c ---------------
   This file must be #included in job.c, as it accesses static functions.

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

#include <string.h>
#include <descrip.h>
#include <clidef.h>

extern char *vmsify PARAMS ((char *name, int type));

static int vms_jobsefnmask = 0;

/* Wait for nchildren children to terminate */
static void
vmsWaitForChildren(int *status)
{
  while (1)
    {
      if (!vms_jobsefnmask)
	{
	  *status = 0;
	  return;
	}

      *status = sys$wflor (32, vms_jobsefnmask);
    }
  return;
}

/* Set up IO redirection.  */

char *
vms_redirect (struct dsc$descriptor_s *desc, char *fname, char *ibuf)
{
  char *fptr;

  ibuf++;
  while (isspace ((unsigned char)*ibuf))
    ibuf++;
  fptr = ibuf;
  while (*ibuf && !isspace ((unsigned char)*ibuf))
    ibuf++;
  *ibuf = 0;
  if (strcmp (fptr, "/dev/null") != 0)
    {
      strcpy (fname, vmsify (fptr, 0));
      if (strchr (fname, '.') == 0)
	strcat (fname, ".");
    }
  desc->dsc$w_length = strlen(fname);
  desc->dsc$a_pointer = fname;
  desc->dsc$b_dtype = DSC$K_DTYPE_T;
  desc->dsc$b_class = DSC$K_CLASS_S;

  if (*fname == 0)
    printf (_("Warning: Empty redirection\n"));
  return ibuf;
}


/* found apostrophe at (p-1)
   inc p until after closing apostrophe.
 */

char *
vms_handle_apos (char *p)
{
  int alast;

#define SEPCHARS ",/()= "

  alast = 0;

  while (*p != 0)
    {
      if (*p == '"')
	{
          if (alast)
            {
              alast = 0;
              p++;
	    }
	  else
	    {
	      p++;
	      if (strchr (SEPCHARS, *p))
		break;
	      alast = 1;
	    }
	}
      else
	p++;
    }

  return p;
}

/* This is called as an AST when a child process dies (it won't get
   interrupted by anything except a higher level AST).
*/
int
vmsHandleChildTerm(struct child *child)
{
    int status;
    register struct child *lastc, *c;
    int child_failed;

    vms_jobsefnmask &= ~(1 << (child->efn - 32));

    lib$free_ef(&child->efn);

    (void) sigblock (fatal_signal_mask);

    child_failed = !(child->cstatus & 1 || ((child->cstatus & 7) == 0));

    /* Search for a child matching the deceased one.  */
    lastc = 0;
#if defined(RECURSIVEJOBS) /* I've had problems with recursive stuff and process handling */
    for (c = children; c != 0 && c != child; lastc = c, c = c->next)
      ;
#else
    c = child;
#endif

    if (child_failed && !c->noerror && !ignore_errors_flag)
      {
	/* The commands failed.  Write an error message,
	   delete non-precious targets, and abort.  */
	child_error (c->file->name, c->cstatus, 0, 0, 0);
	c->file->update_status = 1;
	delete_child_targets (c);
      }
    else
      {
	if (child_failed)
	  {
	    /* The commands failed, but we don't care.  */
	    child_error (c->file->name, c->cstatus, 0, 0, 1);
	    child_failed = 0;
	  }

#if defined(RECURSIVEJOBS) /* I've had problems with recursive stuff and process handling */
	/* If there are more commands to run, try to start them.  */
	start_job (c);

	switch (c->file->command_state)
	  {
	  case cs_running:
	    /* Successfully started.  */
	    break;

	  case cs_finished:
	    if (c->file->update_status != 0) {
		/* We failed to start the commands.  */
		delete_child_targets (c);
	    }
	    break;

	  default:
	    error (NILF, _("internal error: `%s' command_state"),
                   c->file->name);
	    abort ();
	    break;
	  }
#endif /* RECURSIVEJOBS */
      }

    /* Set the state flag to say the commands have finished.  */
    c->file->command_state = cs_finished;
    notice_finished_file (c->file);

#if defined(RECURSIVEJOBS) /* I've had problems with recursive stuff and process handling */
    /* Remove the child from the chain and free it.  */
    if (lastc == 0)
      children = c->next;
    else
      lastc->next = c->next;
    free_child (c);
#endif /* RECURSIVEJOBS */

    /* There is now another slot open.  */
    if (job_slots_used > 0)
      --job_slots_used;

    /* If the job failed, and the -k flag was not given, die.  */
    if (child_failed && !keep_going_flag)
      die (EXIT_FAILURE);

    (void) sigsetmask (sigblock (0) & ~(fatal_signal_mask));

    return 1;
}

/* VMS:
   Spawn a process executing the command in ARGV and return its pid. */

#define MAXCMDLEN 200

/* local helpers to make ctrl+c and ctrl+y working, see below */
#include <iodef.h>
#include <libclidef.h>
#include <ssdef.h>

static int ctrlMask= LIB$M_CLI_CTRLY;
static int oldCtrlMask;
static int setupYAstTried= 0;
static int pidToAbort= 0;
static int chan= 0;

static void
reEnableAst(void)
{
	lib$enable_ctrl (&oldCtrlMask,0);
}

static void
astHandler (void)
{
	if (pidToAbort) {
		sys$forcex (&pidToAbort, 0, SS$_ABORT);
		pidToAbort= 0;
	}
	kill (getpid(),SIGQUIT);
}

static void
tryToSetupYAst(void)
{
	$DESCRIPTOR(inputDsc,"SYS$COMMAND");
	int	status;
	struct {
		short int	status, count;
		int	dvi;
	} iosb;

	setupYAstTried++;

	if (!chan) {
		status= sys$assign(&inputDsc,&chan,0,0);
		if (!(status&SS$_NORMAL)) {
			lib$signal(status);
			return;
		}
	}
	status= sys$qiow (0, chan, IO$_SETMODE|IO$M_CTRLYAST,&iosb,0,0,
		astHandler,0,0,0,0,0);
	if (status==SS$_NORMAL)
		status= iosb.status;
        if (status==SS$_ILLIOFUNC || status==SS$_NOPRIV) {
		sys$dassgn(chan);
#ifdef	CTRLY_ENABLED_ANYWAY
		fprintf (stderr,
                         _("-warning, CTRL-Y will leave sub-process(es) around.\n"));
#else
		return;
#endif
	}
	else if (!(status&SS$_NORMAL)) {
		sys$dassgn(chan);
		lib$signal(status);
		return;
	}

	/* called from AST handler ? */
	if (setupYAstTried>1)
		return;
	if (atexit(reEnableAst))
		fprintf (stderr,
                         _("-warning, you may have to re-enable CTRL-Y handling from DCL.\n"));
	status= lib$disable_ctrl (&ctrlMask, &oldCtrlMask);
	if (!(status&SS$_NORMAL)) {
		lib$signal(status);
		return;
	}
}

int
child_execute_job (char *argv, struct child *child)
{
  int i;
  static struct dsc$descriptor_s cmddsc;
  static struct dsc$descriptor_s pnamedsc;
  static struct dsc$descriptor_s ifiledsc;
  static struct dsc$descriptor_s ofiledsc;
  static struct dsc$descriptor_s efiledsc;
  int have_redirection = 0;
  int have_newline = 0;

  int spflags = CLI$M_NOWAIT;
  int status;
  char *cmd = alloca (strlen (argv) + 512), *p, *q;
  char ifile[256], ofile[256], efile[256];
  char *comname = 0;
  char procname[100];
  int in_string;

  /* Parse IO redirection.  */

  ifile[0] = 0;
  ofile[0] = 0;
  efile[0] = 0;

  DB (DB_JOBS, ("child_execute_job (%s)\n", argv));

  while (isspace ((unsigned char)*argv))
    argv++;

  if (*argv == 0)
    return 0;

  sprintf (procname, "GMAKE_%05x", getpid () & 0xfffff);
  pnamedsc.dsc$w_length = strlen(procname);
  pnamedsc.dsc$a_pointer = procname;
  pnamedsc.dsc$b_dtype = DSC$K_DTYPE_T;
  pnamedsc.dsc$b_class = DSC$K_CLASS_S;

  in_string = 0;
  /* Handle comments and redirection. */
  for (p = argv, q = cmd; *p; p++, q++)
    {
      if (*p == '"')
        in_string = !in_string;
      if (in_string)
        {
          *q = *p;
          continue;
        }
      switch (*p)
	{
	  case '#':
	    *p-- = 0;
	    *q-- = 0;
	    break;
	  case '\\':
	    p++;
	    if (*p == '\n')
	      p++;
	    if (isspace ((unsigned char)*p))
	      {
		do { p++; } while (isspace ((unsigned char)*p));
		p--;
	      }
	    *q = *p;
	    break;
	  case '<':
	    p = vms_redirect (&ifiledsc, ifile, p);
	    *q = ' ';
	    have_redirection = 1;
	    break;
	  case '>':
	    have_redirection = 1;
	    if (*(p-1) == '2')
	      {
		q--;
		if (strncmp (p, ">&1", 3) == 0)
		  {
		    p += 3;
		    strcpy (efile, "sys$output");
		    efiledsc.dsc$w_length = strlen(efile);
		    efiledsc.dsc$a_pointer = efile;
		    efiledsc.dsc$b_dtype = DSC$K_DTYPE_T;
		    efiledsc.dsc$b_class = DSC$K_CLASS_S;
		  }
		else
		  {
		    p = vms_redirect (&efiledsc, efile, p);
		  }
	      }
	    else
	      {
		p = vms_redirect (&ofiledsc, ofile, p);
	      }
	    *q = ' ';
	    break;
	  case '\n':
	    have_newline = 1;
	  default:
	    *q = *p;
	    break;
	}
    }
  *q = *p;
  while (isspace ((unsigned char)*--q))
    *q = '\0';

  if (strncmp (cmd, "builtin_", 8) == 0)
    {
      child->pid = 270163;
      child->efn = 0;
      child->cstatus = 1;

      DB (DB_JOBS, (_("BUILTIN [%s][%s]\n"), cmd, cmd+8));

      p = cmd + 8;

      if ((*(p) == 'c')
	  && (*(p+1) == 'd')
	  && ((*(p+2) == ' ') || (*(p+2) == '\t')))
	{
	  p += 3;
	  while ((*p == ' ') || (*p == '\t'))
	    p++;
	  DB (DB_JOBS, (_("BUILTIN CD %s\n"), p));
	  if (chdir (p))
	    return 0;
	  else
	    return 1;
	}
      else if ((*(p) == 'r')
	  && (*(p+1) == 'm')
	  && ((*(p+2) == ' ') || (*(p+2) == '\t')))
	{
	  int in_arg;

	  /* rm  */
	  p += 3;
	  while ((*p == ' ') || (*p == '\t'))
	    p++;
	  in_arg = 1;

	  DB (DB_JOBS, (_("BUILTIN RM %s\n"), p));
	  while (*p)
	    {
	      switch (*p)
		{
		  case ' ':
		  case '\t':
		    if (in_arg)
		      {
			*p++ = ';';
			in_arg = 0;
		      }
		    break;
		  default:
		    break;
		}
	      p++;
	    }
	}
      else
	{
	  printf(_("Unknown builtin command '%s'\n"), cmd);
	  fflush(stdout);
	  return 0;
	}
    }

  /* Create a *.com file if either the command is too long for
     lib$spawn, or the command contains a newline, or if redirection
     is desired. Forcing commands with newlines into DCLs allows to
     store search lists on user mode logicals.  */

  if (strlen (cmd) > MAXCMDLEN
      || (have_redirection != 0)
      || (have_newline != 0))
    {
      FILE *outfile;
      char c;
      char *sep;
      int alevel = 0;	/* apostrophe level */

      if (strlen (cmd) == 0)
	{
	  printf (_("Error, empty command\n"));
	  fflush (stdout);
	  return 0;
	}

      outfile = open_tmpfile (&comname, "sys$scratch:CMDXXXXXX.COM");
      if (outfile == 0)
	pfatal_with_name (_("fopen (temporary file)"));

      if (ifile[0])
	{
	  fprintf (outfile, "$ assign/user %s sys$input\n", ifile);
          DB (DB_JOBS, (_("Redirected input from %s\n"), ifile));
	  ifiledsc.dsc$w_length = 0;
	}

      if (efile[0])
	{
	  fprintf (outfile, "$ define sys$error %s\n", efile);
          DB (DB_JOBS, (_("Redirected error to %s\n"), efile));
	  efiledsc.dsc$w_length = 0;
	}

      if (ofile[0])
	{
	  fprintf (outfile, "$ define sys$output %s\n", ofile);
	  DB (DB_JOBS, (_("Redirected output to %s\n"), ofile));
	  ofiledsc.dsc$w_length = 0;
	}

      p = sep = q = cmd;
      for (c = '\n'; c; c = *q++)
	{
	  switch (c)
	    {
            case '\n':
              /* At a newline, skip any whitespace around a leading $
                 from the command and issue exactly one $ into the DCL. */
              while (isspace ((unsigned char)*p))
                p++;
              if (*p == '$')
                p++;
              while (isspace ((unsigned char)*p))
                p++;
              fwrite (p, 1, q - p, outfile);
              fputc ('$', outfile);
              fputc (' ', outfile);
              /* Reset variables. */
              p = sep = q;
              break;

	      /* Nice places for line breaks are after strings, after
		 comma or space and before slash. */
            case '"':
              q = vms_handle_apos (q);
              sep = q;
              break;
            case ',':
            case ' ':
              sep = q;
              break;
            case '/':
            case '\0':
              sep = q - 1;
              break;
            default:
              break;
	    }
	  if (sep - p > 78)
	    {
	      /* Enough stuff for a line. */
	      fwrite (p, 1, sep - p, outfile);
	      p = sep;
	      if (*sep)
		{
		  /* The command continues.  */
		  fputc ('-', outfile);
		}
	      fputc ('\n', outfile);
	    }
  	}

      fwrite (p, 1, q - p, outfile);
      fputc ('\n', outfile);

      fclose (outfile);

      sprintf (cmd, "$ @%s", comname);

      DB (DB_JOBS, (_("Executing %s instead\n"), cmd));
    }

  cmddsc.dsc$w_length = strlen(cmd);
  cmddsc.dsc$a_pointer = cmd;
  cmddsc.dsc$b_dtype = DSC$K_DTYPE_T;
  cmddsc.dsc$b_class = DSC$K_CLASS_S;

  child->efn = 0;
  while (child->efn < 32 || child->efn > 63)
    {
      status = lib$get_ef ((unsigned long *)&child->efn);
      if (!(status & 1))
	return 0;
    }

  sys$clref (child->efn);

  vms_jobsefnmask |= (1 << (child->efn - 32));

/*
             LIB$SPAWN  [command-string]
			[,input-file]
			[,output-file]
			[,flags]
			[,process-name]
			[,process-id] [,completion-status-address] [,byte-integer-event-flag-num]
			[,AST-address] [,varying-AST-argument]
			[,prompt-string] [,cli] [,table]
*/

#ifndef DONTWAITFORCHILD
/*
 *	Code to make ctrl+c and ctrl+y working.
 *	The problem starts with the synchronous case where after lib$spawn is
 *	called any input will go to the child. But with input re-directed,
 *	both control characters won't make it to any of the programs, neither
 *	the spawning nor to the spawned one. Hence the caller needs to spawn
 *	with CLI$M_NOWAIT to NOT give up the input focus. A sys$waitfr
 *	has to follow to simulate the wanted synchronous behaviour.
 *	The next problem is ctrl+y which isn't caught by the crtl and
 *	therefore isn't converted to SIGQUIT (for a signal handler which is
 *	already established). The only way to catch ctrl+y, is an AST
 *	assigned to the input channel. But ctrl+y handling of DCL needs to be
 *	disabled, otherwise it will handle it. Not to mention the previous
 *	ctrl+y handling of DCL needs to be re-established before make exits.
 *	One more: At the time of LIB$SPAWN signals are blocked. SIGQUIT will
 *	make it to the signal handler after the child "normally" terminates.
 *	This isn't enough. It seems reasonable for simple command lines like
 *	a 'cc foobar.c' spawned in a subprocess but it is unacceptable for
 *	spawning make. Therefore we need to abort the process in the AST.
 *
 *	Prior to the spawn it is checked if an AST is already set up for
 *	ctrl+y, if not one is set up for a channel to SYS$COMMAND. In general
 *	this will work except if make is run in a batch environment, but there
 *	nobody can press ctrl+y. During the setup the DCL handling of ctrl+y
 *	is disabled and an exit handler is established to re-enable it.
 *	If the user interrupts with ctrl+y, the assigned AST will fire, force
 *	an abort to the subprocess and signal SIGQUIT, which will be caught by
 *	the already established handler and will bring us back to common code.
 *	After the spawn (now /nowait) a sys$waitfr simulates the /wait and
 *	enables the ctrl+y be delivered to this code. And the ctrl+c too,
 *	which the crtl converts to SIGINT and which is caught by the common
 *	signal handler. Because signals were blocked before entering this code
 *	sys$waitfr will always complete and the SIGQUIT will be processed after
 *	it (after termination of the current block, somewhere in common code).
 *	And SIGINT too will be delayed. That is ctrl+c can only abort when the
 *	current command completes. Anyway it's better than nothing :-)
 */

  if (!setupYAstTried)
    tryToSetupYAst();
  status = lib$spawn (&cmddsc,					/* cmd-string  */
		      (ifiledsc.dsc$w_length == 0)?0:&ifiledsc, /* input-file  */
		      (ofiledsc.dsc$w_length == 0)?0:&ofiledsc, /* output-file */
		      &spflags,					/* flags  */
		      &pnamedsc,				/* proc name  */
		      &child->pid, &child->cstatus, &child->efn,
		      0, 0,
		      0, 0, 0);
  if (status & 1)
    {
      pidToAbort= child->pid;
      status= sys$waitfr (child->efn);
      pidToAbort= 0;
      vmsHandleChildTerm(child);
    }
#else
  status = lib$spawn (&cmddsc,
		      (ifiledsc.dsc$w_length == 0)?0:&ifiledsc,
		      (ofiledsc.dsc$w_length == 0)?0:&ofiledsc,
		      &spflags,
		      &pnamedsc,
		      &child->pid, &child->cstatus, &child->efn,
		      vmsHandleChildTerm, child,
		      0, 0, 0);
#endif

  if (!(status & 1))
    {
      printf (_("Error spawning, %d\n") ,status);
      fflush (stdout);
      switch (status)
        {
        case 0x1c:
          errno = EPROCLIM;
          break;
        default:
          errno = EFAIL;
        }
    }

  if (comname && !ISDB (DB_JOBS))
    unlink (comname);

  return (status & 1);
}
