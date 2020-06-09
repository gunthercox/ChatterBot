/* Reading and parsing of makefiles for GNU Make.
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

#include <assert.h>

#include <glob.h>

#include "dep.h"
#include "filedef.h"
#include "job.h"
#include "commands.h"
#include "variable.h"
#include "rule.h"
#include "debug.h"
#include "hash.h"


#ifndef WINDOWS32
#ifndef _AMIGA
#ifndef VMS
#include <pwd.h>
#else
struct passwd *getpwnam PARAMS ((char *name));
#endif
#endif
#endif /* !WINDOWS32 */

/* A 'struct ebuffer' controls the origin of the makefile we are currently
   eval'ing.
*/

struct ebuffer
  {
    char *buffer;       /* Start of the current line in the buffer.  */
    char *bufnext;      /* Start of the next line in the buffer.  */
    char *bufstart;     /* Start of the entire buffer.  */
    unsigned int size;  /* Malloc'd size of buffer. */
    FILE *fp;           /* File, or NULL if this is an internal buffer.  */
    struct floc floc;   /* Info on the file in fp (if any).  */
  };

/* Types of "words" that can be read in a makefile.  */
enum make_word_type
  {
     w_bogus, w_eol, w_static, w_variable, w_colon, w_dcolon, w_semicolon,
     w_varassign
  };


/* A `struct conditionals' contains the information describing
   all the active conditionals in a makefile.

   The global variable `conditionals' contains the conditionals
   information for the current makefile.  It is initialized from
   the static structure `toplevel_conditionals' and is later changed
   to new structures for included makefiles.  */

struct conditionals
  {
    unsigned int if_cmds;	/* Depth of conditional nesting.  */
    unsigned int allocated;	/* Elts allocated in following arrays.  */
    char *ignoring;		/* Are we ignoring or interpreting?
                                   0=interpreting, 1=not yet interpreted,
                                   2=already interpreted */
    char *seen_else;		/* Have we already seen an `else'?  */
  };

static struct conditionals toplevel_conditionals;
static struct conditionals *conditionals = &toplevel_conditionals;


/* Default directories to search for include files in  */

static char *default_include_directories[] =
  {
#if defined(WINDOWS32) && !defined(INCLUDEDIR)
/*
 * This completely up to the user when they install MSVC or other packages.
 * This is defined as a placeholder.
 */
#define INCLUDEDIR "."
#endif
    INCLUDEDIR,
#ifndef _AMIGA
    "/usr/gnu/include",
    "/usr/local/include",
    "/usr/include",
#endif
    0
  };

/* List of directories to search for include files in  */

static char **include_directories;

/* Maximum length of an element of the above.  */

static unsigned int max_incl_len;

/* The filename and pointer to line number of the
   makefile currently being read in.  */

const struct floc *reading_file = 0;

/* The chain of makefiles read by read_makefile.  */

static struct dep *read_makefiles = 0;

static int eval_makefile PARAMS ((char *filename, int flags));
static int eval PARAMS ((struct ebuffer *buffer, int flags));

static long readline PARAMS ((struct ebuffer *ebuf));
static void do_define PARAMS ((char *name, unsigned int namelen,
                               enum variable_origin origin,
                               struct ebuffer *ebuf));
static int conditional_line PARAMS ((char *line, int len, const struct floc *flocp));
static void record_files PARAMS ((struct nameseq *filenames, char *pattern, char *pattern_percent,
			struct dep *deps, unsigned int cmds_started, char *commands,
			unsigned int commands_idx, int two_colon,
                        const struct floc *flocp));
static void record_target_var PARAMS ((struct nameseq *filenames, char *defn,
                                       enum variable_origin origin,
                                       int enabled,
                                       const struct floc *flocp));
static enum make_word_type get_next_mword PARAMS ((char *buffer, char *delim,
                        char **startp, unsigned int *length));
static void remove_comments PARAMS ((char *line));
static char *find_char_unquote PARAMS ((char *string, int stop1,
                                        int stop2, int blank, int ignorevars));

/* Read in all the makefiles and return the chain of their names.  */

struct dep *
read_all_makefiles (char **makefiles)
{
  unsigned int num_makefiles = 0;

  /* Create *_LIST variables, to hold the makefiles, targets, and variables
     we will be reading. */

  define_variable ("MAKEFILE_LIST", sizeof ("MAKEFILE_LIST")-1, "", o_file, 0);

  DB (DB_BASIC, (_("Reading makefiles...\n")));

  /* If there's a non-null variable MAKEFILES, its value is a list of
     files to read first thing.  But don't let it prevent reading the
     default makefiles and don't let the default goal come from there.  */

  {
    char *value;
    char *name, *p;
    unsigned int length;

    {
      /* Turn off --warn-undefined-variables while we expand MAKEFILES.  */
      int save = warn_undefined_variables_flag;
      warn_undefined_variables_flag = 0;

      value = allocated_variable_expand ("$(MAKEFILES)");

      warn_undefined_variables_flag = save;
    }

    /* Set NAME to the start of next token and LENGTH to its length.
       MAKEFILES is updated for finding remaining tokens.  */
    p = value;

    while ((name = find_next_token (&p, &length)) != 0)
      {
	if (*p != '\0')
	  *p++ = '\0';
	eval_makefile (name, RM_NO_DEFAULT_GOAL|RM_INCLUDED|RM_DONTCARE);
      }

    free (value);
  }

  /* Read makefiles specified with -f switches.  */

  if (makefiles != 0)
    while (*makefiles != 0)
      {
	struct dep *tail = read_makefiles;
	register struct dep *d;

	if (! eval_makefile (*makefiles, 0))
	  perror_with_name ("", *makefiles);

	/* Find the right element of read_makefiles.  */
	d = read_makefiles;
	while (d->next != tail)
	  d = d->next;

	/* Use the storage read_makefile allocates.  */
	*makefiles = dep_name (d);
	++num_makefiles;
	++makefiles;
      }

  /* If there were no -f switches, try the default names.  */

  if (num_makefiles == 0)
    {
      static char *default_makefiles[] =
#ifdef VMS
	/* all lower case since readdir() (the vms version) 'lowercasifies' */
	{ "makefile.vms", "gnumakefile.", "makefile.", 0 };
#else
#ifdef _AMIGA
	{ "GNUmakefile", "Makefile", "SMakefile", 0 };
#else /* !Amiga && !VMS */
	{ "GNUmakefile", "makefile", "Makefile", 0 };
#endif /* AMIGA */
#endif /* VMS */
      register char **p = default_makefiles;
      while (*p != 0 && !file_exists_p (*p))
	++p;

      if (*p != 0)
	{
	  if (! eval_makefile (*p, 0))
	    perror_with_name ("", *p);
	}
      else
	{
	  /* No default makefile was found.  Add the default makefiles to the
	     `read_makefiles' chain so they will be updated if possible.  */
	  struct dep *tail = read_makefiles;
	  /* Add them to the tail, after any MAKEFILES variable makefiles.  */
	  while (tail != 0 && tail->next != 0)
	    tail = tail->next;
	  for (p = default_makefiles; *p != 0; ++p)
	    {
	      struct dep *d = alloc_dep ();
	      d->file = enter_file (*p);
	      d->file->dontcare = 1;
	      /* Tell update_goal_chain to bail out as soon as this file is
		 made, and main not to die if we can't make this file.  */
	      d->changed = RM_DONTCARE;
	      if (tail == 0)
		read_makefiles = d;
	      else
		tail->next = d;
	      tail = d;
	    }
	  if (tail != 0)
	    tail->next = 0;
	}
    }

  return read_makefiles;
}

/* Install a new conditional and return the previous one.  */

static struct conditionals *
install_conditionals (struct conditionals *new)
{
  struct conditionals *save = conditionals;

  bzero ((char *) new, sizeof (*new));
  conditionals = new;

  return save;
}

/* Free the current conditionals and reinstate a saved one.  */

static void
restore_conditionals (struct conditionals *saved)
{
  /* Free any space allocated by conditional_line.  */
  if (conditionals->ignoring)
    free (conditionals->ignoring);
  if (conditionals->seen_else)
    free (conditionals->seen_else);

  /* Restore state.  */
  conditionals = saved;
}

static int
eval_makefile (char *filename, int flags)
{
  struct dep *deps;
  struct ebuffer ebuf;
  const struct floc *curfile;
  char *expanded = 0;
  char *included = 0;
  int makefile_errno;
  int r;

  ebuf.floc.filenm = strcache_add (filename);
  ebuf.floc.lineno = 1;

  if (ISDB (DB_VERBOSE))
    {
      printf (_("Reading makefile `%s'"), filename);
      if (flags & RM_NO_DEFAULT_GOAL)
	printf (_(" (no default goal)"));
      if (flags & RM_INCLUDED)
	printf (_(" (search path)"));
      if (flags & RM_DONTCARE)
	printf (_(" (don't care)"));
      if (flags & RM_NO_TILDE)
	printf (_(" (no ~ expansion)"));
      puts ("...");
    }

  /* First, get a stream to read.  */

  /* Expand ~ in FILENAME unless it came from `include',
     in which case it was already done.  */
  if (!(flags & RM_NO_TILDE) && filename[0] == '~')
    {
      expanded = tilde_expand (filename);
      if (expanded != 0)
	filename = expanded;
    }

  ebuf.fp = fopen (filename, "r");
  /* Save the error code so we print the right message later.  */
  makefile_errno = errno;

  /* If the makefile wasn't found and it's either a makefile from
     the `MAKEFILES' variable or an included makefile,
     search the included makefile search path for this makefile.  */
  if (ebuf.fp == 0 && (flags & RM_INCLUDED) && *filename != '/')
    {
      register unsigned int i;
      for (i = 0; include_directories[i] != 0; ++i)
	{
	  included = concat (include_directories[i], "/", filename);
	  ebuf.fp = fopen (included, "r");
	  if (ebuf.fp)
	    {
	      filename = included;
	      break;
	    }
          free (included);
	}
      /* If we're not using it, we already freed it above.  */
      if (filename != included)
        included = 0;
    }

  /* Add FILENAME to the chain of read makefiles.  */
  deps = alloc_dep ();
  deps->next = read_makefiles;
  read_makefiles = deps;
  deps->file = lookup_file (filename);
  if (deps->file == 0)
    deps->file = enter_file (xstrdup (filename));
  filename = deps->file->name;
  deps->changed = flags;
  if (flags & RM_DONTCARE)
    deps->file->dontcare = 1;

  if (expanded)
    free (expanded);
  if (included)
    free (included);

  /* If the makefile can't be found at all, give up entirely.  */

  if (ebuf.fp == 0)
    {
      /* If we did some searching, errno has the error from the last
	 attempt, rather from FILENAME itself.  Restore it in case the
	 caller wants to use it in a message.  */
      errno = makefile_errno;
      return 0;
    }

  /* Add this makefile to the list. */
  do_variable_definition (&ebuf.floc, "MAKEFILE_LIST", filename, o_file,
                          f_append, 0);

  /* Evaluate the makefile */

  ebuf.size = 200;
  ebuf.buffer = ebuf.bufnext = ebuf.bufstart = xmalloc (ebuf.size);

  curfile = reading_file;
  reading_file = &ebuf.floc;

  r = eval (&ebuf, !(flags & RM_NO_DEFAULT_GOAL));

  reading_file = curfile;

  fclose (ebuf.fp);

  free (ebuf.bufstart);
  alloca (0);
  return r;
}

