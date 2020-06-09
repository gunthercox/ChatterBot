/* Pattern and suffix rule internals for GNU Make.
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
#include "job.h"
#include "commands.h"
#include "variable.h"
#include "rule.h"

static void freerule PARAMS ((struct rule *rule, struct rule *lastrule));

/* Chain of all pattern rules.  */

struct rule *pattern_rules;

/* Pointer to last rule in the chain, so we can add onto the end.  */

struct rule *last_pattern_rule;

/* Number of rules in the chain.  */

unsigned int num_pattern_rules;

/* Maximum number of target patterns of any pattern rule.  */

unsigned int max_pattern_targets;

/* Maximum number of dependencies of any pattern rule.  */

unsigned int max_pattern_deps;

/* Maximum length of the name of a dependencies of any pattern rule.  */

unsigned int max_pattern_dep_length;

/* Pointer to structure for the file .SUFFIXES
   whose dependencies are the suffixes to be searched.  */

struct file *suffix_file;

/* Maximum length of a suffix.  */

unsigned int maxsuffix;

/* Compute the maximum dependency length and maximum number of
   dependencies of all implicit rules.  Also sets the subdir
   flag for a rule when appropriate, possibly removing the rule
   completely when appropriate.  */

void
count_implicit_rule_limits (void)
{
  char *name;
  int namelen;
  register struct rule *rule, *lastrule;

  num_pattern_rules = max_pattern_targets = max_pattern_deps = 0;
  max_pattern_dep_length = 0;

  name = 0;
  namelen = 0;
  rule = pattern_rules;
  lastrule = 0;
  while (rule != 0)
    {
      unsigned int ndeps = 0;
      register struct dep *dep;
      struct rule *next = rule->next;
      unsigned int ntargets;

      ++num_pattern_rules;

      ntargets = 0;
      while (rule->targets[ntargets] != 0)
	++ntargets;

      if (ntargets > max_pattern_targets)
	max_pattern_targets = ntargets;

      for (dep = rule->deps; dep != 0; dep = dep->next)
	{
	  unsigned int len = strlen (dep->name);

#ifdef VMS
	  char *p = strrchr (dep->name, ']');
          char *p2;
          if (p == 0)
            p = strrchr (dep->name, ':');
          p2 = p != 0 ? strchr (dep->name, '%') : 0;
#else
	  char *p = strrchr (dep->name, '/');
	  char *p2 = p != 0 ? strchr (dep->name, '%') : 0;
#endif
	  ndeps++;

	  if (len > max_pattern_dep_length)
	    max_pattern_dep_length = len;

	  if (p != 0 && p2 > p)
	    {
	      /* There is a slash before the % in the dep name.
		 Extract the directory name.  */
	      if (p == dep->name)
		++p;
	      if (p - dep->name > namelen)
		{
		  if (name != 0)
		    free (name);
		  namelen = p - dep->name;
		  name = (char *) xmalloc (namelen + 1);
		}
	      bcopy (dep->name, name, p - dep->name);
	      name[p - dep->name] = '\0';

	      /* In the deps of an implicit rule the `changed' flag
		 actually indicates that the dependency is in a
		 nonexistent subdirectory.  */

	      dep->changed = !dir_file_exists_p (name, "");
	    }
	  else
	    /* This dependency does not reside in a subdirectory.  */
	    dep->changed = 0;
	}

      if (ndeps > max_pattern_deps)
	max_pattern_deps = ndeps;

      lastrule = rule;
      rule = next;
    }

  if (name != 0)
    free (name);
}

/* Create a pattern rule from a suffix rule.
   TARGET is the target suffix; SOURCE is the source suffix.
   CMDS are the commands.
   If TARGET is nil, it means the target pattern should be `(%.o)'.
   If SOURCE is nil, it means there should be no deps.  */

