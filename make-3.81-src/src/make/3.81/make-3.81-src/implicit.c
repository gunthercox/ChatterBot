/* Implicit rule searching for GNU Make.
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
#include "filedef.h"
#include "rule.h"
#include "dep.h"
#include "debug.h"
#include "variable.h"
#include "job.h"      /* struct child, used inside commands.h */
#include "commands.h" /* set_file_variables */

static int
pattern_search PARAMS ((struct file *file, int archive,
                        unsigned int depth, unsigned int recursions));

/* For a FILE which has no commands specified, try to figure out some
   from the implicit pattern rules.
   Returns 1 if a suitable implicit rule was found,
   after modifying FILE to contain the appropriate commands and deps,
   or returns 0 if no implicit rule was found.  */

int
try_implicit_rule (struct file *file, unsigned int depth)
{
  DBF (DB_IMPLICIT, _("Looking for an implicit rule for `%s'.\n"));

  /* The order of these searches was previously reversed.  My logic now is
     that since the non-archive search uses more information in the target
     (the archive search omits the archive name), it is more specific and
     should come first.  */

  if (pattern_search (file, 0, depth, 0))
    return 1;

#ifndef	NO_ARCHIVES
  /* If this is an archive member reference, use just the
     archive member name to search for implicit rules.  */
  if (ar_name (file->name))
    {
      DBF (DB_IMPLICIT,
           _("Looking for archive-member implicit rule for `%s'.\n"));
      if (pattern_search (file, 1, depth, 0))
	return 1;
    }
#endif

  return 0;
}


/* Struct idep captures information about implicit prerequisites
   that come from implicit rules. */
struct idep
{
  struct idep *next;              /* struct dep -compatible interface */
  char *name;                     /* name of the prerequisite */
  struct file *intermediate_file; /* intermediate file, 0 otherwise */
  char *intermediate_pattern;     /* pattern for intermediate file */
  unsigned char had_stem;         /* had % substituted with stem */
  unsigned char ignore_mtime;     /* ignore_mtime flag */
};

static void
free_idep_chain (struct idep *p)
{
  struct idep *n;

  for (; p != 0; p = n)
    {
      n = p->next;

      if (p->name)
        {
          struct file *f = p->intermediate_file;

          if (f != 0
              && (f->stem < f->name || f->stem > f->name + strlen (f->name)))
            free (f->stem);

          free (p->name);
        }

      free (p);
    }
}


/* Scans the BUFFER for the next word with whitespace as a separator.
   Returns the pointer to the beginning of the word. LENGTH hold the
   length of the word.  */

static char *
get_next_word (char *buffer, unsigned int *length)
{
  char *p = buffer, *beg;
  char c;

  /* Skip any leading whitespace.  */
  while (isblank ((unsigned char)*p))
    ++p;

  beg = p;
  c = *(p++);

  if (c == '\0')
    return 0;


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
          goto done_word;

        case '$':
          c = *(p++);
          if (c == '$')
            break;

          /* This is a variable reference, so read it to the matching
             close paren.  */

          if (c == '(')
            closeparen = ')';
          else if (c == '{')
            closeparen = '}';
          else
            /* This is a single-letter variable reference.  */
            break;

          for (count = 0; *p != '\0'; ++p)
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

        case '|':
          goto done;

        default:
          break;
        }

      c = *(p++);
    }
 done_word:
  --p;

 done:
  if (length)
    *length = p - beg;

  return beg;
}

/* Search the pattern rules for a rule with an existing dependency to make
   FILE.  If a rule is found, the appropriate commands and deps are put in FILE
   and 1 is returned.  If not, 0 is returned.

   If ARCHIVE is nonzero, FILE->name is of the form "LIB(MEMBER)".  A rule for
   "(MEMBER)" will be searched for, and "(MEMBER)" will not be chopped up into
   directory and filename parts.

   If an intermediate file is found by pattern search, the intermediate file
   is set up as a target by the recursive call and is also made a dependency
   of FILE.

   DEPTH is used for debugging messages.  */