int
eval_buffer (char *buffer)
{
  struct ebuffer ebuf;
  struct conditionals *saved;
  struct conditionals new;
  const struct floc *curfile;
  int r;

  /* Evaluate the buffer */

  ebuf.size = strlen (buffer);
  ebuf.buffer = ebuf.bufnext = ebuf.bufstart = buffer;
  ebuf.fp = NULL;

  ebuf.floc = *reading_file;

  curfile = reading_file;
  reading_file = &ebuf.floc;

  saved = install_conditionals (&new);

  r = eval (&ebuf, 1);

  restore_conditionals (saved);

  reading_file = curfile;

  alloca (0);
  return r;
}


/* Read file FILENAME as a makefile and add its contents to the data base.

   SET_DEFAULT is true if we are allowed to set the default goal.  */


static int
eval (struct ebuffer *ebuf, int set_default)
{
  char *collapsed = 0;
  unsigned int collapsed_length = 0;
  unsigned int commands_len = 200;
  char *commands;
  unsigned int commands_idx = 0;
  unsigned int cmds_started, tgts_started;
  int ignoring = 0, in_ignored_define = 0;
  int no_targets = 0;		/* Set when reading a rule without targets.  */
  struct nameseq *filenames = 0;
  struct dep *deps = 0;
  long nlines = 0;
  int two_colon = 0;
  char *pattern = 0, *pattern_percent;
  struct floc *fstart;
  struct floc fi;

#define record_waiting_files()						      \
  do									      \
    { 									      \
      if (filenames != 0)						      \
        {                                                                     \
	  fi.lineno = tgts_started;                                           \
	  record_files (filenames, pattern, pattern_percent, deps,            \
                        cmds_started, commands, commands_idx, two_colon,      \
                        &fi);                                                 \
        }                                                                     \
      filenames = 0;							      \
      commands_idx = 0;							      \
      no_targets = 0;                                                         \
      if (pattern) { free(pattern); pattern = 0; }                            \
    } while (0)

  pattern_percent = 0;
  cmds_started = tgts_started = 1;

  fstart = &ebuf->floc;
  fi.filenm = ebuf->floc.filenm;

  /* Loop over lines in the file.
     The strategy is to accumulate target names in FILENAMES, dependencies
     in DEPS and commands in COMMANDS.  These are used to define a rule
     when the start of the next rule (or eof) is encountered.

     When you see a "continue" in the loop below, that means we are moving on
     to the next line _without_ ending any rule that we happen to be working
     with at the moment.  If you see a "goto rule_complete", then the
     statement we just parsed also finishes the previous rule.  */

  commands = xmalloc (200);

  while (1)
    {
      unsigned int linelen;
      char *line;
      int len;
      char *p;
      char *p2;

      /* Grab the next line to be evaluated */
      ebuf->floc.lineno += nlines;
      nlines = readline (ebuf);

      /* If there is nothing left to eval, we're done.  */
      if (nlines < 0)
        break;

      /* If this line is empty, skip it.  */
      line = ebuf->buffer;
      if (line[0] == '\0')
        continue;

      linelen = strlen (line);

      /* Check for a shell command line first.
	 If it is not one, we can stop treating tab specially.  */
      if (line[0] == '\t')
	{
	  if (no_targets)
	    /* Ignore the commands in a rule with no targets.  */
	    continue;

	  /* If there is no preceding rule line, don't treat this line
	     as a command, even though it begins with a tab character.
	     SunOS 4 make appears to behave this way.  */

	  if (filenames != 0)
	    {
	      if (ignoring)
		/* Yep, this is a shell command, and we don't care.  */
		continue;

	      /* Append this command line to the line being accumulated.  */
	      if (commands_idx == 0)
		cmds_started = ebuf->floc.lineno;

	      if (linelen + 1 + commands_idx > commands_len)
		{
		  commands_len = (linelen + 1 + commands_idx) * 2;
		  commands = xrealloc (commands, commands_len);
		}
	      bcopy (line, &commands[commands_idx], linelen);
	      commands_idx += linelen;
	      commands[commands_idx++] = '\n';

	      continue;
	    }
	}

      /* This line is not a shell command line.  Don't worry about tabs.
         Get more space if we need it; we don't need to preserve the current
         contents of the buffer.  */

      if (collapsed_length < linelen+1)
	{
	  collapsed_length = linelen+1;
          if (collapsed)
            free ((char *)collapsed);
	  collapsed = (char *) xmalloc (collapsed_length);
	}
      strcpy (collapsed, line);
      /* Collapse continuation lines.  */
      collapse_continuations (collapsed);
      remove_comments (collapsed);

      /* Compare a word, both length and contents. */
#define	word1eq(s) 	(len == sizeof(s)-1 && strneq (s, p, sizeof(s)-1))
      p = collapsed;
      while (isspace ((unsigned char)*p))
	++p;

      if (*p == '\0')
	/* This line is completely empty--ignore it.  */
	continue;

      /* Find the end of the first token.  Note we don't need to worry about
       * ":" here since we compare tokens by length (so "export" will never
       * be equal to "export:").
       */
      for (p2 = p+1; *p2 != '\0' && !isspace ((unsigned char)*p2); ++p2)
        ;
      len = p2 - p;

      /* Find the start of the second token.  If it looks like a target or
         variable definition it can't be a preprocessor token so skip
         them--this allows variables/targets named `ifdef', `export', etc. */
      while (isspace ((unsigned char)*p2))
        ++p2;

      if ((p2[0] == ':' || p2[0] == '+' || p2[0] == '=') && p2[1] == '\0')
        {
          /* It can't be a preprocessor token so skip it if we're ignoring */
          if (ignoring)
            continue;

          goto skip_conditionals;
        }

      /* We must first check for conditional and `define' directives before
	 ignoring anything, since they control what we will do with
	 following lines.  */

      if (!in_ignored_define)
	{
 	  int i = conditional_line (p, len, fstart);
          if (i != -2)
            {
              if (i == -1)
                fatal (fstart, _("invalid syntax in conditional"));

              ignoring = i;
              continue;
            }
	}

      if (word1eq ("endef"))
	{
	  if (!in_ignored_define)
	    fatal (fstart, _("extraneous `endef'"));
          in_ignored_define = 0;
	  continue;
	}

      if (word1eq ("define"))
	{
	  if (ignoring)
	    in_ignored_define = 1;
	  else
	    {
              if (*p2 == '\0')
                fatal (fstart, _("empty variable name"));

	      /* Let the variable name be the whole rest of the line,
		 with trailing blanks stripped (comments have already been
		 removed), so it could be a complex variable/function
		 reference that might contain blanks.  */
	      p = strchr (p2, '\0');
	      while (isblank ((unsigned char)p[-1]))
		--p;
	      do_define (p2, p - p2, o_file, ebuf);
	    }
	  continue;
	}

      if (word1eq ("override"))
        {
	  if (*p2 == '\0')
	    error (fstart, _("empty `override' directive"));

	  if (strneq (p2, "define", 6)
	      && (isblank ((unsigned char)p2[6]) || p2[6] == '\0'))
	    {
	      if (ignoring)
		in_ignored_define = 1;
	      else
		{
		  p2 = next_token (p2 + 6);
                  if (*p2 == '\0')
                    fatal (fstart, _("empty variable name"));

		  /* Let the variable name be the whole rest of the line,
		     with trailing blanks stripped (comments have already been
		     removed), so it could be a complex variable/function
		     reference that might contain blanks.  */
		  p = strchr (p2, '\0');
		  while (isblank ((unsigned char)p[-1]))
		    --p;
		  do_define (p2, p - p2, o_override, ebuf);
		}
	    }
	  else if (!ignoring
		   && !try_variable_definition (fstart, p2, o_override, 0))
	    error (fstart, _("invalid `override' directive"));

	  continue;
	}

      if (ignoring)
	/* Ignore the line.  We continue here so conditionals
	   can appear in the middle of a rule.  */
	continue;

      if (word1eq ("export"))
	{
          /* 'export' by itself causes everything to be exported. */
	  if (*p2 == '\0')
            export_all_variables = 1;
          else
            {
              struct variable *v;

              v = try_variable_definition (fstart, p2, o_file, 0);
              if (v != 0)
                v->export = v_export;
              else
                {
                  unsigned int len;
                  char *ap;

                  /* Expand the line so we can use indirect and constructed
                     variable names in an export command.  */
                  p2 = ap = allocated_variable_expand (p2);

                  for (p = find_next_token (&p2, &len); p != 0;
                       p = find_next_token (&p2, &len))
                    {
                      v = lookup_variable (p, len);
                      if (v == 0)
                        v = define_variable_loc (p, len, "", o_file, 0,
                                                 fstart);
                      v->export = v_export;
                    }

                  free (ap);
                }
            }
          goto rule_complete;
	}

      if (word1eq ("unexport"))
	{
	  if (*p2 == '\0')
	    export_all_variables = 0;
          else
            {
              unsigned int len;
              struct variable *v;
              char *ap;

              /* Expand the line so we can use indirect and constructed
                 variable names in an unexport command.  */
              p2 = ap = allocated_variable_expand (p2);

              for (p = find_next_token (&p2, &len); p != 0;
                   p = find_next_token (&p2, &len))
                {
                  v = lookup_variable (p, len);
                  if (v == 0)
                    v = define_variable_loc (p, len, "", o_file, 0, fstart);

                  v->export = v_noexport;
                }

              free (ap);
            }
          goto rule_complete;
	}

 skip_conditionals:
      if (word1eq ("vpath"))
	{
	  char *pattern;
	  unsigned int len;
	  p2 = variable_expand (p2);
	  p = find_next_token (&p2, &len);
	  if (p != 0)
	    {
	      pattern = savestring (p, len);
	      p = find_next_token (&p2, &len);
	      /* No searchpath means remove all previous
		 selective VPATH's with the same pattern.  */
	    }
	  else
	    /* No pattern means remove all previous selective VPATH's.  */
	    pattern = 0;
	  construct_vpath_list (pattern, p);
	  if (pattern != 0)
	    free (pattern);

          goto rule_complete;
	}

      if (word1eq ("include") || word1eq ("-include") || word1eq ("sinclude"))
	{
	  /* We have found an `include' line specifying a nested
	     makefile to be read at this point.  */
	  struct conditionals *save;
          struct conditionals new_conditionals;
	  struct nameseq *files;
	  /* "-include" (vs "include") says no error if the file does not
	     exist.  "sinclude" is an alias for this from SGI.  */
	  int noerror = (p[0] != 'i');

	  p = allocated_variable_expand (p2);

          /* If no filenames, it's a no-op.  */
	  if (*p == '\0')
            {
              free (p);
              continue;
            }

	  /* Parse the list of file names.  */
	  p2 = p;
	  files = multi_glob (parse_file_seq (&p2, '\0',
					      sizeof (struct nameseq),
					      1),
			      sizeof (struct nameseq));
	  free (p);

	  /* Save the state of conditionals and start
	     the included makefile with a clean slate.  */
	  save = install_conditionals (&new_conditionals);

	  /* Record the rules that are waiting so they will determine
	     the default goal before those in the included makefile.  */
	  record_waiting_files ();

	  /* Read each included makefile.  */
	  while (files != 0)
	    {
	      struct nameseq *next = files->next;
	      char *name = files->name;
              int r;

	      free ((char *)files);
	      files = next;

              r = eval_makefile (name, (RM_INCLUDED | RM_NO_TILDE
                                        | (noerror ? RM_DONTCARE : 0)));
	      if (!r && !noerror)
                error (fstart, "%s: %s", name, strerror (errno));
              free (name);
	    }

	  /* Restore conditional state.  */
	  restore_conditionals (save);

          goto rule_complete;
	}

      if (try_variable_definition (fstart, p, o_file, 0))
	/* This line has been dealt with.  */
	goto rule_complete;

      /* This line starts with a tab but was not caught above because there
         was no preceding target, and the line might have been usable as a
         variable definition.  But now we know it is definitely lossage.  */
      if (line[0] == '\t')
        fatal(fstart, _("commands commence before first target"));

      /* This line describes some target files.  This is complicated by
         the existence of target-specific variables, because we can't
         expand the entire line until we know if we have one or not.  So
         we expand the line word by word until we find the first `:',
         then check to see if it's a target-specific variable.

         In this algorithm, `lb_next' will point to the beginning of the
         unexpanded parts of the input buffer, while `p2' points to the
         parts of the expanded buffer we haven't searched yet. */

      {
        enum make_word_type wtype;
        enum variable_origin v_origin;
        int exported;
        char *cmdleft, *semip, *lb_next;
        unsigned int len, plen = 0;
        char *colonp;
        const char *end, *beg; /* Helpers for whitespace stripping. */

        /* Record the previous rule.  */

        record_waiting_files ();
        tgts_started = fstart->lineno;

        /* Search the line for an unquoted ; that is not after an
           unquoted #.  */
        cmdleft = find_char_unquote (line, ';', '#', 0, 1);
        if (cmdleft != 0 && *cmdleft == '#')
          {
            /* We found a comment before a semicolon.  */
            *cmdleft = '\0';
            cmdleft = 0;
          }
        else if (cmdleft != 0)
          /* Found one.  Cut the line short there before expanding it.  */
          *(cmdleft++) = '\0';
        semip = cmdleft;

        collapse_continuations (line);

        /* We can't expand the entire line, since if it's a per-target
           variable we don't want to expand it.  So, walk from the
           beginning, expanding as we go, and looking for "interesting"
           chars.  The first word is always expandable.  */
        wtype = get_next_mword(line, NULL, &lb_next, &len);
        switch (wtype)
          {
          case w_eol:
            if (cmdleft != 0)
              fatal(fstart, _("missing rule before commands"));
            /* This line contained something but turned out to be nothing
               but whitespace (a comment?).  */
            continue;

          case w_colon:
          case w_dcolon:
            /* We accept and ignore rules without targets for
               compatibility with SunOS 4 make.  */
            no_targets = 1;
            continue;

          default:
            break;
          }

        p2 = variable_expand_string(NULL, lb_next, len);

        while (1)
          {
            lb_next += len;
            if (cmdleft == 0)
              {
                /* Look for a semicolon in the expanded line.  */
                cmdleft = find_char_unquote (p2, ';', 0, 0, 0);

                if (cmdleft != 0)
                  {
                    unsigned long p2_off = p2 - variable_buffer;
                    unsigned long cmd_off = cmdleft - variable_buffer;
                    char *pend = p2 + strlen(p2);

                    /* Append any remnants of lb, then cut the line short
                       at the semicolon.  */
                    *cmdleft = '\0';

                    /* One school of thought says that you shouldn't expand
                       here, but merely copy, since now you're beyond a ";"
                       and into a command script.  However, the old parser
                       expanded the whole line, so we continue that for
                       backwards-compatiblity.  Also, it wouldn't be
                       entirely consistent, since we do an unconditional
                       expand below once we know we don't have a
                       target-specific variable. */
                    (void)variable_expand_string(pend, lb_next, (long)-1);
                    lb_next += strlen(lb_next);
                    p2 = variable_buffer + p2_off;
                    cmdleft = variable_buffer + cmd_off + 1;
                  }
              }

            colonp = find_char_unquote(p2, ':', 0, 0, 0);
#if defined HAVE_DOS_PATHS || defined __CYGWIN32__
            /* The drive spec brain-damage strikes again...  */
            /* Note that the only separators of targets in this context
               are whitespace and a left paren.  If others are possible,
               they should be added to the string in the call to index.  */
            while (colonp && (colonp[1] == '/' || colonp[1] == '\\') &&
                   colonp > p2 && isalpha ((unsigned char)colonp[-1]) &&
                   (colonp == p2 + 1 || strchr (" \t(", colonp[-2]) != 0))
              colonp = find_char_unquote(colonp + 1, ':', 0, 0, 0);
#endif
            if (colonp != 0)
              break;

            wtype = get_next_mword(lb_next, NULL, &lb_next, &len);
            if (wtype == w_eol)
              break;

            p2 += strlen(p2);
            *(p2++) = ' ';
            p2 = variable_expand_string(p2, lb_next, len);
            /* We don't need to worry about cmdleft here, because if it was
               found in the variable_buffer the entire buffer has already
               been expanded... we'll never get here.  */
          }

        p2 = next_token (variable_buffer);

        /* If the word we're looking at is EOL, see if there's _anything_
           on the line.  If not, a variable expanded to nothing, so ignore
           it.  If so, we can't parse this line so punt.  */
        if (wtype == w_eol)
          {
            if (*p2 != '\0')
              /* There's no need to be ivory-tower about this: check for
                 one of the most common bugs found in makefiles...  */
              fatal (fstart, _("missing separator%s"),
                     !strneq(line, "        ", 8) ? ""
                     : _(" (did you mean TAB instead of 8 spaces?)"));
            continue;
          }

        /* Make the colon the end-of-string so we know where to stop
           looking for targets.  */
        *colonp = '\0';
        filenames = multi_glob (parse_file_seq (&p2, '\0',
                                                sizeof (struct nameseq),
                                                1),
                                sizeof (struct nameseq));
        *p2 = ':';

        if (!filenames)
          {
            /* We accept and ignore rules without targets for
               compatibility with SunOS 4 make.  */
            no_targets = 1;
            continue;
          }
        /* This should never be possible; we handled it above.  */
        assert (*p2 != '\0');
        ++p2;

        /* Is this a one-colon or two-colon entry?  */
        two_colon = *p2 == ':';
        if (two_colon)
          p2++;

        /* Test to see if it's a target-specific variable.  Copy the rest
           of the buffer over, possibly temporarily (we'll expand it later
           if it's not a target-specific variable).  PLEN saves the length
           of the unparsed section of p2, for later.  */
        if (*lb_next != '\0')
          {
            unsigned int l = p2 - variable_buffer;
            plen = strlen (p2);
            (void) variable_buffer_output (p2+plen,
                                           lb_next, strlen (lb_next)+1);
            p2 = variable_buffer + l;
          }

        /* See if it's an "override" or "export" keyword; if so see if what
           comes after it looks like a variable definition.  */

        wtype = get_next_mword (p2, NULL, &p, &len);

        v_origin = o_file;
        exported = 0;
        if (wtype == w_static)
          {
            if (word1eq ("override"))
              {
                v_origin = o_override;
                wtype = get_next_mword (p+len, NULL, &p, &len);
              }
            else if (word1eq ("export"))
              {
                exported = 1;
                wtype = get_next_mword (p+len, NULL, &p, &len);
              }
          }

        if (wtype != w_eol)
          wtype = get_next_mword (p+len, NULL, NULL, NULL);

        if (wtype == w_varassign)
          {
            /* If there was a semicolon found, add it back, plus anything
               after it.  */
            if (semip)
              {
                unsigned int l = p - variable_buffer;
                *(--semip) = ';';
                variable_buffer_output (p2 + strlen (p2),
                                        semip, strlen (semip)+1);
                p = variable_buffer + l;
              }
            record_target_var (filenames, p, v_origin, exported, fstart);
            filenames = 0;
            continue;
          }

        /* This is a normal target, _not_ a target-specific variable.
           Unquote any = in the dependency list.  */
        find_char_unquote (lb_next, '=', 0, 0, 0);

        /* We have some targets, so don't ignore the following commands.  */
        no_targets = 0;

        /* Expand the dependencies, etc.  */
        if (*lb_next != '\0')
          {
            unsigned int l = p2 - variable_buffer;
            (void) variable_expand_string (p2 + plen, lb_next, (long)-1);
            p2 = variable_buffer + l;

            /* Look for a semicolon in the expanded line.  */
            if (cmdleft == 0)
              {
                cmdleft = find_char_unquote (p2, ';', 0, 0, 0);
                if (cmdleft != 0)
                  *(cmdleft++) = '\0';
              }
          }

        /* Is this a static pattern rule: `target: %targ: %dep; ...'?  */
        p = strchr (p2, ':');
        while (p != 0 && p[-1] == '\\')
          {
            register char *q = &p[-1];
            register int backslash = 0;
            while (*q-- == '\\')
              backslash = !backslash;
            if (backslash)
              p = strchr (p + 1, ':');
            else
              break;
          }
#ifdef _AMIGA
        /* Here, the situation is quite complicated. Let's have a look
           at a couple of targets:

           install: dev:make

           dev:make: make

           dev:make:: xyz

           The rule is that it's only a target, if there are TWO :'s
           OR a space around the :.
        */
        if (p && !(isspace ((unsigned char)p[1]) || !p[1]
                   || isspace ((unsigned char)p[-1])))
          p = 0;
#endif
#if defined HAVE_DOS_PATHS || defined __CYGWIN32__
        {
          int check_again;

          do {
            check_again = 0;
            /* For DOS-style paths, skip a "C:\..." or a "C:/..." */
            if (p != 0 && (p[1] == '\\' || p[1] == '/') &&
                isalpha ((unsigned char)p[-1]) &&
                (p == p2 + 1 || strchr (" \t:(", p[-2]) != 0)) {
              p = strchr (p + 1, ':');
              check_again = 1;
            }
          } while (check_again);
        }
#endif
        if (p != 0)
          {
            struct nameseq *target;
            target = parse_file_seq (&p2, ':', sizeof (struct nameseq), 1);
            ++p2;
            if (target == 0)
              fatal (fstart, _("missing target pattern"));
            else if (target->next != 0)
              fatal (fstart, _("multiple target patterns"));
            pattern = target->name;
            pattern_percent = find_percent (pattern);
            if (pattern_percent == 0)
              fatal (fstart, _("target pattern contains no `%%'"));
            free ((char *)target);
          }
        else
          pattern = 0;

        /* Strip leading and trailing whitespaces. */
        beg = p2;
        end = beg + strlen (beg) - 1;
        strip_whitespace (&beg, &end);

        if (beg <= end && *beg != '\0')
          {
            /* Put all the prerequisites here; they'll be parsed later.  */
            deps = alloc_dep ();
            deps->name = savestring (beg, end - beg + 1);
          }
        else
          deps = 0;

        commands_idx = 0;
        if (cmdleft != 0)
          {
            /* Semicolon means rest of line is a command.  */
            unsigned int len = strlen (cmdleft);

            cmds_started = fstart->lineno;

            /* Add this command line to the buffer.  */
            if (len + 2 > commands_len)
              {
                commands_len = (len + 2) * 2;
                commands = (char *) xrealloc (commands, commands_len);
              }
            bcopy (cmdleft, commands, len);
            commands_idx += len;
            commands[commands_idx++] = '\n';
          }

        /* Determine if this target should be made default. We used to do
           this in record_files() but because of the delayed target recording
           and because preprocessor directives are legal in target's commands
           it is too late. Consider this fragment for example:

           foo:

           ifeq ($(.DEFAULT_GOAL),foo)
              ...
           endif

           Because the target is not recorded until after ifeq directive is
           evaluated the .DEFAULT_GOAL does not contain foo yet as one
           would expect. Because of this we have to move some of the logic
           here.  */

        if (**default_goal_name == '\0' && set_default)
          {
            char* name;
            struct dep *d;
            struct nameseq *t = filenames;

            for (; t != 0; t = t->next)
              {
                int reject = 0;
                name = t->name;

                /* We have nothing to do if this is an implicit rule. */
                if (strchr (name, '%') != 0)
                  break;

                /* See if this target's name does not start with a `.',
                   unless it contains a slash.  */
                if (*name == '.' && strchr (name, '/') == 0
#if defined HAVE_DOS_PATHS || defined __CYGWIN32__
                    && strchr (name, '\\') == 0
#endif
                    )
                  continue;


                /* If this file is a suffix, don't let it be
                   the default goal file.  */
                for (d = suffix_file->deps; d != 0; d = d->next)
                  {
                    register struct dep *d2;
                    if (*dep_name (d) != '.' && streq (name, dep_name (d)))
                      {
                        reject = 1;
                        break;
                      }
                    for (d2 = suffix_file->deps; d2 != 0; d2 = d2->next)
                      {
                        register unsigned int len = strlen (dep_name (d2));
                        if (!strneq (name, dep_name (d2), len))
                          continue;
                        if (streq (name + len, dep_name (d)))
                          {
                            reject = 1;
                            break;
                          }
                      }

                    if (reject)
                      break;
                  }

                if (!reject)
                  {
                    define_variable_global (".DEFAULT_GOAL", 13, t->name,
                                            o_file, 0, NILF);
                    break;
                  }
              }
          }

        continue;
      }

      /* We get here except in the case that we just read a rule line.
	 Record now the last rule we read, so following spurious
	 commands are properly diagnosed.  */
 rule_complete:
      record_waiting_files ();
    }

#undef	word1eq

  if (conditionals->if_cmds)
    fatal (fstart, _("missing `endif'"));

  /* At eof, record the last rule.  */
  record_waiting_files ();

  if (collapsed)
    free ((char *) collapsed);
  free ((char *) commands);

  return 1;
}


