/* Command processing for GNU Make.
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
#include "dep.h"
#include "filedef.h"
#include "variable.h"
#include "job.h"
#include "commands.h"
#ifdef WINDOWS32
#include <windows.h>
#include "w32err.h"
#endif

#if VMS
# define FILE_LIST_SEPARATOR ','
#else
# define FILE_LIST_SEPARATOR ' '
#endif

extern int remote_kill PARAMS ((int id, int sig));

#ifndef	HAVE_UNISTD_H
extern int getpid ();
#endif

/* Set FILE's automatic variables up.  */

void
set_file_variables (struct file *file)
{
  struct dep *d;
  char *at, *percent, *star, *less;

#ifndef	NO_ARCHIVES
  /* If the target is an archive member `lib(member)',
     then $@ is `lib' and $% is `member'.  */

  if (ar_name (file->name))
    {
      unsigned int len;
      char *p;

      p = strchr (file->name, '(');
      at = (char *) alloca (p - file->name + 1);
      bcopy (file->name, at, p - file->name);
      at[p - file->name] = '\0';
      len = strlen (p + 1);
      percent = (char *) alloca (len);
      bcopy (p + 1, percent, len - 1);
      percent[len - 1] = '\0';
    }
  else
#endif	/* NO_ARCHIVES.  */
    {
      at = file->name;
      percent = "";
    }

  /* $* is the stem from an implicit or static pattern rule.  */
  if (file->stem == 0)
    {
      /* In Unix make, $* is set to the target name with
	 any suffix in the .SUFFIXES list stripped off for
	 explicit rules.  We store this in the `stem' member.  */
      register struct dep *d;
      char *name;
      unsigned int len;

#ifndef	NO_ARCHIVES
      if (ar_name (file->name))
	{
	  name = strchr (file->name, '(') + 1;
	  len = strlen (name) - 1;
	}
      else
#endif
	{
	  name = file->name;
	  len = strlen (name);
	}

      for (d = enter_file (".SUFFIXES")->deps; d != 0; d = d->next)
	{
	  unsigned int slen = strlen (dep_name (d));
	  if (len > slen && strneq (dep_name (d), name + (len - slen), slen))
	    {
	      file->stem = savestring (name, len - slen);
	      break;
	    }
	}
      if (d == 0)
	file->stem = "";
    }
  star = file->stem;

  /* $< is the first not order-only dependency.  */
  less = "";
  for (d = file->deps; d != 0; d = d->next)
    if (!d->ignore_mtime)
      {
        less = dep_name (d);
        break;
      }

  if (file->cmds == default_file->cmds)
    /* This file got its commands from .DEFAULT.
       In this case $< is the same as $@.  */
    less = at;

#define	DEFINE_VARIABLE(name, len, value) \
  (void) define_variable_for_file (name,len,value,o_automatic,0,file)

  /* Define the variables.  */

  DEFINE_VARIABLE ("<", 1, less);
  DEFINE_VARIABLE ("*", 1, star);
  DEFINE_VARIABLE ("@", 1, at);
  DEFINE_VARIABLE ("%", 1, percent);

  /* Compute the values for $^, $+, $?, and $|.  */

  {
    static char *plus_value=0, *bar_value=0, *qmark_value=0;
    static unsigned int qmark_max=0, plus_max=0, bar_max=0;

    unsigned int qmark_len, plus_len, bar_len;
    char *cp;
    char *caret_value;
    char *qp;
    char *bp;
    unsigned int len;

    /* Compute first the value for $+, which is supposed to contain
       duplicate dependencies as they were listed in the makefile.  */

    plus_len = 0;
    for (d = file->deps; d != 0; d = d->next)
      if (! d->ignore_mtime)
	plus_len += strlen (dep_name (d)) + 1;
    if (plus_len == 0)
      plus_len++;

    if (plus_len > plus_max)
      plus_value = xrealloc (plus_value, plus_max = plus_len);
    cp = plus_value;

    qmark_len = plus_len + 1;	/* Will be this or less.  */
    for (d = file->deps; d != 0; d = d->next)
      if (! d->ignore_mtime)
        {
          char *c = dep_name (d);

#ifndef	NO_ARCHIVES
          if (ar_name (c))
            {
              c = strchr (c, '(') + 1;
              len = strlen (c) - 1;
            }
          else
#endif
            len = strlen (c);

          bcopy (c, cp, len);
          cp += len;
          *cp++ = FILE_LIST_SEPARATOR;
          if (! d->changed)
            qmark_len -= len + 1;	/* Don't space in $? for this one.  */
        }

    /* Kill the last space and define the variable.  */

    cp[cp > plus_value ? -1 : 0] = '\0';
    DEFINE_VARIABLE ("+", 1, plus_value);

    /* Make sure that no dependencies are repeated.  This does not
       really matter for the purpose of updating targets, but it
       might make some names be listed twice for $^ and $?.  */

    uniquize_deps (file->deps);

    bar_len = 0;
    for (d = file->deps; d != 0; d = d->next)
      if (d->ignore_mtime)
	bar_len += strlen (dep_name (d)) + 1;
    if (bar_len == 0)
      bar_len++;

    /* Compute the values for $^, $?, and $|.  */

    cp = caret_value = plus_value; /* Reuse the buffer; it's big enough.  */

    if (qmark_len > qmark_max)
      qmark_value = xrealloc (qmark_value, qmark_max = qmark_len);
    qp = qmark_value;

    if (bar_len > bar_max)
      bar_value = xrealloc (bar_value, bar_max = bar_len);
    bp = bar_value;

    for (d = file->deps; d != 0; d = d->next)
      {
	char *c = dep_name (d);

#ifndef	NO_ARCHIVES
	if (ar_name (c))
	  {
	    c = strchr (c, '(') + 1;
	    len = strlen (c) - 1;
	  }
	else
#endif
	  len = strlen (c);

        if (d->ignore_mtime)
          {
	    bcopy (c, bp, len);
	    bp += len;
	    *bp++ = FILE_LIST_SEPARATOR;
	  }
	else
	  {
            bcopy (c, cp, len);
            cp += len;
            *cp++ = FILE_LIST_SEPARATOR;
            if (d->changed)
              {
                bcopy (c, qp, len);
                qp += len;
                *qp++ = FILE_LIST_SEPARATOR;
              }
          }
      }

    /* Kill the last spaces and define the variables.  */

    cp[cp > caret_value ? -1 : 0] = '\0';
    DEFINE_VARIABLE ("^", 1, caret_value);

    qp[qp > qmark_value ? -1 : 0] = '\0';
    DEFINE_VARIABLE ("?", 1, qmark_value);

    bp[bp > bar_value ? -1 : 0] = '\0';
    DEFINE_VARIABLE ("|", 1, bar_value);
  }

#undef	DEFINE_VARIABLE
}