static void
convert_suffix_rule (char *target, char *source, struct commands *cmds)
{
  char *targname, *targpercent, *depname;
  char **names, **percents;
  struct dep *deps;
  unsigned int len;

  if (target == 0)
    /* Special case: TARGET being nil means we are defining a
       `.X.a' suffix rule; the target pattern is always `(%.o)'.  */
    {
#ifdef VMS
      targname = savestring ("(%.obj)", 7);
#else
      targname = savestring ("(%.o)", 5);
#endif
      targpercent = targname + 1;
    }
  else
    {
      /* Construct the target name.  */
      len = strlen (target);
      targname = xmalloc (1 + len + 1);
      targname[0] = '%';
      bcopy (target, targname + 1, len + 1);
      targpercent = targname;
    }

  names = (char **) xmalloc (2 * sizeof (char *));
  percents = (char **) alloca (2 * sizeof (char *));
  names[0] = targname;
  percents[0] = targpercent;
  names[1] = percents[1] = 0;

  if (source == 0)
    deps = 0;
  else
    {
      /* Construct the dependency name.  */
      len = strlen (source);
      depname = xmalloc (1 + len + 1);
      depname[0] = '%';
      bcopy (source, depname + 1, len + 1);
      deps = alloc_dep ();
      deps->name = depname;
    }

  create_pattern_rule (names, percents, 0, deps, cmds, 0);
}

/* Convert old-style suffix rules to pattern rules.
   All rules for the suffixes on the .SUFFIXES list
   are converted and added to the chain of pattern rules.  */

void
convert_to_pattern (void)
{
  register struct dep *d, *d2;
  register struct file *f;
  register char *rulename;
  register unsigned int slen, s2len;

  /* Compute maximum length of all the suffixes.  */

  maxsuffix = 0;
  for (d = suffix_file->deps; d != 0; d = d->next)
    {
      register unsigned int namelen = strlen (dep_name (d));
      if (namelen > maxsuffix)
	maxsuffix = namelen;
    }

  rulename = (char *) alloca ((maxsuffix * 2) + 1);

  for (d = suffix_file->deps; d != 0; d = d->next)
    {
      /* Make a rule that is just the suffix, with no deps or commands.
	 This rule exists solely to disqualify match-anything rules.  */
      convert_suffix_rule (dep_name (d), (char *) 0, (struct commands *) 0);

      f = d->file;
      if (f->cmds != 0)
	/* Record a pattern for this suffix's null-suffix rule.  */
	convert_suffix_rule ("", dep_name (d), f->cmds);

      /* Record a pattern for each of this suffix's two-suffix rules.  */
      slen = strlen (dep_name (d));
      bcopy (dep_name (d), rulename, slen);
      for (d2 = suffix_file->deps; d2 != 0; d2 = d2->next)
	{
	  s2len = strlen (dep_name (d2));

	  if (slen == s2len && streq (dep_name (d), dep_name (d2)))
	    continue;

	  bcopy (dep_name (d2), rulename + slen, s2len + 1);
	  f = lookup_file (rulename);
	  if (f == 0 || f->cmds == 0)
	    continue;

	  if (s2len == 2 && rulename[slen] == '.' && rulename[slen + 1] == 'a')
	    /* A suffix rule `.X.a:' generates the pattern rule `(%.o): %.X'.
	       It also generates a normal `%.a: %.X' rule below.  */
	    convert_suffix_rule ((char *) 0, /* Indicates `(%.o)'.  */
				 dep_name (d),
				 f->cmds);

	  /* The suffix rule `.X.Y:' is converted
	     to the pattern rule `%.Y: %.X'.  */
	  convert_suffix_rule (dep_name (d2), dep_name (d), f->cmds);
	}
    }
}


/* Install the pattern rule RULE (whose fields have been filled in)
   at the end of the list (so that any rules previously defined
   will take precedence).  If this rule duplicates a previous one
   (identical target and dependencies), the old one is replaced
   if OVERRIDE is nonzero, otherwise this new one is thrown out.
   When an old rule is replaced, the new one is put at the end of the
   list.  Return nonzero if RULE is used; zero if not.  */