/* Remove comments from LINE.
   This is done by copying the text at LINE onto itself.  */

static void
remove_comments (char *line)
{
  char *comment;

  comment = find_char_unquote (line, '#', 0, 0, 0);

  if (comment != 0)
    /* Cut off the line at the #.  */
    *comment = '\0';
}

/* Execute a `define' directive.
   The first line has already been read, and NAME is the name of
   the variable to be defined.  The following lines remain to be read.  */

static void
do_define (char *name, unsigned int namelen,
           enum variable_origin origin, struct ebuffer *ebuf)
{
  struct floc defstart;
  long nlines = 0;
  int nlevels = 1;
  unsigned int length = 100;
  char *definition = (char *) xmalloc (length);
  unsigned int idx = 0;
  char *p;

  /* Expand the variable name.  */
  char *var = (char *) alloca (namelen + 1);
  bcopy (name, var, namelen);
  var[namelen] = '\0';
  var = variable_expand (var);

  defstart = ebuf->floc;

  while (1)
    {
      unsigned int len;
      char *line;

      nlines = readline (ebuf);
      ebuf->floc.lineno += nlines;

      /* If there is nothing left to eval, we're done. */
      if (nlines < 0)
        break;

      line = ebuf->buffer;

      collapse_continuations (line);

      /* If the line doesn't begin with a tab, test to see if it introduces
         another define, or ends one.  */

      /* Stop if we find an 'endef' */
      if (line[0] != '\t')
        {
          p = next_token (line);
          len = strlen (p);

          /* If this is another 'define', increment the level count.  */
          if ((len == 6 || (len > 6 && isblank ((unsigned char)p[6])))
              && strneq (p, "define", 6))
            ++nlevels;

          /* If this is an 'endef', decrement the count.  If it's now 0,
             we've found the last one.  */
          else if ((len == 5 || (len > 5 && isblank ((unsigned char)p[5])))
                   && strneq (p, "endef", 5))
            {
              p += 5;
              remove_comments (p);
              if (*next_token (p) != '\0')
                error (&ebuf->floc,
                       _("Extraneous text after `endef' directive"));

              if (--nlevels == 0)
                {
                  /* Define the variable.  */
                  if (idx == 0)
                    definition[0] = '\0';
                  else
                    definition[idx - 1] = '\0';

                  /* Always define these variables in the global set.  */
                  define_variable_global (var, strlen (var), definition,
                                          origin, 1, &defstart);
                  free (definition);
                  return;
                }
            }
        }

      /* Otherwise add this line to the variable definition.  */
      len = strlen (line);
      if (idx + len + 1 > length)
        {
          length = (idx + len) * 2;
          definition = (char *) xrealloc (definition, length + 1);
        }

      bcopy (line, &definition[idx], len);
      idx += len;
      /* Separate lines with a newline.  */
      definition[idx++] = '\n';
    }