/* Chop CMDS up into individual command lines if necessary.
   Also set the `lines_flags' and `any_recurse' members.  */

void
chop_commands (struct commands *cmds)
{
  register char *p;
  unsigned int nlines, idx;
  char **lines;

  /* If we don't have any commands,
     or we already parsed them, never mind.  */

  if (!cmds || cmds->command_lines != 0)
    return;

  /* Chop CMDS->commands up into lines in CMDS->command_lines.
	 Also set the corresponding CMDS->lines_flags elements,
	 and the CMDS->any_recurse flag.  */

  nlines = 5;
  lines = (char **) xmalloc (5 * sizeof (char *));
  idx = 0;
  p = cmds->commands;
  while (*p != '\0')
    {
      char *end = p;
    find_end:;
      end = strchr (end, '\n');
      if (end == 0)
        end = p + strlen (p);
      else if (end > p && end[-1] == '\\')
        {
          int backslash = 1;
          register char *b;
          for (b = end - 2; b >= p && *b == '\\'; --b)
            backslash = !backslash;
          if (backslash)
            {
              ++end;
              goto find_end;
            }
        }

      if (idx == nlines)
        {
          nlines += 2;
          lines = (char **) xrealloc ((char *) lines,
                                      nlines * sizeof (char *));
        }
      lines[idx++] = savestring (p, end - p);
      p = end;
      if (*p != '\0')
        ++p;
    }

  if (idx != nlines)
    {
      nlines = idx;
      lines = (char **) xrealloc ((char *) lines,
                                  nlines * sizeof (char *));
    }

  cmds->ncommand_lines = nlines;
  cmds->command_lines = lines;

  cmds->any_recurse = 0;
  cmds->lines_flags = (char *) xmalloc (nlines);
  for (idx = 0; idx < nlines; ++idx)
    {
      int flags = 0;

      for (p = lines[idx];
           isblank ((unsigned char)*p) || *p == '-' || *p == '@' || *p == '+';
           ++p)
        switch (*p)
          {
          case '+':
            flags |= COMMANDS_RECURSE;
            break;
          case '@':
            flags |= COMMANDS_SILENT;
            break;
          case '-':
            flags |= COMMANDS_NOERROR;
            break;
          }

      /* If no explicit '+' was given, look for MAKE variable references.  */
      if (!(flags & COMMANDS_RECURSE)
          && (strstr (p, "$(MAKE)") != 0 || strstr (p, "${MAKE}") != 0))
        flags |= COMMANDS_RECURSE;

      cmds->lines_flags[idx] = flags;
      cmds->any_recurse |= flags & COMMANDS_RECURSE;
    }
}