static int
pattern_search (struct file *file, int archive,
                unsigned int depth, unsigned int recursions)
{
  /* Filename we are searching for a rule for.  */
  char *filename = archive ? strchr (file->name, '(') : file->name;

  /* Length of FILENAME.  */
  unsigned int namelen = strlen (filename);

  /* The last slash in FILENAME (or nil if there is none).  */
  char *lastslash;

  /* This is a file-object used as an argument in
     recursive calls.  It never contains any data
     except during a recursive call.  */
  struct file *intermediate_file = 0;

  /* This linked list records all the prerequisites actually
     found for a rule along with some other useful information
     (see struct idep for details). */
  struct idep* deps = 0;

  /* 1 if we need to remove explicit prerequisites, 0 otherwise. */
  unsigned int remove_explicit_deps = 0;

  /* Names of possible dependencies are constructed in this buffer.  */
  register char *depname = (char *) alloca (namelen + max_pattern_dep_length);

  /* The start and length of the stem of FILENAME for the current rule.  */
  register char *stem = 0;
  register unsigned int stemlen = 0;
  register unsigned int fullstemlen = 0;

  /* Buffer in which we store all the rules that are possibly applicable.  */
  struct rule **tryrules
    = (struct rule **) xmalloc (num_pattern_rules * max_pattern_targets
                                * sizeof (struct rule *));

  /* Number of valid elements in TRYRULES.  */
  unsigned int nrules;

  /* The numbers of the rule targets of each rule
     in TRYRULES that matched the target file.  */
  unsigned int *matches
    = (unsigned int *) alloca (num_pattern_rules * sizeof (unsigned int));

  /* Each element is nonzero if LASTSLASH was used in
     matching the corresponding element of TRYRULES.  */
  char *checked_lastslash
    = (char *) alloca (num_pattern_rules * sizeof (char));

  /* The index in TRYRULES of the rule we found.  */
  unsigned int foundrule;

  /* Nonzero if should consider intermediate files as dependencies.  */
  int intermed_ok;

  /* Nonzero if we have matched a pattern-rule target
     that is not just `%'.  */
  int specific_rule_matched = 0;

  unsigned int i = 0;  /* uninit checks OK */
  struct rule *rule;
  struct dep *dep, *expl_d;

  char *p, *vname;

  struct idep *d;
  struct idep **id_ptr;
  struct dep **d_ptr;

  PATH_VAR (stem_str); /* @@ Need to get rid of stem, stemlen, etc. */

#ifndef	NO_ARCHIVES
  if (archive || ar_name (filename))
    lastslash = 0;
  else
#endif
    {
      /* Set LASTSLASH to point at the last slash in FILENAME
	 but not counting any slash at the end.  (foo/bar/ counts as
	 bar/ in directory foo/, not empty in directory foo/bar/.)  */
#ifdef VMS
      lastslash = strrchr (filename, ']');
      if (lastslash == 0)
	lastslash = strrchr (filename, ':');
#else
      lastslash = strrchr (filename, '/');
#ifdef HAVE_DOS_PATHS
      /* Handle backslashes (possibly mixed with forward slashes)
	 and the case of "d:file".  */
      {
	char *bslash = strrchr (filename, '\\');
	if (lastslash == 0 || bslash > lastslash)
	  lastslash = bslash;
	if (lastslash == 0 && filename[0] && filename[1] == ':')
	  lastslash = filename + 1;
      }
#endif
#endif
      if (lastslash != 0 && lastslash[1] == '\0')
	lastslash = 0;
    }

  /* First see which pattern rules match this target
     and may be considered.  Put them in TRYRULES.  */

  nrules = 0;
  for (rule = pattern_rules; rule != 0; rule = rule->next)
    {
      /* If the pattern rule has deps but no commands, ignore it.
	 Users cancel built-in rules by redefining them without commands.  */
      if (rule->deps != 0 && rule->cmds == 0)
	continue;

      /* If this rule is in use by a parent pattern_search,
	 don't use it here.  */
      if (rule->in_use)
	{
	  DBS (DB_IMPLICIT, (_("Avoiding implicit rule recursion.\n")));
	  continue;
	}

      for (i = 0; rule->targets[i] != 0; ++i)
	{
	  char *target = rule->targets[i];
	  char *suffix = rule->suffixes[i];
	  int check_lastslash;

	  /* Rules that can match any filename and are not terminal
	     are ignored if we're recursing, so that they cannot be
	     intermediate files.  */
	  if (recursions > 0 && target[1] == '\0' && !rule->terminal)
	    continue;

	  if (rule->lens[i] > namelen)
	    /* It can't possibly match.  */
	    continue;

	  /* From the lengths of the filename and the pattern parts,
	     find the stem: the part of the filename that matches the %.  */
	  stem = filename + (suffix - target - 1);
	  stemlen = namelen - rule->lens[i] + 1;

	  /* Set CHECK_LASTSLASH if FILENAME contains a directory
	     prefix and the target pattern does not contain a slash.  */

          check_lastslash = 0;
          if (lastslash)
            {
#ifdef VMS
              check_lastslash = (strchr (target, ']') == 0
                                 && strchr (target, ':') == 0);
#else
              check_lastslash = strchr (target, '/') == 0;
#ifdef HAVE_DOS_PATHS
              /* Didn't find it yet: check for DOS-type directories.  */
              if (check_lastslash)
                {
                  char *b = strchr (target, '\\');
                  check_lastslash = !(b || (target[0] && target[1] == ':'));
                }
#endif
#endif
            }
	  if (check_lastslash)
	    {
	      /* If so, don't include the directory prefix in STEM here.  */
	      unsigned int difference = lastslash - filename + 1;
	      if (difference > stemlen)
		continue;
	      stemlen -= difference;
	      stem += difference;
	    }

	  /* Check that the rule pattern matches the text before the stem.  */
	  if (check_lastslash)
	    {
	      if (stem > (lastslash + 1)
		  && !strneq (target, lastslash + 1, stem - lastslash - 1))
		continue;
	    }
	  else if (stem > filename
		   && !strneq (target, filename, stem - filename))
	    continue;

	  /* Check that the rule pattern matches the text after the stem.
	     We could test simply use streq, but this way we compare the
	     first two characters immediately.  This saves time in the very
	     common case where the first character matches because it is a
	     period.  */
	  if (*suffix != stem[stemlen]
	      || (*suffix != '\0' && !streq (&suffix[1], &stem[stemlen + 1])))
	    continue;

	  /* Record if we match a rule that not all filenames will match.  */
	  if (target[1] != '\0')
	    specific_rule_matched = 1;

	  /* A rule with no dependencies and no commands exists solely to set
	     specific_rule_matched when it matches.  Don't try to use it.  */
	  if (rule->deps == 0 && rule->cmds == 0)
	    continue;

	  /* Record this rule in TRYRULES and the index of the matching
	     target in MATCHES.  If several targets of the same rule match,
	     that rule will be in TRYRULES more than once.  */
	  tryrules[nrules] = rule;
	  matches[nrules] = i;
	  checked_lastslash[nrules] = check_lastslash;
	  ++nrules;
	}
    }

  /* If we have found a matching rule that won't match all filenames,
     retroactively reject any non-"terminal" rules that do always match.  */
  if (specific_rule_matched)
    for (i = 0; i < nrules; ++i)
      if (!tryrules[i]->terminal)
	{
	  register unsigned int j;
	  for (j = 0; tryrules[i]->targets[j] != 0; ++j)
	    if (tryrules[i]->targets[j][1] == '\0')
	      break;
	  if (tryrules[i]->targets[j] != 0)
	    tryrules[i] = 0;
	}

  /* We are going to do second expansion so initialize file variables
     for the rule. */
  initialize_file_variables (file, 0);

  /* Try each rule once without intermediate files, then once with them.  */
  for (intermed_ok = 0; intermed_ok == !!intermed_ok; ++intermed_ok)
    {
      /* Try each pattern rule till we find one that applies.
	 If it does, expand its dependencies (as substituted)
	 and chain them in DEPS.  */

      for (i = 0; i < nrules; i++)
	{
          struct file *f;
          unsigned int failed = 0;
	  int check_lastslash;
          int file_variables_set = 0;

	  rule = tryrules[i];

          remove_explicit_deps = 0;

	  /* RULE is nil when we discover that a rule,
	     already placed in TRYRULES, should not be applied.  */
	  if (rule == 0)
	    continue;

	  /* Reject any terminal rules if we're
	     looking to make intermediate files.  */
	  if (intermed_ok && rule->terminal)
	    continue;

	  /* Mark this rule as in use so a recursive
	     pattern_search won't try to use it.  */
	  rule->in_use = 1;

	  /* From the lengths of the filename and the matching pattern parts,
	     find the stem: the part of the filename that matches the %.  */
	  stem = filename
	    + (rule->suffixes[matches[i]] - rule->targets[matches[i]]) - 1;
	  stemlen = namelen - rule->lens[matches[i]] + 1;
	  check_lastslash = checked_lastslash[i];
	  if (check_lastslash)
	    {
	      stem += lastslash - filename + 1;
	      stemlen -= (lastslash - filename) + 1;
	    }

	  DBS (DB_IMPLICIT, (_("Trying pattern rule with stem `%.*s'.\n"),
                             (int) stemlen, stem));

          strncpy (stem_str, stem, stemlen);
          stem_str[stemlen] = '\0';

          /* Temporary assign STEM to file->stem (needed to set file
             variables below).   */
          file->stem = stem_str;

	  /* Try each dependency; see if it "exists".  */

	  for (dep = rule->deps; dep != 0; dep = dep->next)
	    {
              unsigned int len;
              char *p2;
              unsigned int order_only = 0; /* Set if '|' was seen. */

              /* In an ideal world we would take the dependency line,
                 substitute the stem, re-expand the whole line and chop it
                 into individual prerequisites. Unfortunately this won't work
                 because of the "check_lastslash" twist.  Instead, we will
                 have to go word by word, taking $()'s into account, for each
                 word we will substitute the stem, re-expand, chop it up, and,
                 if check_lastslash != 0, add the directory part to each
                 resulting prerequisite.  */

              p = get_next_word (dep->name, &len);

              while (1)
                {
                  int add_dir = 0;
                  int had_stem = 0;

                  if (p == 0)
                    break; /* No more words */

                  /* Is there a pattern in this prerequisite?  */

                  for (p2 = p; p2 < p + len && *p2 != '%'; ++p2)
                    ;

                  if (dep->need_2nd_expansion)
                    {
                      /* If the dependency name has %, substitute the stem.

                         Watch out, we are going to do something tricky
                         here. If we just replace % with the stem value,
                         later, when we do the second expansion, we will
                         re-expand this stem value once again. This is not
                         good especially if you have certain characters in
                         your stem (like $).

                         Instead, we will replace % with $* and allow the
                         second expansion to take care of it for us. This way
                         (since $* is a simple variable) there won't be
                         additional re-expansion of the stem.  */

                      if (p2 < p + len)
                        {
                          register unsigned int i = p2 - p;
                          bcopy (p, depname, i);
                          bcopy ("$*", depname + i, 2);
                          bcopy (p2 + 1, depname + i + 2, len - i - 1);
                          depname[len + 2 - 1] = '\0';

                          if (check_lastslash)
                            add_dir = 1;

                          had_stem = 1;
                        }
                      else
                        {
                          bcopy (p, depname, len);
                          depname[len] = '\0';
                        }

                      /* Set file variables. Note that we cannot do it once
                         at the beginning of the function because of the stem
                         value.  */
                      if (!file_variables_set)
                        {
                          set_file_variables (file);
                          file_variables_set = 1;
                        }

                      p2 = variable_expand_for_file (depname, file);
                    }
                  else
                    {
                       if (p2 < p + len)
                        {
                          register unsigned int i = p2 - p;
                          bcopy (p, depname, i);
                          bcopy (stem_str, depname + i, stemlen);
                          bcopy (p2 + 1, depname + i + stemlen, len - i - 1);
                          depname[len + stemlen - 1] = '\0';

                          if (check_lastslash)
                            add_dir = 1;

                          had_stem = 1;
                        }
                      else
                        {
                          bcopy (p, depname, len);
                          depname[len] = '\0';
                        }

                       p2 = depname;
                    }

                  /* Parse the dependencies. */

                  while (1)
                    {
                      id_ptr = &deps;

                      for (; *id_ptr; id_ptr = &(*id_ptr)->next)
                        ;

                      *id_ptr = (struct idep *)
                        multi_glob (
                          parse_file_seq (&p2,
                                          order_only ? '\0' : '|',
                                          sizeof (struct idep),
                                          1), sizeof (struct idep));

                      /* @@ It would be nice to teach parse_file_seq or
                         multi_glob to add prefix. This would save us some
                         reallocations. */

                      if (order_only || add_dir || had_stem)
                        {
                          unsigned long l = lastslash - filename + 1;

                          for (d = *id_ptr; d != 0; d = d->next)
                            {
                              if (order_only)
                                d->ignore_mtime = 1;

                              if (add_dir)
                                {
                                  char *p = d->name;

                                  d->name = xmalloc (strlen (p) + l + 1);

                                  bcopy (filename, d->name, l);
                                  bcopy (p, d->name + l, strlen (p) + 1);

                                  free (p);
                                }

                              if (had_stem)
                                d->had_stem = 1;
                            }
                        }

                      if (!order_only && *p2)
                      {
                        ++p2;
                        order_only = 1;
                        continue;
                      }

                      break;
                    }

                  p += len;
                  p = get_next_word (p, &len);
                }
	    }

          /* Reset the stem in FILE. */

          file->stem = 0;

          /* @@ This loop can be combined with the previous one. I do
             it separately for now for transparency.*/

          for (d = deps; d != 0; d = d->next)
            {
              char *name = d->name;

              if (file_impossible_p (name))
                {
                  /* If this dependency has already been ruled "impossible",
                     then the rule fails and don't bother trying it on the
                     second pass either since we know that will fail too.  */
                  DBS (DB_IMPLICIT,
                       (d->had_stem
                        ? _("Rejecting impossible implicit prerequisite `%s'.\n")
                        : _("Rejecting impossible rule prerequisite `%s'.\n"),
                        name));
                  tryrules[i] = 0;

                  failed = 1;
                  break;
                }

              DBS (DB_IMPLICIT,
                   (d->had_stem
                    ? _("Trying implicit prerequisite `%s'.\n")
                    : _("Trying rule prerequisite `%s'.\n"), name));

              /* If this prerequisite also happened to be explicitly mentioned
                 for FILE skip all the test below since it it has to be built
                 anyway, no matter which implicit rule we choose. */

              for (expl_d = file->deps; expl_d != 0; expl_d = expl_d->next)
                if (streq (dep_name (expl_d), name))
                  break;
              if (expl_d != 0)
                continue;

              /* The DEP->changed flag says that this dependency resides in a
                 nonexistent directory.  So we normally can skip looking for
                 the file.  However, if CHECK_LASTSLASH is set, then the
                 dependency file we are actually looking for is in a different
                 directory (the one gotten by prepending FILENAME's directory),
                 so it might actually exist.  */

              /* @@ dep->changed check is disabled. */
              if (((f = lookup_file (name)) != 0 && f->is_target)
                  /*|| ((!dep->changed || check_lastslash) && */
                  || file_exists_p (name))
                continue;

              /* This code, given FILENAME = "lib/foo.o", dependency name
                 "lib/foo.c", and VPATH=src, searches for "src/lib/foo.c".  */
              vname = name;
              if (vpath_search (&vname, (FILE_TIMESTAMP *) 0))
                {
                  DBS (DB_IMPLICIT,
                       (_("Found prerequisite `%s' as VPATH `%s'\n"),
                        name,
                        vname));

                  free (vname);
                  continue;
                }


              /* We could not find the file in any place we should look.  Try
                 to make this dependency as an intermediate file, but only on
                 the second pass.  */

              if (intermed_ok)
                {
                  if (intermediate_file == 0)
                    intermediate_file
                      = (struct file *) alloca (sizeof (struct file));

                  DBS (DB_IMPLICIT,
                       (_("Looking for a rule with intermediate file `%s'.\n"),
                        name));

                  bzero ((char *) intermediate_file, sizeof (struct file));
                  intermediate_file->name = name;
                  if (pattern_search (intermediate_file,
                                      0,
                                      depth + 1,
                                      recursions + 1))
                    {
                      d->intermediate_file = intermediate_file;
                      d->intermediate_pattern = intermediate_file->name;

                      intermediate_file->name = xstrdup (name);
                      intermediate_file = 0;

                      continue;
                    }

                  /* If we have tried to find P as an intermediate
                     file and failed, mark that name as impossible
                     so we won't go through the search again later.  */
                  if (intermediate_file->variables)
                    free_variable_set (intermediate_file->variables);
                  file_impossible (name);
                }

              /* A dependency of this rule does not exist. Therefore,
                 this rule fails.  */
              failed = 1;
              break;
            }

          /* This rule is no longer `in use' for recursive searches.  */
	  rule->in_use = 0;

          if (failed)
            {
              /* This pattern rule does not apply. If some of its
                 dependencies succeeded, free the data structure
                 describing them.  */
              free_idep_chain (deps);
              deps = 0;
            }
	  else
	    /* This pattern rule does apply.  Stop looking for one.  */
	    break;
	}

      /* If we found an applicable rule without
	 intermediate files, don't try with them.  */
      if (i < nrules)
	break;

      rule = 0;
    }

  /* RULE is nil if the loop went all the way
     through the list and everything failed.  */
  if (rule == 0)
    goto done;

  foundrule = i;

  /* If we are recursing, store the pattern that matched
     FILENAME in FILE->name for use in upper levels.  */

  if (recursions > 0)
    /* Kludge-o-matic */
    file->name = rule->targets[matches[foundrule]];

  /* FOUND_FILES lists the dependencies for the rule we found.
     This includes the intermediate files, if any.
     Convert them into entries on the deps-chain of FILE.  */

  if (remove_explicit_deps)
    {
      /* Remove all the dependencies that didn't come from
         this implicit rule. */

      dep = file->deps;
      while (dep != 0)
        {
          struct dep *next = dep->next;
          free_dep (dep);
          dep = next;
        }
      file->deps = 0;
  }

  expl_d = file->deps; /* We will add them at the end. */
  d_ptr = &file->deps;

  for (d = deps; d != 0; d = d->next)
    {
      register char *s;

      if (d->intermediate_file != 0)
	{
	  /* If we need to use an intermediate file,
	     make sure it is entered as a target, with the info that was
	     found for it in the recursive pattern_search call.
	     We know that the intermediate file did not already exist as
	     a target; therefore we can assume that the deps and cmds
	     of F below are null before we change them.  */

	  struct file *imf = d->intermediate_file;
	  register struct file *f = lookup_file (imf->name);

          /* We don't want to delete an intermediate file that happened
             to be a prerequisite of some (other) target. Mark it as
             precious.  */
          if (f != 0)
            f->precious = 1;
          else
            f = enter_file (imf->name);

	  f->deps = imf->deps;
	  f->cmds = imf->cmds;
	  f->stem = imf->stem;
          f->also_make = imf->also_make;
          f->is_target = 1;

          if (!f->precious)
            {
              imf = lookup_file (d->intermediate_pattern);
              if (imf != 0 && imf->precious)
                f->precious = 1;
            }

	  f->intermediate = 1;
	  f->tried_implicit = 1;
	  for (dep = f->deps; dep != 0; dep = dep->next)
	    {
	      dep->file = enter_file (dep->name);
              /* enter_file uses dep->name _if_ we created a new file.  */
              if (dep->name != dep->file->name)
                free (dep->name);
	      dep->name = 0;
	      dep->file->tried_implicit |= dep->changed;
	    }
	}

      dep = alloc_dep ();
      dep->ignore_mtime = d->ignore_mtime;
      s = d->name; /* Hijacking the name. */
      d->name = 0;
      if (recursions == 0)
	{
	  dep->file = lookup_file (s);
	  if (dep->file == 0)
	    /* enter_file consumes S's storage.  */
	    dep->file = enter_file (s);
	  else
	    /* A copy of S is already allocated in DEP->file->name.
	       So we can free S.  */
	    free (s);
	}
      else
	{
	  dep->name = s;
	}

      if (d->intermediate_file == 0 && tryrules[foundrule]->terminal)
	{
	  /* If the file actually existed (was not an intermediate file),
	     and the rule that found it was a terminal one, then we want
	     to mark the found file so that it will not have implicit rule
	     search done for it.  If we are not entering a `struct file' for
	     it now, we indicate this with the `changed' flag.  */
	  if (dep->file == 0)
	    dep->changed = 1;
	  else
	    dep->file->tried_implicit = 1;
	}

      *d_ptr = dep;
      d_ptr = &dep->next;
    }

  *d_ptr = expl_d;

  if (!checked_lastslash[foundrule])
    {
      /* Always allocate new storage, since STEM might be
         on the stack for an intermediate file.  */
      file->stem = savestring (stem, stemlen);
      fullstemlen = stemlen;
    }
  else
    {
      int dirlen = (lastslash + 1) - filename;

      /* We want to prepend the directory from
	 the original FILENAME onto the stem.  */
      fullstemlen = dirlen + stemlen;
      file->stem = (char *) xmalloc (fullstemlen + 1);
      bcopy (filename, file->stem, dirlen);
      bcopy (stem, file->stem + dirlen, stemlen);
      file->stem[fullstemlen] = '\0';
    }

  file->cmds = rule->cmds;
  file->is_target = 1;

  /* Set precious flag. */
  {
    struct file *f = lookup_file (rule->targets[matches[foundrule]]);
    if (f && f->precious)
      file->precious = 1;
  }

  /* If this rule builds other targets, too, put the others into FILE's
     `also_make' member.  */

  if (rule->targets[1] != 0)
    for (i = 0; rule->targets[i] != 0; ++i)
      if (i != matches[foundrule])
	{
	  struct file *f;
	  struct dep *new = alloc_dep ();

	  /* GKM FIMXE: handle '|' here too */
	  new->name = p = (char *) xmalloc (rule->lens[i] + fullstemlen + 1);
	  bcopy (rule->targets[i], p,
		 rule->suffixes[i] - rule->targets[i] - 1);
	  p += rule->suffixes[i] - rule->targets[i] - 1;
	  bcopy (file->stem, p, fullstemlen);
	  p += fullstemlen;
	  bcopy (rule->suffixes[i], p,
		 rule->lens[i] - (rule->suffixes[i] - rule->targets[i]) + 1);
	  new->file = enter_file (new->name);
	  new->next = file->also_make;

	  /* Set precious flag. */
	  f = lookup_file (rule->targets[i]);
	  if (f && f->precious)
            new->file->precious = 1;

          /* Set the is_target flag so that this file is not treated
             as intermediate by the pattern rule search algorithm and
             file_exists_p cannot pick it up yet.  */
          new->file->is_target = 1;

	  file->also_make = new;
	}

 done:
  free_idep_chain (deps);
  free (tryrules);

  return rule != 0;
}