  /* No `endef'!!  */
  fatal (&defstart, _("missing `endef', unterminated `define'"));

  /* NOTREACHED */
  return;
}

/* Interpret conditional commands "ifdef", "ifndef", "ifeq",
   "ifneq", "else" and "endif".
   LINE is the input line, with the command as its first word.

   FILENAME and LINENO are the filename and line number in the
   current makefile.  They are used for error messages.

   Value is -2 if the line is not a conditional at all,
   -1 if the line is an invalid conditional,
   0 if following text should be interpreted,
   1 if following text should be ignored.  */

static int
conditional_line (char *line, int len, const struct floc *flocp)
{
  char *cmdname;
  enum { c_ifdef, c_ifndef, c_ifeq, c_ifneq, c_else, c_endif } cmdtype;
  unsigned int i;
  unsigned int o;

  /* Compare a word, both length and contents. */
#define	word1eq(s)      (len == sizeof(s)-1 && strneq (s, line, sizeof(s)-1))
#define	chkword(s, t)   if (word1eq (s)) { cmdtype = (t); cmdname = (s); }

  /* Make sure this line is a conditional.  */
  chkword ("ifdef", c_ifdef)
  else chkword ("ifndef", c_ifndef)
  else chkword ("ifeq", c_ifeq)
  else chkword ("ifneq", c_ifneq)
  else chkword ("else", c_else)
  else chkword ("endif", c_endif)
  else
    return -2;

  /* Found one: skip past it and any whitespace after it.  */
  line = next_token (line + len);

#define EXTRANEOUS() error (flocp, _("Extraneous text after `%s' directive"), cmdname)

  /* An 'endif' cannot contain extra text, and reduces the if-depth by 1  */
  if (cmdtype == c_endif)
    {
      if (*line != '\0')
	EXTRANEOUS ();

      if (!conditionals->if_cmds)
	fatal (flocp, _("extraneous `%s'"), cmdname);

      --conditionals->if_cmds;

      goto DONE;
    }

  /* An 'else' statement can either be simple, or it can have another
     conditional after it.  */
  if (cmdtype == c_else)
    {
      const char *p;

      if (!conditionals->if_cmds)
	fatal (flocp, _("extraneous `%s'"), cmdname);

      o = conditionals->if_cmds - 1;

      if (conditionals->seen_else[o])
        fatal (flocp, _("only one `else' per conditional"));

      /* Change the state of ignorance.  */
      switch (conditionals->ignoring[o])
        {
          case 0:
            /* We've just been interpreting.  Never do it again.  */
            conditionals->ignoring[o] = 2;
            break;
          case 1:
            /* We've never interpreted yet.  Maybe this time!  */
            conditionals->ignoring[o] = 0;
            break;
        }

      /* It's a simple 'else'.  */
      if (*line == '\0')
        {
          conditionals->seen_else[o] = 1;
          goto DONE;
        }

      /* The 'else' has extra text.  That text must be another conditional
         and cannot be an 'else' or 'endif'.  */

      /* Find the length of the next word.  */
      for (p = line+1; *p != '\0' && !isspace ((unsigned char)*p); ++p)
        ;
      len = p - line;

      /* If it's 'else' or 'endif' or an illegal conditional, fail.  */
      if (word1eq("else") || word1eq("endif")
          || conditional_line (line, len, flocp) < 0)
	EXTRANEOUS ();
      else
        {
          /* conditional_line() created a new level of conditional.
             Raise it back to this level.  */
          if (conditionals->ignoring[o] < 2)
            conditionals->ignoring[o] = conditionals->ignoring[o+1];
          --conditionals->if_cmds;
        }

      goto DONE;
    }

  if (conditionals->allocated == 0)
    {
      conditionals->allocated = 5;
      conditionals->ignoring = (char *) xmalloc (conditionals->allocated);
      conditionals->seen_else = (char *) xmalloc (conditionals->allocated);
    }

  o = conditionals->if_cmds++;
  if (conditionals->if_cmds > conditionals->allocated)
    {
      conditionals->allocated += 5;
      conditionals->ignoring = (char *)
	xrealloc (conditionals->ignoring, conditionals->allocated);
      conditionals->seen_else = (char *)
	xrealloc (conditionals->seen_else, conditionals->allocated);
    }

  /* Record that we have seen an `if...' but no `else' so far.  */
  conditionals->seen_else[o] = 0;

  /* Search through the stack to see if we're already ignoring.  */
  for (i = 0; i < o; ++i)
    if (conditionals->ignoring[i])
      {
	/* We are already ignoring, so just push a level to match the next
	   "else" or "endif", and keep ignoring.  We don't want to expand
	   variables in the condition.  */
	conditionals->ignoring[o] = 1;
	return 1;
      }

  if (cmdtype == c_ifdef || cmdtype == c_ifndef)
    {
      char *var;
      struct variable *v;
      char *p;

      /* Expand the thing we're looking up, so we can use indirect and
         constructed variable names.  */
      var = allocated_variable_expand (line);

      /* Make sure there's only one variable name to test.  */
      p = end_of_token (var);
      i = p - var;
      p = next_token (p);
      if (*p != '\0')
	return -1;

      var[i] = '\0';
      v = lookup_variable (var, i);

      conditionals->ignoring[o] =
        ((v != 0 && *v->value != '\0') == (cmdtype == c_ifndef));

      free (var);
    }
  else
    {
      /* "Ifeq" or "ifneq".  */
      char *s1, *s2;
      unsigned int len;
      char termin = *line == '(' ? ',' : *line;

      if (termin != ',' && termin != '"' && termin != '\'')
	return -1;

      s1 = ++line;
      /* Find the end of the first string.  */
      if (termin == ',')
	{
	  int count = 0;
	  for (; *line != '\0'; ++line)
	    if (*line == '(')
	      ++count;
	    else if (*line == ')')
	      --count;
	    else if (*line == ',' && count <= 0)
	      break;
	}
      else
	while (*line != '\0' && *line != termin)
	  ++line;

      if (*line == '\0')
	return -1;

      if (termin == ',')
	{
	  /* Strip blanks after the first string.  */
	  char *p = line++;
	  while (isblank ((unsigned char)p[-1]))
	    --p;
	  *p = '\0';
	}
      else
	*line++ = '\0';

      s2 = variable_expand (s1);
      /* We must allocate a new copy of the expanded string because
	 variable_expand re-uses the same buffer.  */
      len = strlen (s2);
      s1 = (char *) alloca (len + 1);
      bcopy (s2, s1, len + 1);

      if (termin != ',')
	/* Find the start of the second string.  */
	line = next_token (line);

      termin = termin == ',' ? ')' : *line;
      if (termin != ')' && termin != '"' && termin != '\'')
	return -1;

      /* Find the end of the second string.  */
      if (termin == ')')
	{
	  register int count = 0;
	  s2 = next_token (line);
	  for (line = s2; *line != '\0'; ++line)
	    {
	      if (*line == '(')
		++count;
	      else if (*line == ')')
		{
		  if (count <= 0)
		    break;
		  else
		    --count;
		}
	    }
	}
      else
	{
	  ++line;
	  s2 = line;
	  while (*line != '\0' && *line != termin)
	    ++line;
	}

      if (*line == '\0')
	return -1;

      *line = '\0';
      line = next_token (++line);
      if (*line != '\0')
	EXTRANEOUS ();

      s2 = variable_expand (s2);
      conditionals->ignoring[o] = (streq (s1, s2) == (cmdtype == c_ifneq));
    }

 DONE:
  /* Search through the stack to see if we're ignoring.  */
  for (i = 0; i < conditionals->if_cmds; ++i)
    if (conditionals->ignoring[i])
      return 1;
  return 0;
}