/* Execute the commands to remake FILE.  If they are currently executing,
   return or have already finished executing, just return.  Otherwise,
   fork off a child process to run the first command line in the sequence.  */

void
execute_file_commands (struct file *file)
{
  register char *p;

  /* Don't go through all the preparations if
     the commands are nothing but whitespace.  */

  for (p = file->cmds->commands; *p != '\0'; ++p)
    if (!isspace ((unsigned char)*p) && *p != '-' && *p != '@')
      break;
  if (*p == '\0')
    {
      /* If there are no commands, assume everything worked.  */
      set_command_state (file, cs_running);
      file->update_status = 0;
      notice_finished_file (file);
      return;
    }

  /* First set the automatic variables according to this file.  */

  initialize_file_variables (file, 0);

  set_file_variables (file);

  /* Start the commands running.  */
  new_job (file);
}

/* This is set while we are inside fatal_error_signal,
   so things can avoid nonreentrant operations.  */

int handling_fatal_signal = 0;

/* Handle fatal signals.  */

RETSIGTYPE
fatal_error_signal (int sig)
{
#ifdef __MSDOS__
  extern int dos_status, dos_command_running;

  if (dos_command_running)
    {
      /* That was the child who got the signal, not us.  */
      dos_status |= (sig << 8);
      return;
    }
  remove_intermediates (1);
  exit (EXIT_FAILURE);
#else /* not __MSDOS__ */
#ifdef _AMIGA
  remove_intermediates (1);
  if (sig == SIGINT)
     fputs (_("*** Break.\n"), stderr);

  exit (10);
#else /* not Amiga */
#ifdef WINDOWS32
  extern HANDLE main_thread;

  /* Windows creates a sperate thread for handling Ctrl+C, so we need
     to suspend the main thread, or else we will have race conditions
     when both threads call reap_children.  */
  if (main_thread)
    {
      DWORD susp_count = SuspendThread (main_thread);

      if (susp_count != 0)
	fprintf (stderr, "SuspendThread: suspend count = %ld\n", susp_count);
      else if (susp_count == (DWORD)-1)
	{
	  DWORD ierr = GetLastError ();

	  fprintf (stderr, "SuspendThread: error %ld: %s\n",
		   ierr, map_windows32_error_to_string (ierr));
	}
    }
#endif
  handling_fatal_signal = 1;

  /* Set the handling for this signal to the default.
     It is blocked now while we run this handler.  */
  signal (sig, SIG_DFL);

  /* A termination signal won't be sent to the entire
     process group, but it means we want to kill the children.  */

  if (sig == SIGTERM)
    {
      register struct child *c;
      for (c = children; c != 0; c = c->next)
	if (!c->remote)
	  (void) kill (c->pid, SIGTERM);
    }

  /* If we got a signal that means the user
     wanted to kill make, remove pending targets.  */

  if (sig == SIGTERM || sig == SIGINT
#ifdef SIGHUP
    || sig == SIGHUP
#endif
#ifdef SIGQUIT
    || sig == SIGQUIT
#endif
    )
    {
      register struct child *c;

      /* Remote children won't automatically get signals sent
	 to the process group, so we must send them.  */
      for (c = children; c != 0; c = c->next)
	if (c->remote)
	  (void) remote_kill (c->pid, sig);

      for (c = children; c != 0; c = c->next)
	delete_child_targets (c);

      /* Clean up the children.  We don't just use the call below because
	 we don't want to print the "Waiting for children" message.  */
      while (job_slots_used > 0)
	reap_children (1, 0);
    }
  else
    /* Wait for our children to die.  */
    while (job_slots_used > 0)
      reap_children (1, 1);

  /* Delete any non-precious intermediate files that were made.  */

  remove_intermediates (1);

#ifdef SIGQUIT
  if (sig == SIGQUIT)
    /* We don't want to send ourselves SIGQUIT, because it will
       cause a core dump.  Just exit instead.  */
    exit (EXIT_FAILURE);
#endif

#ifdef WINDOWS32
  if (main_thread)
    CloseHandle (main_thread);
  /* Cannot call W32_kill with a pid (it needs a handle).  The exit
     status of 130 emulates what happens in Bash.  */
  exit (130);
#else
  /* Signal the same code; this time it will really be fatal.  The signal
     will be unblocked when we return and arrive then to kill us.  */
  if (kill (getpid (), sig) < 0)
    pfatal_with_name ("kill");
#endif /* not WINDOWS32 */
#endif /* not Amiga */
#endif /* not __MSDOS__  */
}