int
new_pattern_rule (struct rule *rule, int override)
{
  register struct rule *r, *lastrule;
  register unsigned int i, j;

  rule->in_use = 0;
  rule->terminal = 0;

  rule->next = 0;

  /* Search for an identical rule.  */
  lastrule = 0;
  for (r = pattern_rules; r != 0; lastrule = r, r = r->next)
    for (i = 0; rule->targets[i] != 0; ++i)
      {
	for (j = 0; r->targets[j] != 0; ++j)
	  if (!streq (rule->targets[i], r->targets[j]))
	    break;
	if (r->targets[j] == 0)
	  /* All the targets matched.  */
	  {
	    register struct dep *d, *d2;
	    for (d = rule->deps, d2 = r->deps;
		 d != 0 && d2 != 0; d = d->next, d2 = d2->next)
	      if (!streq (dep_name (d), dep_name (d2)))
		break;
	    if (d == 0 && d2 == 0)
	      {
		/* All the dependencies matched.  */
		if (override)
		  {
		    /* Remove the old rule.  */
		    freerule (r, lastrule);
		    /* Install the new one.  */
		    if (pattern_rules == 0)
		      pattern_rules = rule;
		    else
		      last_pattern_rule->next = rule;
		    last_pattern_rule = rule;

		    /* We got one.  Stop looking.  */
		    goto matched;
		  }
		else
		  {
		    /* The old rule stays intact.  Destroy the new one.  */
		    freerule (rule, (struct rule *) 0);
		    return 0;
		  }
	      }
	  }
      }

 matched:;

  if (r == 0)
    {
      /* There was no rule to replace.  */
      if (pattern_rules == 0)
	pattern_rules = rule;
      else
	last_pattern_rule->next = rule;
      last_pattern_rule = rule;
    }

  return 1;
}


/* Install an implicit pattern rule based on the three text strings
   in the structure P points to.  These strings come from one of
   the arrays of default implicit pattern rules.
   TERMINAL specifies what the `terminal' field of the rule should be.  */

void
install_pattern_rule (struct pspec *p, int terminal)
{
  register struct rule *r;
  char *ptr;

  r = (struct rule *) xmalloc (sizeof (struct rule));

  r->targets = (char **) xmalloc (2 * sizeof (char *));
  r->suffixes = (char **) xmalloc (2 * sizeof (char *));
  r->lens = (unsigned int *) xmalloc (2 * sizeof (unsigned int));

  r->targets[1] = 0;
  r->suffixes[1] = 0;
  r->lens[1] = 0;

  r->lens[0] = strlen (p->target);
  /* These will all be string literals, but we malloc space for
     them anyway because somebody might want to free them later on.  */
  r->targets[0] = savestring (p->target, r->lens[0]);
  r->suffixes[0] = find_percent (r->targets[0]);
  if (r->suffixes[0] == 0)
    /* Programmer-out-to-lunch error.  */
    abort ();
  else
    ++r->suffixes[0];

  ptr = p->dep;
  r->deps = (struct dep *) multi_glob (parse_file_seq (&ptr, '\0',
                                                       sizeof (struct dep), 1),
				       sizeof (struct dep));

  if (new_pattern_rule (r, 0))
    {
      r->terminal = terminal;
      r->cmds = (struct commands *) xmalloc (sizeof (struct commands));
      r->cmds->fileinfo.filenm = 0;
      r->cmds->fileinfo.lineno = 0;
      /* These will all be string literals, but we malloc space for them
	 anyway because somebody might want to free them later.  */
      r->cmds->commands = xstrdup (p->commands);
      r->cmds->command_lines = 0;
    }
}


/* Free all the storage used in RULE and take it out of the
   pattern_rules chain.  LASTRULE is the rule whose next pointer
   points to RULE.  */

static void
freerule (struct rule *rule, struct rule *lastrule)
{
  struct rule *next = rule->next;
  register unsigned int i;
  register struct dep *dep;

  for (i = 0; rule->targets[i] != 0; ++i)
    free (rule->targets[i]);

  dep = rule->deps;
  while (dep)
    {
      struct dep *t;

      t = dep->next;
      /* We might leak dep->name here, but I'm not sure how to fix this: I
         think that pointer might be shared (e.g., in the file hash?)  */
      dep->name = 0; /* Make sure free_dep does not free name.  */
      free_dep (dep);
      dep = t;
    }

  free ((char *) rule->targets);
  free ((char *) rule->suffixes);
  free ((char *) rule->lens);

  /* We can't free the storage for the commands because there
     are ways that they could be in more than one place:
       * If the commands came from a suffix rule, they could also be in
       the `struct file's for other suffix rules or plain targets given
       on the same makefile line.
       * If two suffixes that together make a two-suffix rule were each
       given twice in the .SUFFIXES list, and in the proper order, two
       identical pattern rules would be created and the second one would
       be discarded here, but both would contain the same `struct commands'
       pointer from the `struct file' for the suffix rule.  */

  free ((char *) rule);

  if (pattern_rules == rule)
    if (lastrule != 0)
      abort ();
    else
      pattern_rules = next;
  else if (lastrule != 0)
    lastrule->next = next;
  if (last_pattern_rule == rule)
    last_pattern_rule = lastrule;
}