/* Remove duplicate dependencies in CHAIN.  */

static unsigned long
dep_hash_1 (const void *key)
{
  return_STRING_HASH_1 (dep_name ((struct dep const *) key));
}

static unsigned long
dep_hash_2 (const void *key)
{
  return_STRING_HASH_2 (dep_name ((struct dep const *) key));
}

static int
dep_hash_cmp (const void *x, const void *y)
{
  struct dep *dx = (struct dep *) x;
  struct dep *dy = (struct dep *) y;
  int cmp = strcmp (dep_name (dx), dep_name (dy));

  /* If the names are the same but ignore_mtimes are not equal, one of these
     is an order-only prerequisite and one isn't.  That means that we should
     remove the one that isn't and keep the one that is.  */

  if (!cmp && dx->ignore_mtime != dy->ignore_mtime)
    dx->ignore_mtime = dy->ignore_mtime = 0;

  return cmp;
}


void
uniquize_deps (struct dep *chain)
{
  struct hash_table deps;
  register struct dep **depp;

  hash_init (&deps, 500, dep_hash_1, dep_hash_2, dep_hash_cmp);

  /* Make sure that no dependencies are repeated.  This does not
     really matter for the purpose of updating targets, but it
     might make some names be listed twice for $^ and $?.  */

  depp = &chain;
  while (*depp)
    {
      struct dep *dep = *depp;
      struct dep **dep_slot = (struct dep **) hash_find_slot (&deps, dep);
      if (HASH_VACANT (*dep_slot))
	{
	  hash_insert_at (&deps, dep, dep_slot);
	  depp = &dep->next;
	}
      else
	{
	  /* Don't bother freeing duplicates.
	     It's dangerous and little benefit accrues.  */
	  *depp = dep->next;
	}
    }

  hash_free (&deps, 0);
}

/* Record target-specific variable values for files FILENAMES.
   TWO_COLON is nonzero if a double colon was used.

   The links of FILENAMES are freed, and so are any names in it
   that are not incorporated into other data structures.

   If the target is a pattern, add the variable to the pattern-specific
   variable value list.  */

static void
record_target_var (struct nameseq *filenames, char *defn,
                   enum variable_origin origin, int exported,
                   const struct floc *flocp)
{
  struct nameseq *nextf;
  struct variable_set_list *global;

  global = current_variable_set_list;

  /* If the variable is an append version, store that but treat it as a
     normal recursive variable.  */

  for (; filenames != 0; filenames = nextf)
    {
      struct variable *v;
      register char *name = filenames->name;
      char *fname;
      char *percent;
      struct pattern_var *p;

      nextf = filenames->next;
      free ((char *) filenames);

      /* If it's a pattern target, then add it to the pattern-specific
         variable list.  */
      percent = find_percent (name);
      if (percent)
        {
          /* Get a reference for this pattern-specific variable struct.  */
          p = create_pattern_var (name, percent);
          p->variable.fileinfo = *flocp;
          /* I don't think this can fail since we already determined it was a
             variable definition.  */
          v = parse_variable_definition (&p->variable, defn);
          assert (v != 0);

          if (v->flavor == f_simple)
            v->value = allocated_variable_expand (v->value);
          else
            v->value = xstrdup (v->value);

          fname = p->target;
        }
      else
        {
          struct file *f;

          /* Get a file reference for this file, and initialize it.
             We don't want to just call enter_file() because that allocates a
             new entry if the file is a double-colon, which we don't want in
             this situation.  */
          f = lookup_file (name);
          if (!f)
            f = enter_file (name);
          else if (f->double_colon)
            f = f->double_colon;

          initialize_file_variables (f, 1);
          fname = f->name;

          current_variable_set_list = f->variables;
          v = try_variable_definition (flocp, defn, origin, 1);
          if (!v)
            error (flocp, _("Malformed target-specific variable definition"));
          current_variable_set_list = global;
        }

      /* Set up the variable to be *-specific.  */
      v->origin = origin;
      v->per_target = 1;
      v->export = exported ? v_export : v_default;

      /* If it's not an override, check to see if there was a command-line
         setting.  If so, reset the value.  */
      if (origin != o_override)
        {
          struct variable *gv;
          int len = strlen(v->name);

          gv = lookup_variable (v->name, len);
          if (gv && (gv->origin == o_env_override || gv->origin == o_command))
            {
              if (v->value != 0)
                free (v->value);
              v->value = xstrdup (gv->value);
              v->origin = gv->origin;
              v->recursive = gv->recursive;
              v->append = 0;
            }
        }

      /* Free name if not needed further.  */
      if (name != fname && (name < fname || name > fname + strlen (fname)))
        free (name);
    }
}

/* Record a description line for files FILENAMES,
   with dependencies DEPS, commands to execute described
   by COMMANDS and COMMANDS_IDX, coming from FILENAME:COMMANDS_STARTED.
   TWO_COLON is nonzero if a double colon was used.
   If not nil, PATTERN is the `%' pattern to make this
   a static pattern rule, and PATTERN_PERCENT is a pointer
   to the `%' within it.

   The links of FILENAMES are freed, and so are any names in it
   that are not incorporated into other data structures.  */