/* Delete FILE unless it's precious or not actually a file (phony),
   and it has changed on disk since we last stat'd it.  */

static void
delete_target (struct file *file, char *on_behalf_of)
{
  struct stat st;
  int e;

  if (file->precious || file->phony)
    return;

#ifndef NO_ARCHIVES
  if (ar_name (file->name))
    {
      time_t file_date = (file->last_mtime == NONEXISTENT_MTIME
			  ? (time_t) -1
			  : (time_t) FILE_TIMESTAMP_S (file->last_mtime));
      if (ar_member_date (file->name) != file_date)
	{
	  if (on_behalf_of)
	    error (NILF, _("*** [%s] Archive member `%s' may be bogus; not deleted"),
		   on_behalf_of, file->name);
	  else
	    error (NILF, _("*** Archive member `%s' may be bogus; not deleted"),
		   file->name);
	}
      return;
    }
#endif

  EINTRLOOP (e, stat (file->name, &st));
  if (e == 0
      && S_ISREG (st.st_mode)
      && FILE_TIMESTAMP_STAT_MODTIME (file->name, st) != file->last_mtime)
    {
      if (on_behalf_of)
	error (NILF, _("*** [%s] Deleting file `%s'"), on_behalf_of, file->name);
      else
	error (NILF, _("*** Deleting file `%s'"), file->name);
      if (unlink (file->name) < 0
	  && errno != ENOENT)	/* It disappeared; so what.  */
	perror_with_name ("unlink: ", file->name);
    }
}


/* Delete all non-precious targets of CHILD unless they were already deleted.
   Set the flag in CHILD to say they've been deleted.  */

void
delete_child_targets (struct child *child)
{
  struct dep *d;

  if (child->deleted)
    return;

  /* Delete the target file if it changed.  */
  delete_target (child->file, (char *) 0);

  /* Also remove any non-precious targets listed in the `also_make' member.  */
  for (d = child->file->also_make; d != 0; d = d->next)
    delete_target (d->file, child->file->name);

  child->deleted = 1;
}

/* Print out the commands in CMDS.  */

void
print_commands (struct commands *cmds)
{
  register char *s;

  fputs (_("#  commands to execute"), stdout);

  if (cmds->fileinfo.filenm == 0)
    puts (_(" (built-in):"));
  else
    printf (_(" (from `%s', line %lu):\n"),
            cmds->fileinfo.filenm, cmds->fileinfo.lineno);

  s = cmds->commands;
  while (*s != '\0')
    {
      char *end;

      while (isspace ((unsigned char)*s))
	++s;

      end = strchr (s, '\n');
      if (end == 0)
	end = s + strlen (s);

      printf ("\t%.*s\n", (int) (end - s), s);

      s = end;
    }
}