/* Create a new pattern rule with the targets in the nil-terminated
   array TARGETS.  If TARGET_PERCENTS is not nil, it is an array of
   pointers into the elements of TARGETS, where the `%'s are.
   The new rule has dependencies DEPS and commands from COMMANDS.
   It is a terminal rule if TERMINAL is nonzero.  This rule overrides
   identical rules with different commands if OVERRIDE is nonzero.

   The storage for TARGETS and its elements is used and must not be freed
   until the rule is destroyed.  The storage for TARGET_PERCENTS is not used;
   it may be freed.  */

void
create_pattern_rule (char **targets, char **target_percents,
		     int terminal, struct dep *deps,
                     struct commands *commands, int override)
{
  unsigned int max_targets, i;
  struct rule *r = (struct rule *) xmalloc (sizeof (struct rule));

  r->cmds = commands;
  r->deps = deps;
  r->targets = targets;

  max_targets = 2;
  r->lens = (unsigned int *) xmalloc (2 * sizeof (unsigned int));
  r->suffixes = (char **) xmalloc (2 * sizeof (char *));
  for (i = 0; targets[i] != 0; ++i)
    {
      if (i == max_targets - 1)
	{
	  max_targets += 5;
	  r->lens = (unsigned int *)
	    xrealloc ((char *) r->lens, max_targets * sizeof (unsigned int));
	  r->suffixes = (char **)
	    xrealloc ((char *) r->suffixes, max_targets * sizeof (char *));
	}
      r->lens[i] = strlen (targets[i]);
      r->suffixes[i] = (target_percents == 0 ? find_percent (targets[i])
			: target_percents[i]) + 1;
      if (r->suffixes[i] == 0)
	abort ();
    }

  if (i < max_targets - 1)
    {
      r->lens = (unsigned int *) xrealloc ((char *) r->lens,
					   (i + 1) * sizeof (unsigned int));
      r->suffixes = (char **) xrealloc ((char *) r->suffixes,
					(i + 1) * sizeof (char *));
    }

  if (new_pattern_rule (r, override))
    r->terminal = terminal;
}

/* Print the data base of rules.  */

static void			/* Useful to call from gdb.  */
print_rule (struct rule *r)
{
  register unsigned int i;
  register struct dep *d;

  for (i = 0; r->targets[i] != 0; ++i)
    {
      fputs (r->targets[i], stdout);
      if (r->targets[i + 1] != 0)
	putchar (' ');
      else
	putchar (':');
    }
  if (r->terminal)
    putchar (':');

  for (d = r->deps; d != 0; d = d->next)
    printf (" %s", dep_name (d));
  putchar ('\n');

  if (r->cmds != 0)
    print_commands (r->cmds);
}

void
print_rule_data_base (void)
{
  register unsigned int rules, terminal;
  register struct rule *r;

  puts (_("\n# Implicit Rules"));

  rules = terminal = 0;
  for (r = pattern_rules; r != 0; r = r->next)
    {
      ++rules;

      putchar ('\n');
      print_rule (r);

      if (r->terminal)
	++terminal;
    }

  if (rules == 0)
    puts (_("\n# No implicit rules."));
  else
    {
      printf (_("\n# %u implicit rules, %u"), rules, terminal);
#ifndef	NO_FLOAT
      printf (" (%.1f%%)", (double) terminal / (double) rules * 100.0);
#else
      {
	int f = (terminal * 1000 + 5) / rules;
	printf (" (%d.%d%%)", f/10, f%10);
      }
#endif
      puts (_(" terminal."));
    }

  if (num_pattern_rules != rules)
    {
      /* This can happen if a fatal error was detected while reading the
         makefiles and thus count_implicit_rule_limits wasn't called yet.  */
      if (num_pattern_rules != 0)
        fatal (NILF, _("BUG: num_pattern_rules wrong!  %u != %u"),
               num_pattern_rules, rules);
    }
}