static void
record_files (struct nameseq *filenames, char *pattern, char *pattern_percent,
              struct dep *deps, unsigned int cmds_started, char *commands,
              unsigned int commands_idx, int two_colon,
              const struct floc *flocp)
{
  struct nameseq *nextf;
  int implicit = 0;
  unsigned int max_targets = 0, target_idx = 0;
  char **targets = 0, **target_percents = 0;
  struct commands *cmds;

  /* If we've already snapped deps, that means we're in an eval being
     resolved after the makefiles have been read in.  We can't add more rules
     at this time, since they won't get snapped and we'll get core dumps.
     See Savannah bug # 12124.  */
  if (snapped_deps)
    fatal (flocp, _("prerequisites cannot be defined in command scripts"));

  if (commands_idx > 0)
    {
      cmds = (struct commands *) xmalloc (sizeof (struct commands));
      cmds->fileinfo.filenm = flocp->filenm;
      cmds->fileinfo.lineno = cmds_started;
      cmds->commands = savestring (commands, commands_idx);
      cmds->command_lines = 0;
    }
  else
    cmds = 0;

  for (; filenames != 0; filenames = nextf)
    {
      char *name = filenames->name;
      struct file *f;
      struct dep *this = 0;
      char *implicit_percent;

      nextf = filenames->next;
      free (filenames);

      /* Check for special targets.  Do it here instead of, say, snap_deps()
         so that we can immediately use the value.  */

      if (streq (name, ".POSIX"))
        posix_pedantic = 1;
      else if (streq (name, ".SECONDEXPANSION"))
        second_expansion = 1;

      implicit_percent = find_percent (name);
      implicit |= implicit_percent != 0;

      if (implicit && pattern != 0)
	fatal (flocp, _("mixed implicit and static pattern rules"));

      if (implicit && implicit_percent == 0)
	fatal (flocp, _("mixed implicit and normal rules"));

      if (implicit)
	{
	  if (targets == 0)
	    {
	      max_targets = 5;
	      targets = (char **) xmalloc (5 * sizeof (char *));
	      target_percents = (char **) xmalloc (5 * sizeof (char *));
	      target_idx = 0;
	    }
	  else if (target_idx == max_targets - 1)
	    {
	      max_targets += 5;
	      targets = (char **) xrealloc ((char *) targets,
					    max_targets * sizeof (char *));
	      target_percents
		= (char **) xrealloc ((char *) target_percents,
				      max_targets * sizeof (char *));
	    }
	  targets[target_idx] = name;
	  target_percents[target_idx] = implicit_percent;
	  ++target_idx;
	  continue;
	}

      /* If this is a static pattern rule:
         `targets: target%pattern: dep%pattern; cmds',
         make sure the pattern matches this target name.  */
      if (pattern && !pattern_matches (pattern, pattern_percent, name))
        error (flocp, _("target `%s' doesn't match the target pattern"), name);
      else if (deps)
        {
          /* If there are multiple filenames, copy the chain DEPS for all but
             the last one.  It is not safe for the same deps to go in more
             than one place in the database.  */
          this = nextf != 0 ? copy_dep_chain (deps) : deps;
          this->need_2nd_expansion = (second_expansion
				      && strchr (this->name, '$'));
        }

      if (!two_colon)
	{
	  /* Single-colon.  Combine these dependencies
	     with others in file's existing record, if any.  */
	  f = enter_file (name);

	  if (f->double_colon)
	    fatal (flocp,
                   _("target file `%s' has both : and :: entries"), f->name);

	  /* If CMDS == F->CMDS, this target was listed in this rule
	     more than once.  Just give a warning since this is harmless.  */
	  if (cmds != 0 && cmds == f->cmds)
	    error (flocp,
                   _("target `%s' given more than once in the same rule."),
                   f->name);

	  /* Check for two single-colon entries both with commands.
	     Check is_target so that we don't lose on files such as .c.o
	     whose commands were preinitialized.  */
	  else if (cmds != 0 && f->cmds != 0 && f->is_target)
	    {
	      error (&cmds->fileinfo,
                     _("warning: overriding commands for target `%s'"),
                     f->name);
	      error (&f->cmds->fileinfo,
                     _("warning: ignoring old commands for target `%s'"),
                     f->name);
	    }

	  f->is_target = 1;

	  /* Defining .DEFAULT with no deps or cmds clears it.  */
	  if (f == default_file && this == 0 && cmds == 0)
	    f->cmds = 0;
	  if (cmds != 0)
	    f->cmds = cmds;

	  /* Defining .SUFFIXES with no dependencies clears out the list of
	     suffixes.  */
	  if (f == suffix_file && this == 0)
	    {
              free_dep_chain (f->deps);
	      f->deps = 0;
	    }
          else if (this != 0)
	    {
	      /* Add the file's old deps and the new ones in THIS together.  */

              if (f->deps != 0)
                {
                  struct dep **d_ptr = &f->deps;

                  while ((*d_ptr)->next != 0)
                    d_ptr = &(*d_ptr)->next;

                  if (cmds != 0)
                    /* This is the rule with commands, so put its deps
                       last. The rationale behind this is that $< expands to
                       the first dep in the chain, and commands use $<
                       expecting to get the dep that rule specifies.  However
                       the second expansion algorithm reverses the order thus
                       we need to make it last here.  */
                    (*d_ptr)->next = this;
                  else
                    {
                      /* This is the rule without commands. Put its
                         dependencies at the end but before dependencies from
                         the rule with commands (if any). This way everything
                         appears in makefile order.  */

                      if (f->cmds != 0)
                        {
                          this->next = *d_ptr;
                          *d_ptr = this;
                        }
                      else
                        (*d_ptr)->next = this;
                    }
                }
              else
                f->deps = this;

              /* This is a hack. I need a way to communicate to snap_deps()
                 that the last dependency line in this file came with commands
                 (so that logic in snap_deps() can put it in front and all
                 this $< -logic works). I cannot simply rely on file->cmds
                 being not 0 because of the cases like the following:

                 foo: bar
                 foo:
                     ...

                 I am going to temporarily "borrow" UPDATING member in
                 `struct file' for this.   */

              if (cmds != 0)
                f->updating = 1;
	    }
	}
      else
	{
	  /* Double-colon.  Make a new record even if there already is one.  */
	  f = lookup_file (name);

	  /* Check for both : and :: rules.  Check is_target so
	     we don't lose on default suffix rules or makefiles.  */
	  if (f != 0 && f->is_target && !f->double_colon)
	    fatal (flocp,
                   _("target file `%s' has both : and :: entries"), f->name);
	  f = enter_file (name);
	  /* If there was an existing entry and it was a double-colon entry,
	     enter_file will have returned a new one, making it the prev
	     pointer of the old one, and setting its double_colon pointer to
	     the first one.  */
	  if (f->double_colon == 0)
	    /* This is the first entry for this name, so we must set its
	       double_colon pointer to itself.  */
	    f->double_colon = f;
	  f->is_target = 1;
	  f->deps = this;
	  f->cmds = cmds;
	}

      /* If this is a static pattern rule, set the stem to the part of its
         name that matched the `%' in the pattern, so you can use $* in the
         commands.  */
      if (pattern)
        {
          static char *percent = "%";
          char *buffer = variable_expand ("");
          char *o = patsubst_expand (buffer, name, pattern, percent,
                                     pattern_percent+1, percent+1);
          f->stem = savestring (buffer, o - buffer);
          if (this)
            {
              this->staticpattern = 1;
              this->stem = xstrdup (f->stem);
            }
        }

      /* Free name if not needed further.  */
      if (f != 0 && name != f->name
	  && (name < f->name || name > f->name + strlen (f->name)))
	{
	  free (name);
	  name = f->name;
	}

      /* If this target is a default target, update DEFAULT_GOAL_FILE.  */
      if (streq (*default_goal_name, name)
          && (default_goal_file == 0
              || ! streq (default_goal_file->name, name)))
        default_goal_file = f;
    }

  if (implicit)
    {
      targets[target_idx] = 0;
      target_percents[target_idx] = 0;
      if (deps)
        deps->need_2nd_expansion = second_expansion;
      create_pattern_rule (targets, target_percents, two_colon, deps, cmds, 1);
      free ((char *) target_percents);
    }
}

/* Search STRING for an unquoted STOPCHAR or blank (if BLANK is nonzero).
   Backslashes quote STOPCHAR, blanks if BLANK is nonzero, and backslash.
   Quoting backslashes are removed from STRING by compacting it into
   itself.  Returns a pointer to the first unquoted STOPCHAR if there is
   one, or nil if there are none.  STOPCHARs inside variable references are
   ignored if IGNOREVARS is true.

   STOPCHAR _cannot_ be '$' if IGNOREVARS is true.  */

static char *
find_char_unquote (char *string, int stop1, int stop2, int blank,
                   int ignorevars)
{
  unsigned int string_len = 0;
  register char *p = string;

  if (ignorevars)
    ignorevars = '$';

  while (1)
    {
      if (stop2 && blank)
	while (*p != '\0' && *p != ignorevars && *p != stop1 && *p != stop2
	       && ! isblank ((unsigned char) *p))
	  ++p;
      else if (stop2)
	while (*p != '\0' && *p != ignorevars && *p != stop1 && *p != stop2)
	  ++p;
      else if (blank)
	while (*p != '\0' && *p != ignorevars && *p != stop1
	       && ! isblank ((unsigned char) *p))
	  ++p;
      else
	while (*p != '\0' && *p != ignorevars && *p != stop1)
	  ++p;

      if (*p == '\0')
	break;

      /* If we stopped due to a variable reference, skip over its contents.  */
      if (*p == ignorevars)
        {
          char openparen = p[1];

          p += 2;

          /* Skip the contents of a non-quoted, multi-char variable ref.  */
          if (openparen == '(' || openparen == '{')
            {
              unsigned int pcount = 1;
              char closeparen = (openparen == '(' ? ')' : '}');

              while (*p)
                {
                  if (*p == openparen)
                    ++pcount;
                  else if (*p == closeparen)
                    if (--pcount == 0)
                      {
                        ++p;
                        break;
                      }
                  ++p;
                }
            }

          /* Skipped the variable reference: look for STOPCHARS again.  */
          continue;
        }

      if (p > string && p[-1] == '\\')
	{
	  /* Search for more backslashes.  */
	  register int i = -2;
	  while (&p[i] >= string && p[i] == '\\')
	    --i;
	  ++i;
	  /* Only compute the length if really needed.  */
	  if (string_len == 0)
	    string_len = strlen (string);
	  /* The number of backslashes is now -I.
	     Copy P over itself to swallow half of them.  */
	  bcopy (&p[i / 2], &p[i], (string_len - (p - string)) - (i / 2) + 1);
	  p += i / 2;
	  if (i % 2 == 0)
	    /* All the backslashes quoted each other; the STOPCHAR was
	       unquoted.  */
	    return p;

	  /* The STOPCHAR was quoted by a backslash.  Look for another.  */
	}
      else
	/* No backslash in sight.  */
	return p;
    }

  /* Never hit a STOPCHAR or blank (with BLANK nonzero).  */
  return 0;
}

/* Search PATTERN for an unquoted %.  */

char *
find_percent (char *pattern)
{
  return find_char_unquote (pattern, '%', 0, 0, 0);
}

/* Parse a string into a sequence of filenames represented as a
   chain of struct nameseq's in reverse order and return that chain.

   The string is passed as STRINGP, the address of a string pointer.
   The string pointer is updated to point at the first character
   not parsed, which either is a null char or equals STOPCHAR.

   SIZE is how big to construct chain elements.
   This is useful if we want them actually to be other structures
   that have room for additional info.

   If STRIP is nonzero, strip `./'s off the beginning.  */

struct nameseq *
parse_file_seq (char **stringp, int stopchar, unsigned int size, int strip)
{
  struct nameseq *new = 0;
  struct nameseq *new1, *lastnew1;
  char *p = *stringp;
  char *q;
  char *name;

#ifdef VMS
# define VMS_COMMA ','
#else
# define VMS_COMMA 0
#endif

  while (1)
    {
      /* Skip whitespace; see if any more names are left.  */
      p = next_token (p);
      if (*p == '\0')
	break;
      if (*p == stopchar)
	break;

      /* Yes, find end of next name.  */
      q = p;
      p = find_char_unquote (q, stopchar, VMS_COMMA, 1, 0);
#ifdef VMS
	/* convert comma separated list to space separated */
      if (p && *p == ',')
	*p =' ';
#endif
#ifdef _AMIGA
      if (stopchar == ':' && p && *p == ':'
          && !(isspace ((unsigned char)p[1]) || !p[1]
               || isspace ((unsigned char)p[-1])))
      {
	p = find_char_unquote (p+1, stopchar, VMS_COMMA, 1, 0);
      }
#endif
#if defined HAVE_DOS_PATHS || defined __CYGWIN32__
    /* For DOS paths, skip a "C:\..." or a "C:/..." until we find the
       first colon which isn't followed by a slash or a backslash.
       Note that tokens separated by spaces should be treated as separate
       tokens since make doesn't allow path names with spaces */
    if (stopchar == ':')
      while (p != 0 && !isspace ((unsigned char)*p) &&
             (p[1] == '\\' || p[1] == '/') && isalpha ((unsigned char)p[-1]))
        p = find_char_unquote (p + 1, stopchar, VMS_COMMA, 1, 0);
#endif
      if (p == 0)
	p = q + strlen (q);

      if (strip)
#ifdef VMS
	/* Skip leading `[]'s.  */
	while (p - q > 2 && q[0] == '[' && q[1] == ']')
#else
	/* Skip leading `./'s.  */
	while (p - q > 2 && q[0] == '.' && q[1] == '/')
#endif
	  {
	    q += 2;		/* Skip "./".  */
	    while (q < p && *q == '/')
	      /* Skip following slashes: ".//foo" is "foo", not "/foo".  */
	      ++q;
	  }

      /* Extract the filename just found, and skip it.  */

      if (q == p)
	/* ".///" was stripped to "". */
#ifdef VMS
	continue;
#else
#ifdef _AMIGA
	name = savestring ("", 0);
#else
	name = savestring ("./", 2);
#endif
#endif
      else
#ifdef VMS
/* VMS filenames can have a ':' in them but they have to be '\'ed but we need
 *  to remove this '\' before we can use the filename.
 * Savestring called because q may be read-only string constant.
 */
	{
	  char *qbase = xstrdup (q);
	  char *pbase = qbase + (p-q);
	  char *q1 = qbase;
	  char *q2 = q1;
	  char *p1 = pbase;

	  while (q1 != pbase)
	    {
	      if (*q1 == '\\' && *(q1+1) == ':')
		{
		  q1++;
		  p1--;
		}
	      *q2++ = *q1++;
	    }
	  name = savestring (qbase, p1 - qbase);
	  free (qbase);
	}
#else
	name = savestring (q, p - q);
#endif

      /* Add it to the front of the chain.  */
      new1 = (struct nameseq *) xmalloc (size);
      new1->name = name;
      new1->next = new;
      new = new1;
    }

#ifndef NO_ARCHIVES

  /* Look for multi-word archive references.
     They are indicated by a elt ending with an unmatched `)' and
     an elt further down the chain (i.e., previous in the file list)
     with an unmatched `(' (e.g., "lib(mem").  */

  new1 = new;
  lastnew1 = 0;
  while (new1 != 0)
    if (new1->name[0] != '('	/* Don't catch "(%)" and suchlike.  */
	&& new1->name[strlen (new1->name) - 1] == ')'
	&& strchr (new1->name, '(') == 0)
      {
	/* NEW1 ends with a `)' but does not contain a `('.
	   Look back for an elt with an opening `(' but no closing `)'.  */

	struct nameseq *n = new1->next, *lastn = new1;
	char *paren = 0;
	while (n != 0 && (paren = strchr (n->name, '(')) == 0)
	  {
	    lastn = n;
	    n = n->next;
	  }
	if (n != 0
	    /* Ignore something starting with `(', as that cannot actually
	       be an archive-member reference (and treating it as such
	       results in an empty file name, which causes much lossage).  */
	    && n->name[0] != '(')
	  {
	    /* N is the first element in the archive group.
	       Its name looks like "lib(mem" (with no closing `)').  */

	    char *libname;

	    /* Copy "lib(" into LIBNAME.  */
	    ++paren;
	    libname = (char *) alloca (paren - n->name + 1);
	    bcopy (n->name, libname, paren - n->name);
	    libname[paren - n->name] = '\0';

	    if (*paren == '\0')
	      {
		/* N was just "lib(", part of something like "lib( a b)".
		   Edit it out of the chain and free its storage.  */
		lastn->next = n->next;
		free (n->name);
		free ((char *) n);
		/* LASTN->next is the new stopping elt for the loop below.  */
		n = lastn->next;
	      }
	    else
	      {
		/* Replace N's name with the full archive reference.  */
		name = concat (libname, paren, ")");
		free (n->name);
		n->name = name;
	      }

	    if (new1->name[1] == '\0')
	      {
		/* NEW1 is just ")", part of something like "lib(a b )".
		   Omit it from the chain and free its storage.  */
		if (lastnew1 == 0)
		  new = new1->next;
		else
		  lastnew1->next = new1->next;
		lastn = new1;
		new1 = new1->next;
		free (lastn->name);
		free ((char *) lastn);
	      }
	    else
	      {
		/* Replace also NEW1->name, which already has closing `)'.  */
		name = concat (libname, new1->name, "");
		free (new1->name);
		new1->name = name;
		new1 = new1->next;
	      }

	    /* Trace back from NEW1 (the end of the list) until N
	       (the beginning of the list), rewriting each name
	       with the full archive reference.  */

	    while (new1 != n)
	      {
		name = concat (libname, new1->name, ")");
		free (new1->name);
		new1->name = name;
		lastnew1 = new1;
		new1 = new1->next;
	      }
	  }
	else
	  {
	    /* No frobnication happening.  Just step down the list.  */
	    lastnew1 = new1;
	    new1 = new1->next;
	  }
      }
    else
      {
	lastnew1 = new1;
	new1 = new1->next;
      }

#endif

  *stringp = p;
  return new;
}

/* Find the next line of text in an eval buffer, combining continuation lines
   into one line.
   Return the number of actual lines read (> 1 if continuation lines).
   Returns -1 if there's nothing left in the buffer.

   After this function, ebuf->buffer points to the first character of the
   line we just found.
 */

/* Read a line of text from a STRING.
   Since we aren't really reading from a file, don't bother with linenumbers.
 */

static unsigned long
readstring (struct ebuffer *ebuf)
{
  char *eol;

  /* If there is nothing left in this buffer, return 0.  */
  if (ebuf->bufnext >= ebuf->bufstart + ebuf->size)
    return -1;

  /* Set up a new starting point for the buffer, and find the end of the
     next logical line (taking into account backslash/newline pairs).  */

  eol = ebuf->buffer = ebuf->bufnext;

  while (1)
    {
      int backslash = 0;
      char *bol = eol;
      char *p;

      /* Find the next newline.  At EOS, stop.  */
      eol = p = strchr (eol , '\n');
      if (!eol)
        {
          ebuf->bufnext = ebuf->bufstart + ebuf->size + 1;
          return 0;
        }

      /* Found a newline; if it's escaped continue; else we're done.  */
      while (p > bol && *(--p) == '\\')
        backslash = !backslash;
      if (!backslash)
        break;
      ++eol;
    }

  /* Overwrite the newline char.  */
  *eol = '\0';
  ebuf->bufnext = eol+1;

  return 0;
}

static long
readline (struct ebuffer *ebuf)
{
  char *p;
  char *end;
  char *start;
  long nlines = 0;

  /* The behaviors between string and stream buffers are different enough to
     warrant different functions.  Do the Right Thing.  */

  if (!ebuf->fp)
    return readstring (ebuf);

  /* When reading from a file, we always start over at the beginning of the
     buffer for each new line.  */

  p = start = ebuf->bufstart;
  end = p + ebuf->size;
  *p = '\0';

  while (fgets (p, end - p, ebuf->fp) != 0)
    {
      char *p2;
      unsigned long len;
      int backslash;

      len = strlen (p);
      if (len == 0)
	{
	  /* This only happens when the first thing on the line is a '\0'.
	     It is a pretty hopeless case, but (wonder of wonders) Athena
	     lossage strikes again!  (xmkmf puts NULs in its makefiles.)
	     There is nothing really to be done; we synthesize a newline so
	     the following line doesn't appear to be part of this line.  */
	  error (&ebuf->floc,
                 _("warning: NUL character seen; rest of line ignored"));
	  p[0] = '\n';
	  len = 1;
	}

      /* Jump past the text we just read.  */
      p += len;

      /* If the last char isn't a newline, the whole line didn't fit into the
         buffer.  Get some more buffer and try again.  */
      if (p[-1] != '\n')
        goto more_buffer;

      /* We got a newline, so add one to the count of lines.  */
      ++nlines;

#if !defined(WINDOWS32) && !defined(__MSDOS__) && !defined(__EMX__)
      /* Check to see if the line was really ended with CRLF; if so ignore
         the CR.  */
      if ((p - start) > 1 && p[-2] == '\r')
        {
          --p;
          p[-1] = '\n';
        }
#endif

      backslash = 0;
      for (p2 = p - 2; p2 >= start; --p2)
	{
	  if (*p2 != '\\')
	    break;
          backslash = !backslash;
	}

      if (!backslash)
	{
	  p[-1] = '\0';
	  break;
	}

      /* It was a backslash/newline combo.  If we have more space, read
         another line.  */
      if (end - p >= 80)
        continue;

      /* We need more space at the end of our buffer, so realloc it.
         Make sure to preserve the current offset of p.  */
    more_buffer:
      {
        unsigned long off = p - start;
        ebuf->size *= 2;
        start = ebuf->buffer = ebuf->bufstart = (char *) xrealloc (start,
                                                                   ebuf->size);
        p = start + off;
        end = start + ebuf->size;
        *p = '\0';
      }
    }

  if (ferror (ebuf->fp))
    pfatal_with_name (ebuf->floc.filenm);

  /* If we found some lines, return how many.
     If we didn't, but we did find _something_, that indicates we read the last
     line of a file with no final newline; return 1.
     If we read nothing, we're at EOF; return -1.  */

  return nlines ? nlines : p == ebuf->bufstart ? -1 : 1;
}

/* Parse the next "makefile word" from the input buffer, and return info
   about it.

   A "makefile word" is one of:

     w_bogus        Should never happen
     w_eol          End of input
     w_static       A static word; cannot be expanded
     w_variable     A word containing one or more variables/functions
     w_colon        A colon
     w_dcolon       A double-colon
     w_semicolon    A semicolon
     w_varassign    A variable assignment operator (=, :=, +=, or ?=)

   Note that this function is only used when reading certain parts of the
   makefile.  Don't use it where special rules hold sway (RHS of a variable,
   in a command list, etc.)  */

static enum make_word_type
get_next_mword (char *buffer, char *delim, char **startp, unsigned int *length)
{
  enum make_word_type wtype = w_bogus;
  char *p = buffer, *beg;
  char c;

  /* Skip any leading whitespace.  */
  while (isblank ((unsigned char)*p))
    ++p;

  beg = p;
  c = *(p++);
  switch (c)
    {
    case '\0':
      wtype = w_eol;
      break;

    case ';':
      wtype = w_semicolon;
      break;

    case '=':
      wtype = w_varassign;
      break;

    case ':':
      wtype = w_colon;
      switch (*p)
        {
        case ':':
          ++p;
          wtype = w_dcolon;
          break;

        case '=':
          ++p;
          wtype = w_varassign;
          break;
        }
      break;

    case '+':
    case '?':
      if (*p == '=')
        {
          ++p;
          wtype = w_varassign;
          break;
        }

    default:
      if (delim && strchr (delim, c))
        wtype = w_static;
      break;
    }

  /* Did we find something?  If so, return now.  */
  if (wtype != w_bogus)
    goto done;

  /* This is some non-operator word.  A word consists of the longest
     string of characters that doesn't contain whitespace, one of [:=#],
     or [?+]=, or one of the chars in the DELIM string.  */

  /* We start out assuming a static word; if we see a variable we'll
     adjust our assumptions then.  */
  wtype = w_static;

  /* We already found the first value of "c", above.  */
  while (1)
    {
      char closeparen;
      int count;

      switch (c)
        {
        case '\0':
        case ' ':
        case '\t':
        case '=':
          goto done_word;

        case ':':
#if defined HAVE_DOS_PATHS || defined __CYGWIN32__
	  /* A word CAN include a colon in its drive spec.  The drive
	     spec is allowed either at the beginning of a word, or as part
	     of the archive member name, like in "libfoo.a(d:/foo/bar.o)".  */
	  if (!(p - beg >= 2
		&& (*p == '/' || *p == '\\') && isalpha ((unsigned char)p[-2])
		&& (p - beg == 2 || p[-3] == '(')))
#endif
	  goto done_word;

        case '$':
          c = *(p++);
          if (c == '$')
            break;

          /* This is a variable reference, so note that it's expandable.
             Then read it to the matching close paren.  */
          wtype = w_variable;

          if (c == '(')
            closeparen = ')';
          else if (c == '{')
            closeparen = '}';
          else
            /* This is a single-letter variable reference.  */
            break;

          for (count=0; *p != '\0'; ++p)
            {
              if (*p == c)
                ++count;
              else if (*p == closeparen && --count < 0)
                {
                  ++p;
                  break;
                }
            }
          break;

        case '?':
        case '+':
          if (*p == '=')
            goto done_word;
          break;

        case '\\':
          switch (*p)
            {
            case ':':
            case ';':
            case '=':
            case '\\':
              ++p;
              break;
            }
          break;

        default:
          if (delim && strchr (delim, c))
            goto done_word;
          break;
        }

      c = *(p++);
    }
 done_word:
  --p;

 done:
  if (startp)
    *startp = beg;
  if (length)
    *length = p - beg;
  return wtype;
}

/* Construct the list of include directories
   from the arguments and the default list.  */

void
construct_include_path (char **arg_dirs)
{
  register unsigned int i;
#ifdef VAXC		/* just don't ask ... */
  stat_t stbuf;
#else
  struct stat stbuf;
#endif
  /* Table to hold the dirs.  */

  register unsigned int defsize = (sizeof (default_include_directories)
				   / sizeof (default_include_directories[0]));
  register unsigned int max = 5;
  register char **dirs = (char **) xmalloc ((5 + defsize) * sizeof (char *));
  register unsigned int idx = 0;

#ifdef  __MSDOS__
  defsize++;
#endif

  /* First consider any dirs specified with -I switches.
     Ignore dirs that don't exist.  */

  if (arg_dirs != 0)
    while (*arg_dirs != 0)
      {
	char *dir = *arg_dirs++;
        int e;

	if (dir[0] == '~')
	  {
	    char *expanded = tilde_expand (dir);
	    if (expanded != 0)
	      dir = expanded;
	  }

        EINTRLOOP (e, stat (dir, &stbuf));
	if (e == 0 && S_ISDIR (stbuf.st_mode))
	  {
	    if (idx == max - 1)
	      {
		max += 5;
		dirs = (char **)
		  xrealloc ((char *) dirs, (max + defsize) * sizeof (char *));
	      }
	    dirs[idx++] = dir;
	  }
	else if (dir != arg_dirs[-1])
	  free (dir);
      }

  /* Now add at the end the standard default dirs.  */

#ifdef  __MSDOS__
  {
    /* The environment variable $DJDIR holds the root of the
       DJGPP directory tree; add ${DJDIR}/include.  */
    struct variable *djdir = lookup_variable ("DJDIR", 5);

    if (djdir)
      {
	char *defdir = (char *) xmalloc (strlen (djdir->value) + 8 + 1);

	strcat (strcpy (defdir, djdir->value), "/include");
	dirs[idx++] = defdir;
      }
  }
#endif

  for (i = 0; default_include_directories[i] != 0; ++i)
    {
      int e;

      EINTRLOOP (e, stat (default_include_directories[i], &stbuf));
      if (e == 0 && S_ISDIR (stbuf.st_mode))
        dirs[idx++] = default_include_directories[i];
    }

  dirs[idx] = 0;

  /* Now compute the maximum length of any name in it. Also add each
     dir to the .INCLUDE_DIRS variable.  */

  max_incl_len = 0;
  for (i = 0; i < idx; ++i)
    {
      unsigned int len = strlen (dirs[i]);
      /* If dir name is written with a trailing slash, discard it.  */
      if (dirs[i][len - 1] == '/')
	/* We can't just clobber a null in because it may have come from
	   a literal string and literal strings may not be writable.  */
	dirs[i] = savestring (dirs[i], len - 1);
      if (len > max_incl_len)
	max_incl_len = len;

      /* Append to .INCLUDE_DIRS.   */
      do_variable_definition (NILF, ".INCLUDE_DIRS", dirs[i],
                              o_default, f_append, 0);
    }

  include_directories = dirs;
}

/* Expand ~ or ~USER at the beginning of NAME.
   Return a newly malloc'd string or 0.  */

char *
tilde_expand (char *name)
{
#ifndef VMS
  if (name[1] == '/' || name[1] == '\0')
    {
      extern char *getenv ();
      char *home_dir;
      int is_variable;

      {
	/* Turn off --warn-undefined-variables while we expand HOME.  */
	int save = warn_undefined_variables_flag;
	warn_undefined_variables_flag = 0;

	home_dir = allocated_variable_expand ("$(HOME)");

	warn_undefined_variables_flag = save;
      }

      is_variable = home_dir[0] != '\0';
      if (!is_variable)
	{
	  free (home_dir);
	  home_dir = getenv ("HOME");
	}
#if !defined(_AMIGA) && !defined(WINDOWS32)
      if (home_dir == 0 || home_dir[0] == '\0')
	{
	  extern char *getlogin ();
	  char *logname = getlogin ();
	  home_dir = 0;
	  if (logname != 0)
	    {
	      struct passwd *p = getpwnam (logname);
	      if (p != 0)
		home_dir = p->pw_dir;
	    }
	}
#endif /* !AMIGA && !WINDOWS32 */
      if (home_dir != 0)
	{
	  char *new = concat (home_dir, "", name + 1);
	  if (is_variable)
	    free (home_dir);
	  return new;
	}
    }
#if !defined(_AMIGA) && !defined(WINDOWS32)
  else
    {
      struct passwd *pwent;
      char *userend = strchr (name + 1, '/');
      if (userend != 0)
	*userend = '\0';
      pwent = getpwnam (name + 1);
      if (pwent != 0)
	{
	  if (userend == 0)
	    return xstrdup (pwent->pw_dir);
	  else
	    return concat (pwent->pw_dir, "/", userend + 1);
	}
      else if (userend != 0)
	*userend = '/';
    }
#endif /* !AMIGA && !WINDOWS32 */
#endif /* !VMS */
  return 0;
}

/* Given a chain of struct nameseq's describing a sequence of filenames,
   in reverse of the intended order, return a new chain describing the
   result of globbing the filenames.  The new chain is in forward order.
   The links of the old chain are freed or used in the new chain.
   Likewise for the names in the old chain.

   SIZE is how big to construct chain elements.
   This is useful if we want them actually to be other structures
   that have room for additional info.  */

struct nameseq *
multi_glob (struct nameseq *chain, unsigned int size)
{
  extern void dir_setup_glob ();
  register struct nameseq *new = 0;
  register struct nameseq *old;
  struct nameseq *nexto;
  glob_t gl;

  dir_setup_glob (&gl);

  for (old = chain; old != 0; old = nexto)
    {
#ifndef NO_ARCHIVES
      char *memname;
#endif

      nexto = old->next;

      if (old->name[0] == '~')
	{
	  char *newname = tilde_expand (old->name);
	  if (newname != 0)
	    {
	      free (old->name);
	      old->name = newname;
	    }
	}

#ifndef NO_ARCHIVES
      if (ar_name (old->name))
	{
	  /* OLD->name is an archive member reference.
	     Replace it with the archive file name,
	     and save the member name in MEMNAME.
	     We will glob on the archive name and then
	     reattach MEMNAME later.  */
	  char *arname;
	  ar_parse_name (old->name, &arname, &memname);
	  free (old->name);
	  old->name = arname;
	}
      else
	memname = 0;
#endif /* !NO_ARCHIVES */

      switch (glob (old->name, GLOB_NOCHECK|GLOB_ALTDIRFUNC, NULL, &gl))
	{
	case 0:			/* Success.  */
	  {
	    register int i = gl.gl_pathc;
	    while (i-- > 0)
	      {
#ifndef NO_ARCHIVES
		if (memname != 0)
		  {
		    /* Try to glob on MEMNAME within the archive.  */
		    struct nameseq *found
		      = ar_glob (gl.gl_pathv[i], memname, size);
		    if (found == 0)
		      {
			/* No matches.  Use MEMNAME as-is.  */
			unsigned int alen = strlen (gl.gl_pathv[i]);
			unsigned int mlen = strlen (memname);
			struct nameseq *elt
			  = (struct nameseq *) xmalloc (size);
                        if (size > sizeof (struct nameseq))
                          bzero (((char *) elt) + sizeof (struct nameseq),
                                 size - sizeof (struct nameseq));
			elt->name = (char *) xmalloc (alen + 1 + mlen + 2);
			bcopy (gl.gl_pathv[i], elt->name, alen);
			elt->name[alen] = '(';
			bcopy (memname, &elt->name[alen + 1], mlen);
			elt->name[alen + 1 + mlen] = ')';
			elt->name[alen + 1 + mlen + 1] = '\0';
			elt->next = new;
			new = elt;
		      }
		    else
		      {
			/* Find the end of the FOUND chain.  */
			struct nameseq *f = found;
			while (f->next != 0)
			  f = f->next;

			/* Attach the chain being built to the end of the FOUND
			   chain, and make FOUND the new NEW chain.  */
			f->next = new;
			new = found;
		      }

		    free (memname);
		  }
		else
#endif /* !NO_ARCHIVES */
		  {
		    struct nameseq *elt = (struct nameseq *) xmalloc (size);
                    if (size > sizeof (struct nameseq))
                      bzero (((char *) elt) + sizeof (struct nameseq),
                             size - sizeof (struct nameseq));
		    elt->name = xstrdup (gl.gl_pathv[i]);
		    elt->next = new;
		    new = elt;
		  }
	      }
	    globfree (&gl);
	    free (old->name);
	    free ((char *)old);
	    break;
	  }

	case GLOB_NOSPACE:
	  fatal (NILF, _("virtual memory exhausted"));
	  break;

	default:
	  old->next = new;
	  new = old;
	  break;
	}
    }

  return new;
}
