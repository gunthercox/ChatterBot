/* Builtin function expansion for GNU Make.
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
#include "variable.h"
#include "dep.h"
#include "job.h"
#include "commands.h"
#include "debug.h"

#ifdef _AMIGA
#include "amiga.h"
#endif


struct function_table_entry
  {
    const char *name;
    unsigned char len;
    unsigned char minimum_args;
    unsigned char maximum_args;
    char expand_args;
    char *(*func_ptr) PARAMS ((char *output, char **argv, const char *fname));
  };

static unsigned long
function_table_entry_hash_1 (const void *keyv)
{
  struct function_table_entry const *key = (struct function_table_entry const *) keyv;
  return_STRING_N_HASH_1 (key->name, key->len);
}

static unsigned long
function_table_entry_hash_2 (const void *keyv)
{
  struct function_table_entry const *key = (struct function_table_entry const *) keyv;
  return_STRING_N_HASH_2 (key->name, key->len);
}

static int
function_table_entry_hash_cmp (const void *xv, const void *yv)
{
  struct function_table_entry const *x = (struct function_table_entry const *) xv;
  struct function_table_entry const *y = (struct function_table_entry const *) yv;
  int result = x->len - y->len;
  if (result)
    return result;
  return_STRING_N_COMPARE (x->name, y->name, x->len);
}

static struct hash_table function_table;


/* Store into VARIABLE_BUFFER at O the result of scanning TEXT and replacing
   each occurrence of SUBST with REPLACE. TEXT is null-terminated.  SLEN is
   the length of SUBST and RLEN is the length of REPLACE.  If BY_WORD is
   nonzero, substitutions are done only on matches which are complete
   whitespace-delimited words.  */

char *
subst_expand (char *o, char *text, char *subst, char *replace,
              unsigned int slen, unsigned int rlen, int by_word)
{
  char *t = text;
  char *p;

  if (slen == 0 && !by_word)
    {
      /* The first occurrence of "" in any string is its end.  */
      o = variable_buffer_output (o, t, strlen (t));
      if (rlen > 0)
	o = variable_buffer_output (o, replace, rlen);
      return o;
    }

  do
    {
      if (by_word && slen == 0)
	/* When matching by words, the empty string should match
	   the end of each word, rather than the end of the whole text.  */
	p = end_of_token (next_token (t));
      else
	{
	  p = strstr (t, subst);
	  if (p == 0)
	    {
	      /* No more matches.  Output everything left on the end.  */
	      o = variable_buffer_output (o, t, strlen (t));
	      return o;
	    }
	}

      /* Output everything before this occurrence of the string to replace.  */
      if (p > t)
	o = variable_buffer_output (o, t, p - t);

      /* If we're substituting only by fully matched words,
	 or only at the ends of words, check that this case qualifies.  */
      if (by_word
          && ((p > text && !isblank ((unsigned char)p[-1]))
              || (p[slen] != '\0' && !isblank ((unsigned char)p[slen]))))
	/* Struck out.  Output the rest of the string that is
	   no longer to be replaced.  */
	o = variable_buffer_output (o, subst, slen);
      else if (rlen > 0)
	/* Output the replacement string.  */
	o = variable_buffer_output (o, replace, rlen);

      /* Advance T past the string to be replaced.  */
      {
        char *nt = p + slen;
        t = nt;
      }
    } while (*t != '\0');

  return o;
}


/* Store into VARIABLE_BUFFER at O the result of scanning TEXT
   and replacing strings matching PATTERN with REPLACE.
   If PATTERN_PERCENT is not nil, PATTERN has already been
   run through find_percent, and PATTERN_PERCENT is the result.
   If REPLACE_PERCENT is not nil, REPLACE has already been
   run through find_percent, and REPLACE_PERCENT is the result.
   Note that we expect PATTERN_PERCENT and REPLACE_PERCENT to point to the
   character _AFTER_ the %, not to the % itself.
*/

char *
patsubst_expand (char *o, char *text, char *pattern, char *replace,
                 char *pattern_percent, char *replace_percent)
{
  unsigned int pattern_prepercent_len, pattern_postpercent_len;
  unsigned int replace_prepercent_len, replace_postpercent_len;
  char *t;
  unsigned int len;
  int doneany = 0;

  /* We call find_percent on REPLACE before checking PATTERN so that REPLACE
     will be collapsed before we call subst_expand if PATTERN has no %.  */
  if (!replace_percent)
    {
      replace_percent = find_percent (replace);
      if (replace_percent)
        ++replace_percent;
    }

  /* Record the length of REPLACE before and after the % so we don't have to
     compute these lengths more than once.  */
  if (replace_percent)
    {
      replace_prepercent_len = replace_percent - replace - 1;
      replace_postpercent_len = strlen (replace_percent);
    }
  else
    {
      replace_prepercent_len = strlen (replace);
      replace_postpercent_len = 0;
    }

  if (!pattern_percent)
    {
      pattern_percent = find_percent (pattern);
      if (pattern_percent)
        ++pattern_percent;
    }
  if (!pattern_percent)
    /* With no % in the pattern, this is just a simple substitution.  */
    return subst_expand (o, text, pattern, replace,
			 strlen (pattern), strlen (replace), 1);

  /* Record the length of PATTERN before and after the %
     so we don't have to compute it more than once.  */
  pattern_prepercent_len = pattern_percent - pattern - 1;
  pattern_postpercent_len = strlen (pattern_percent);

  while ((t = find_next_token (&text, &len)) != 0)
    {
      int fail = 0;

      /* Is it big enough to match?  */
      if (len < pattern_prepercent_len + pattern_postpercent_len)
	fail = 1;

      /* Does the prefix match? */
      if (!fail && pattern_prepercent_len > 0
	  && (*t != *pattern
	      || t[pattern_prepercent_len - 1] != pattern_percent[-2]
	      || !strneq (t + 1, pattern + 1, pattern_prepercent_len - 1)))
	fail = 1;

      /* Does the suffix match? */
      if (!fail && pattern_postpercent_len > 0
	  && (t[len - 1] != pattern_percent[pattern_postpercent_len - 1]
	      || t[len - pattern_postpercent_len] != *pattern_percent
	      || !strneq (&t[len - pattern_postpercent_len],
			  pattern_percent, pattern_postpercent_len - 1)))
	fail = 1;

      if (fail)
	/* It didn't match.  Output the string.  */
	o = variable_buffer_output (o, t, len);
      else
	{
	  /* It matched.  Output the replacement.  */

	  /* Output the part of the replacement before the %.  */
	  o = variable_buffer_output (o, replace, replace_prepercent_len);

	  if (replace_percent != 0)
	    {
	      /* Output the part of the matched string that
		 matched the % in the pattern.  */
	      o = variable_buffer_output (o, t + pattern_prepercent_len,
					  len - (pattern_prepercent_len
						 + pattern_postpercent_len));
	      /* Output the part of the replacement after the %.  */
	      o = variable_buffer_output (o, replace_percent,
					  replace_postpercent_len);
	    }
	}

      /* Output a space, but not if the replacement is "".  */
      if (fail || replace_prepercent_len > 0
	  || (replace_percent != 0 && len + replace_postpercent_len > 0))
	{
	  o = variable_buffer_output (o, " ", 1);
	  doneany = 1;
	}
    }
  if (doneany)
    /* Kill the last space.  */
    --o;

  return o;
}


/* Look up a function by name.  */

static const struct function_table_entry *
lookup_function (const char *s)
{
  const char *e = s;

  while (*e && ( (*e >= 'a' && *e <= 'z') || *e == '-'))
    e++;
  if (*e == '\0' || isblank ((unsigned char) *e))
    {
      struct function_table_entry function_table_entry_key;
      function_table_entry_key.name = s;
      function_table_entry_key.len = e - s;

      return hash_find_item (&function_table, &function_table_entry_key);
    }
  return 0;
}


/* Return 1 if PATTERN matches STR, 0 if not.  */

int
pattern_matches (char *pattern, char *percent, char *str)
{
  unsigned int sfxlen, strlength;

  if (percent == 0)
    {
      unsigned int len = strlen (pattern) + 1;
      char *new_chars = (char *) alloca (len);
      bcopy (pattern, new_chars, len);
      pattern = new_chars;
      percent = find_percent (pattern);
      if (percent == 0)
	return streq (pattern, str);
    }

  sfxlen = strlen (percent + 1);
  strlength = strlen (str);

  if (strlength < (percent - pattern) + sfxlen
      || !strneq (pattern, str, percent - pattern))
    return 0;

  return !strcmp (percent + 1, str + (strlength - sfxlen));
}


/* Find the next comma or ENDPAREN (counting nested STARTPAREN and
   ENDPARENtheses), starting at PTR before END.  Return a pointer to
   next character.

   If no next argument is found, return NULL.
*/

static char *
find_next_argument (char startparen, char endparen,
                    const char *ptr, const char *end)
{
  int count = 0;

  for (; ptr < end; ++ptr)
    if (*ptr == startparen)
      ++count;

    else if (*ptr == endparen)
      {
	--count;
	if (count < 0)
	  return NULL;
      }

    else if (*ptr == ',' && !count)
      return (char *)ptr;

  /* We didn't find anything.  */
  return NULL;
}


/* Glob-expand LINE.  The returned pointer is
   only good until the next call to string_glob.  */

static char *
string_glob (char *line)
{
  static char *result = 0;
  static unsigned int length;
  register struct nameseq *chain;
  register unsigned int idx;

  chain = multi_glob (parse_file_seq
		      (&line, '\0', sizeof (struct nameseq),
		       /* We do not want parse_file_seq to strip `./'s.
			  That would break examples like:
			  $(patsubst ./%.c,obj/%.o,$(wildcard ./?*.c)).  */
		       0),
		      sizeof (struct nameseq));

  if (result == 0)
    {
      length = 100;
      result = (char *) xmalloc (100);
    }

  idx = 0;
  while (chain != 0)
    {
      register char *name = chain->name;
      unsigned int len = strlen (name);

      struct nameseq *next = chain->next;
      free ((char *) chain);
      chain = next;

      /* multi_glob will pass names without globbing metacharacters
	 through as is, but we want only files that actually exist.  */
      if (file_exists_p (name))
	{
	  if (idx + len + 1 > length)
	    {
	      length += (len + 1) * 2;
	      result = (char *) xrealloc (result, length);
	    }
	  bcopy (name, &result[idx], len);
	  idx += len;
	  result[idx++] = ' ';
	}

      free (name);
    }

  /* Kill the last space and terminate the string.  */
  if (idx == 0)
    result[0] = '\0';
  else
    result[idx - 1] = '\0';

  return result;
}

/*
  Builtin functions
 */

static char *
func_patsubst (char *o, char **argv, const char *funcname UNUSED)
{
  o = patsubst_expand (o, argv[2], argv[0], argv[1], (char *) 0, (char *) 0);
  return o;
}


static char *
func_join (char *o, char **argv, const char *funcname UNUSED)
{
  int doneany = 0;

  /* Write each word of the first argument directly followed
     by the corresponding word of the second argument.
     If the two arguments have a different number of words,
     the excess words are just output separated by blanks.  */
  register char *tp;
  register char *pp;
  char *list1_iterator = argv[0];
  char *list2_iterator = argv[1];
  do
    {
      unsigned int len1, len2;

      tp = find_next_token (&list1_iterator, &len1);
      if (tp != 0)
	o = variable_buffer_output (o, tp, len1);

      pp = find_next_token (&list2_iterator, &len2);
      if (pp != 0)
	o = variable_buffer_output (o, pp, len2);

      if (tp != 0 || pp != 0)
	{
	  o = variable_buffer_output (o, " ", 1);
	  doneany = 1;
	}
    }
  while (tp != 0 || pp != 0);
  if (doneany)
    /* Kill the last blank.  */
    --o;

  return o;
}


static char *
func_origin (char *o, char **argv, const char *funcname UNUSED)
{
  /* Expand the argument.  */
  register struct variable *v = lookup_variable (argv[0], strlen (argv[0]));
  if (v == 0)
    o = variable_buffer_output (o, "undefined", 9);
  else
    switch (v->origin)
      {
      default:
      case o_invalid:
	abort ();
	break;
      case o_default:
	o = variable_buffer_output (o, "default", 7);
	break;
      case o_env:
	o = variable_buffer_output (o, "environment", 11);
	break;
      case o_file:
	o = variable_buffer_output (o, "file", 4);
	break;
      case o_env_override:
	o = variable_buffer_output (o, "environment override", 20);
	break;
      case o_command:
	o = variable_buffer_output (o, "command line", 12);
	break;
      case o_override:
	o = variable_buffer_output (o, "override", 8);
	break;
      case o_automatic:
	o = variable_buffer_output (o, "automatic", 9);
	break;
      }

  return o;
}

static char *
func_flavor (char *o, char **argv, const char *funcname UNUSED)
{
  register struct variable *v = lookup_variable (argv[0], strlen (argv[0]));

  if (v == 0)
    o = variable_buffer_output (o, "undefined", 9);
  else
    if (v->recursive)
      o = variable_buffer_output (o, "recursive", 9);
    else
      o = variable_buffer_output (o, "simple", 6);

  return o;
}

#ifdef VMS
# define IS_PATHSEP(c) ((c) == ']')
#else
# ifdef HAVE_DOS_PATHS
#  define IS_PATHSEP(c) ((c) == '/' || (c) == '\\')
# else
#  define IS_PATHSEP(c) ((c) == '/')
# endif
#endif


static char *
func_notdir_suffix (char *o, char **argv, const char *funcname)
{
  /* Expand the argument.  */
  char *list_iterator = argv[0];
  char *p2 =0;
  int doneany =0;
  unsigned int len=0;

  int is_suffix = streq (funcname, "suffix");
  int is_notdir = !is_suffix;
  while ((p2 = find_next_token (&list_iterator, &len)) != 0)
    {
      char *p = p2 + len;


      while (p >= p2 && (!is_suffix || *p != '.'))
	{
	  if (IS_PATHSEP (*p))
	    break;
	  --p;
	}

      if (p >= p2)
	{
	  if (is_notdir)
	    ++p;
	  else if (*p != '.')
	    continue;
	  o = variable_buffer_output (o, p, len - (p - p2));
	}
#ifdef HAVE_DOS_PATHS
      /* Handle the case of "d:foo/bar".  */
      else if (streq (funcname, "notdir") && p2[0] && p2[1] == ':')
	{
	  p = p2 + 2;
	  o = variable_buffer_output (o, p, len - (p - p2));
	}
#endif
      else if (is_notdir)
	o = variable_buffer_output (o, p2, len);

      if (is_notdir || p >= p2)
	{
	  o = variable_buffer_output (o, " ", 1);
	  doneany = 1;
	}
    }
  if (doneany)
    /* Kill last space.  */
    --o;


  return o;

}


static char *
func_basename_dir (char *o, char **argv, const char *funcname)
{
  /* Expand the argument.  */
  char *p3 = argv[0];
  char *p2=0;
  int doneany=0;
  unsigned int len=0;
  char *p=0;
  int is_basename= streq (funcname, "basename");
  int is_dir= !is_basename;

  while ((p2 = find_next_token (&p3, &len)) != 0)
	{
	  p = p2 + len;
	  while (p >= p2 && (!is_basename  || *p != '.'))
	    {
	      if (IS_PATHSEP (*p))
		break;
	      	    --p;
	    }

	  if (p >= p2 && (is_dir))
	    o = variable_buffer_output (o, p2, ++p - p2);
	  else if (p >= p2 && (*p == '.'))
	    o = variable_buffer_output (o, p2, p - p2);
#ifdef HAVE_DOS_PATHS
	/* Handle the "d:foobar" case */
	  else if (p2[0] && p2[1] == ':' && is_dir)
	    o = variable_buffer_output (o, p2, 2);
#endif
	  else if (is_dir)
#ifdef VMS
	    o = variable_buffer_output (o, "[]", 2);
#else
#ifndef _AMIGA
	    o = variable_buffer_output (o, "./", 2);
#else
	    ; /* Just a nop...  */
#endif /* AMIGA */
#endif /* !VMS */
	  else
	    /* The entire name is the basename.  */
	    o = variable_buffer_output (o, p2, len);

	  o = variable_buffer_output (o, " ", 1);
	  doneany = 1;
	}
      if (doneany)
	/* Kill last space.  */
	--o;


 return o;
}

static char *
func_addsuffix_addprefix (char *o, char **argv, const char *funcname)
{
  int fixlen = strlen (argv[0]);
  char *list_iterator = argv[1];
  int is_addprefix = streq (funcname, "addprefix");
  int is_addsuffix = !is_addprefix;

  int doneany = 0;
  char *p;
  unsigned int len;

  while ((p = find_next_token (&list_iterator, &len)) != 0)
    {
      if (is_addprefix)
	o = variable_buffer_output (o, argv[0], fixlen);
      o = variable_buffer_output (o, p, len);
      if (is_addsuffix)
	o = variable_buffer_output (o, argv[0], fixlen);
      o = variable_buffer_output (o, " ", 1);
      doneany = 1;
    }

  if (doneany)
    /* Kill last space.  */
    --o;

  return o;
}

static char *
func_subst (char *o, char **argv, const char *funcname UNUSED)
{
  o = subst_expand (o, argv[2], argv[0], argv[1], strlen (argv[0]),
		    strlen (argv[1]), 0);

  return o;
}


static char *
func_firstword (char *o, char **argv, const char *funcname UNUSED)
{
  unsigned int i;
  char *words = argv[0];    /* Use a temp variable for find_next_token */
  char *p = find_next_token (&words, &i);

  if (p != 0)
    o = variable_buffer_output (o, p, i);

  return o;
}

static char *
func_lastword (char *o, char **argv, const char *funcname UNUSED)
{
  unsigned int i;
  char *words = argv[0];    /* Use a temp variable for find_next_token */
  char *p = 0;
  char *t;

  while ((t = find_next_token (&words, &i)))
    p = t;

  if (p != 0)
    o = variable_buffer_output (o, p, i);

  return o;
}

static char *
func_words (char *o, char **argv, const char *funcname UNUSED)
{
  int i = 0;
  char *word_iterator = argv[0];
  char buf[20];

  while (find_next_token (&word_iterator, (unsigned int *) 0) != 0)
    ++i;

  sprintf (buf, "%d", i);
  o = variable_buffer_output (o, buf, strlen (buf));


  return o;
}

/* Set begpp to point to the first non-whitespace character of the string,
 * and endpp to point to the last non-whitespace character of the string.
 * If the string is empty or contains nothing but whitespace, endpp will be
 * begpp-1.
 */
char *
strip_whitespace (const char **begpp, const char **endpp)
{
  while (*begpp <= *endpp && isspace ((unsigned char)**begpp))
    (*begpp) ++;
  while (*endpp >= *begpp && isspace ((unsigned char)**endpp))
    (*endpp) --;
  return (char *)*begpp;
}

static void
check_numeric (const char *s, const char *message)
{
  const char *end = s + strlen (s) - 1;
  const char *beg = s;
  strip_whitespace (&s, &end);

  for (; s <= end; ++s)
    if (!ISDIGIT (*s))  /* ISDIGIT only evals its arg once: see make.h.  */
      break;

  if (s <= end || end - beg < 0)
    fatal (*expanding_var, "%s: '%s'", message, beg);
}



static char *
func_word (char *o, char **argv, const char *funcname UNUSED)
{
  char *end_p=0;
  int i=0;
  char *p=0;

  /* Check the first argument.  */
  check_numeric (argv[0], _("non-numeric first argument to `word' function"));
  i =  atoi (argv[0]);

  if (i == 0)
    fatal (*expanding_var,
           _("first argument to `word' function must be greater than 0"));


  end_p = argv[1];
  while ((p = find_next_token (&end_p, 0)) != 0)
    if (--i == 0)
      break;

  if (i == 0)
    o = variable_buffer_output (o, p, end_p - p);

  return o;
}

static char *
func_wordlist (char *o, char **argv, const char *funcname UNUSED)
{
  int start, count;

  /* Check the arguments.  */
  check_numeric (argv[0],
		 _("non-numeric first argument to `wordlist' function"));
  check_numeric (argv[1],
		 _("non-numeric second argument to `wordlist' function"));

  start = atoi (argv[0]);
  if (start < 1)
    fatal (*expanding_var,
           "invalid first argument to `wordlist' function: `%d'", start);

  count = atoi (argv[1]) - start + 1;

  if (count > 0)
    {
      char *p;
      char *end_p = argv[2];

      /* Find the beginning of the "start"th word.  */
      while (((p = find_next_token (&end_p, 0)) != 0) && --start)
        ;

      if (p)
        {
          /* Find the end of the "count"th word from start.  */
          while (--count && (find_next_token (&end_p, 0) != 0))
            ;

          /* Return the stuff in the middle.  */
          o = variable_buffer_output (o, p, end_p - p);
        }
    }

  return o;
}

static char*
func_findstring (char *o, char **argv, const char *funcname UNUSED)
{
  /* Find the first occurrence of the first string in the second.  */
  if (strstr (argv[1], argv[0]) != 0)
    o = variable_buffer_output (o, argv[0], strlen (argv[0]));

  return o;
}

static char *
func_foreach (char *o, char **argv, const char *funcname UNUSED)
{
  /* expand only the first two.  */
  char *varname = expand_argument (argv[0], NULL);
  char *list = expand_argument (argv[1], NULL);
  char *body = argv[2];

  int doneany = 0;
  char *list_iterator = list;
  char *p;
  unsigned int len;
  register struct variable *var;

  push_new_variable_scope ();
  var = define_variable (varname, strlen (varname), "", o_automatic, 0);

  /* loop through LIST,  put the value in VAR and expand BODY */
  while ((p = find_next_token (&list_iterator, &len)) != 0)
    {
      char *result = 0;

      {
	char save = p[len];

	p[len] = '\0';
	free (var->value);
	var->value = (char *) xstrdup ((char*) p);
	p[len] = save;
      }

      result = allocated_variable_expand (body);

      o = variable_buffer_output (o, result, strlen (result));
      o = variable_buffer_output (o, " ", 1);
      doneany = 1;
      free (result);
    }

  if (doneany)
    /* Kill the last space.  */
    --o;

  pop_variable_scope ();
  free (varname);
  free (list);

  return o;
}

struct a_word
{
  struct a_word *next;
  struct a_word *chain;
  char *str;
  int length;
  int matched;
};

static unsigned long
a_word_hash_1 (const void *key)
{
  return_STRING_HASH_1 (((struct a_word const *) key)->str);
}

static unsigned long
a_word_hash_2 (const void *key)
{
  return_STRING_HASH_2 (((struct a_word const *) key)->str);
}

static int
a_word_hash_cmp (const void *x, const void *y)
{
  int result = ((struct a_word const *) x)->length - ((struct a_word const *) y)->length;
  if (result)
    return result;
  return_STRING_COMPARE (((struct a_word const *) x)->str,
			 ((struct a_word const *) y)->str);
}

struct a_pattern
{
  struct a_pattern *next;
  char *str;
  char *percent;
  int length;
  int save_c;
};

static char *
func_filter_filterout (char *o, char **argv, const char *funcname)
{
  struct a_word *wordhead;
  struct a_word **wordtail;
  struct a_word *wp;
  struct a_pattern *pathead;
  struct a_pattern **pattail;
  struct a_pattern *pp;

  struct hash_table a_word_table;
  int is_filter = streq (funcname, "filter");
  char *pat_iterator = argv[0];
  char *word_iterator = argv[1];
  int literals = 0;
  int words = 0;
  int hashing = 0;
  char *p;
  unsigned int len;

  /* Chop ARGV[0] up into patterns to match against the words.  */

  pattail = &pathead;
  while ((p = find_next_token (&pat_iterator, &len)) != 0)
    {
      struct a_pattern *pat = (struct a_pattern *) alloca (sizeof (struct a_pattern));

      *pattail = pat;
      pattail = &pat->next;

      if (*pat_iterator != '\0')
	++pat_iterator;

      pat->str = p;
      pat->length = len;
      pat->save_c = p[len];
      p[len] = '\0';
      pat->percent = find_percent (p);
      if (pat->percent == 0)
	literals++;
    }
  *pattail = 0;

  /* Chop ARGV[1] up into words to match against the patterns.  */

  wordtail = &wordhead;
  while ((p = find_next_token (&word_iterator, &len)) != 0)
    {
      struct a_word *word = (struct a_word *) alloca (sizeof (struct a_word));

      *wordtail = word;
      wordtail = &word->next;

      if (*word_iterator != '\0')
	++word_iterator;

      p[len] = '\0';
      word->str = p;
      word->length = len;
      word->matched = 0;
      word->chain = 0;
      words++;
    }
  *wordtail = 0;

  /* Only use a hash table if arg list lengths justifies the cost.  */
  hashing = (literals >= 2 && (literals * words) >= 10);
  if (hashing)
    {
      hash_init (&a_word_table, words, a_word_hash_1, a_word_hash_2, a_word_hash_cmp);
      for (wp = wordhead; wp != 0; wp = wp->next)
	{
	  struct a_word *owp = hash_insert (&a_word_table, wp);
	  if (owp)
	    wp->chain = owp;
	}
    }

  if (words)
    {
      int doneany = 0;

      /* Run each pattern through the words, killing words.  */
      for (pp = pathead; pp != 0; pp = pp->next)
	{
	  if (pp->percent)
	    for (wp = wordhead; wp != 0; wp = wp->next)
	      wp->matched |= pattern_matches (pp->str, pp->percent, wp->str);
	  else if (hashing)
	    {
	      struct a_word a_word_key;
	      a_word_key.str = pp->str;
	      a_word_key.length = pp->length;
	      wp = (struct a_word *) hash_find_item (&a_word_table, &a_word_key);
	      while (wp)
		{
		  wp->matched |= 1;
		  wp = wp->chain;
		}
	    }
	  else
	    for (wp = wordhead; wp != 0; wp = wp->next)
	      wp->matched |= (wp->length == pp->length
			      && strneq (pp->str, wp->str, wp->length));
	}

      /* Output the words that matched (or didn't, for filter-out).  */
      for (wp = wordhead; wp != 0; wp = wp->next)
	if (is_filter ? wp->matched : !wp->matched)
	  {
	    o = variable_buffer_output (o, wp->str, strlen (wp->str));
	    o = variable_buffer_output (o, " ", 1);
	    doneany = 1;
	  }

      if (doneany)
	/* Kill the last space.  */
	--o;
    }

  for (pp = pathead; pp != 0; pp = pp->next)
    pp->str[pp->length] = pp->save_c;

  if (hashing)
    hash_free (&a_word_table, 0);

  return o;
}


static char *
func_strip (char *o, char **argv, const char *funcname UNUSED)
{
  char *p = argv[0];
  int doneany =0;

  while (*p != '\0')
    {
      int i=0;
      char *word_start=0;

      while (isspace ((unsigned char)*p))
	++p;
      word_start = p;
      for (i=0; *p != '\0' && !isspace ((unsigned char)*p); ++p, ++i)
	{}
      if (!i)
	break;
      o = variable_buffer_output (o, word_start, i);
      o = variable_buffer_output (o, " ", 1);
      doneany = 1;
    }

  if (doneany)
    /* Kill the last space.  */
    --o;
  return o;
}

/*
  Print a warning or fatal message.
*/
static char *
func_error (char *o, char **argv, const char *funcname)
{
  char **argvp;
  char *msg, *p;
  int len;

  /* The arguments will be broken on commas.  Rather than create yet
     another special case where function arguments aren't broken up,
     just create a format string that puts them back together.  */
  for (len=0, argvp=argv; *argvp != 0; ++argvp)
    len += strlen (*argvp) + 2;

  p = msg = (char *) alloca (len + 1);

  for (argvp=argv; argvp[1] != 0; ++argvp)
    {
      strcpy (p, *argvp);
      p += strlen (*argvp);
      *(p++) = ',';
      *(p++) = ' ';
    }
  strcpy (p, *argvp);

  switch (*funcname) {
    case 'e':
      fatal (reading_file, "%s", msg);

    case 'w':
      error (reading_file, "%s", msg);
      break;

    case 'i':
      printf ("%s\n", msg);
      fflush(stdout);
      break;

    default:
      fatal (*expanding_var, "Internal error: func_error: '%s'", funcname);
  }

  /* The warning function expands to the empty string.  */
  return o;
}


/*
  chop argv[0] into words, and sort them.
 */
static char *
func_sort (char *o, char **argv, const char *funcname UNUSED)
{
  char **words = 0;
  int nwords = 0;
  register int wordi = 0;

  /* Chop ARGV[0] into words and put them in WORDS.  */
  char *t = argv[0];
  char *p;
  unsigned int len;
  int i;

  while ((p = find_next_token (&t, &len)) != 0)
    {
      if (wordi >= nwords - 1)
	{
	  nwords = (2 * nwords) + 5;
	  words = (char **) xrealloc ((char *) words,
				      nwords * sizeof (char *));
	}
      words[wordi++] = savestring (p, len);
    }

  if (!wordi)
    return o;

  /* Now sort the list of words.  */
  qsort ((char *) words, wordi, sizeof (char *), alpha_compare);

  /* Now write the sorted list.  */
  for (i = 0; i < wordi; ++i)
    {
      len = strlen (words[i]);
      if (i == wordi - 1 || strlen (words[i + 1]) != len
          || strcmp (words[i], words[i + 1]))
        {
          o = variable_buffer_output (o, words[i], len);
          o = variable_buffer_output (o, " ", 1);
        }
      free (words[i]);
    }
  /* Kill the last space.  */
  --o;

  free (words);

  return o;
}

/*
  $(if condition,true-part[,false-part])

  CONDITION is false iff it evaluates to an empty string.  White
  space before and after condition are stripped before evaluation.

  If CONDITION is true, then TRUE-PART is evaluated, otherwise FALSE-PART is
  evaluated (if it exists).  Because only one of the two PARTs is evaluated,
  you can use $(if ...) to create side-effects (with $(shell ...), for
  example).
*/

static char *
func_if (char *o, char **argv, const char *funcname UNUSED)
{
  const char *begp = argv[0];
  const char *endp = begp + strlen (argv[0]) - 1;
  int result = 0;

  /* Find the result of the condition: if we have a value, and it's not
     empty, the condition is true.  If we don't have a value, or it's the
     empty string, then it's false.  */

  strip_whitespace (&begp, &endp);

  if (begp <= endp)
    {
      char *expansion = expand_argument (begp, endp+1);

      result = strlen (expansion);
      free (expansion);
    }

  /* If the result is true (1) we want to eval the first argument, and if
     it's false (0) we want to eval the second.  If the argument doesn't
     exist we do nothing, otherwise expand it and add to the buffer.  */

  argv += 1 + !result;

  if (argv[0])
    {
      char *expansion;

      expansion = expand_argument (argv[0], NULL);

      o = variable_buffer_output (o, expansion, strlen (expansion));

      free (expansion);
    }

  return o;
}

/*
  $(or condition1[,condition2[,condition3[...]]])

  A CONDITION is false iff it evaluates to an empty string.  White
  space before and after CONDITION are stripped before evaluation.

  CONDITION1 is evaluated.  If it's true, then this is the result of
  expansion.  If it's false, CONDITION2 is evaluated, and so on.  If none of
  the conditions are true, the expansion is the empty string.

  Once a CONDITION is true no further conditions are evaluated
  (short-circuiting).
*/

static char *
func_or (char *o, char **argv, const char *funcname UNUSED)
{
  for ( ; *argv ; ++argv)
    {
      const char *begp = *argv;
      const char *endp = begp + strlen (*argv) - 1;
      char *expansion;
      int result = 0;

      /* Find the result of the condition: if it's false keep going.  */

      strip_whitespace (&begp, &endp);

      if (begp > endp)
        continue;

      expansion = expand_argument (begp, endp+1);
      result = strlen (expansion);

      /* If the result is false keep going.  */
      if (!result)
        {
          free (expansion);
          continue;
        }

      /* It's true!  Keep this result and return.  */
      o = variable_buffer_output (o, expansion, result);
      free (expansion);
      break;
    }

  return o;
}

/*
  $(and condition1[,condition2[,condition3[...]]])

  A CONDITION is false iff it evaluates to an empty string.  White
  space before and after CONDITION are stripped before evaluation.

  CONDITION1 is evaluated.  If it's false, then this is the result of
  expansion.  If it's true, CONDITION2 is evaluated, and so on.  If all of
  the conditions are true, the expansion is the result of the last condition.

  Once a CONDITION is false no further conditions are evaluated
  (short-circuiting).
*/

static char *
func_and (char *o, char **argv, const char *funcname UNUSED)
{
  char *expansion;
  int result;

  while (1)
    {
      const char *begp = *argv;
      const char *endp = begp + strlen (*argv) - 1;

      /* An empty condition is always false.  */
      strip_whitespace (&begp, &endp);
      if (begp > endp)
        return o;

      expansion = expand_argument (begp, endp+1);
      result = strlen (expansion);

      /* If the result is false, stop here: we're done.  */
      if (!result)
        break;

      /* Otherwise the result is true.  If this is the last one, keep this
         result and quit.  Otherwise go on to the next one!  */

      if (*(++argv))
        free (expansion);
      else
        {
          o = variable_buffer_output (o, expansion, result);
          break;
        }
    }

  free (expansion);

  return o;
}

static char *
func_wildcard (char *o, char **argv, const char *funcname UNUSED)
{

#ifdef _AMIGA
   o = wildcard_expansion (argv[0], o);
#else
   char *p = string_glob (argv[0]);
   o = variable_buffer_output (o, p, strlen (p));
#endif
   return o;
}

/*
  $(eval <makefile string>)

  Always resolves to the empty string.

  Treat the arguments as a segment of makefile, and parse them.
*/

static char *
func_eval (char *o, char **argv, const char *funcname UNUSED)
{
  char *buf;
  unsigned int len;

  /* Eval the buffer.  Pop the current variable buffer setting so that the
     eval'd code can use its own without conflicting.  */

  install_variable_buffer (&buf, &len);

  eval_buffer (argv[0]);

  restore_variable_buffer (buf, len);

  return o;
}


static char *
func_value (char *o, char **argv, const char *funcname UNUSED)
{
  /* Look up the variable.  */
  struct variable *v = lookup_variable (argv[0], strlen (argv[0]));

  /* Copy its value into the output buffer without expanding it.  */
  if (v)
    o = variable_buffer_output (o, v->value, strlen(v->value));

  return o;
}

/*
  \r  is replaced on UNIX as well. Is this desirable?
 */
static void
fold_newlines (char *buffer, unsigned int *length)
{
  char *dst = buffer;
  char *src = buffer;
  char *last_nonnl = buffer -1;
  src[*length] = 0;
  for (; *src != '\0'; ++src)
    {
      if (src[0] == '\r' && src[1] == '\n')
	continue;
      if (*src == '\n')
	{
	  *dst++ = ' ';
	}
      else
	{
	  last_nonnl = dst;
	  *dst++ = *src;
	}
    }
  *(++last_nonnl) = '\0';
  *length = last_nonnl - buffer;
}



int shell_function_pid = 0, shell_function_completed;


#ifdef WINDOWS32
/*untested*/

#include <windows.h>
#include <io.h>
#include "sub_proc.h"


void
windows32_openpipe (int *pipedes, int *pid_p, char **command_argv, char **envp)
{
  SECURITY_ATTRIBUTES saAttr;
  HANDLE hIn;
  HANDLE hErr;
  HANDLE hChildOutRd;
  HANDLE hChildOutWr;
  HANDLE hProcess;


  saAttr.nLength = sizeof (SECURITY_ATTRIBUTES);
  saAttr.bInheritHandle = TRUE;
  saAttr.lpSecurityDescriptor = NULL;

  if (DuplicateHandle (GetCurrentProcess(),
		      GetStdHandle(STD_INPUT_HANDLE),
		      GetCurrentProcess(),
		      &hIn,
		      0,
		      TRUE,
		      DUPLICATE_SAME_ACCESS) == FALSE) {
    fatal (NILF, _("create_child_process: DuplicateHandle(In) failed (e=%ld)\n"),
	   GetLastError());

  }
  if (DuplicateHandle(GetCurrentProcess(),
		      GetStdHandle(STD_ERROR_HANDLE),
		      GetCurrentProcess(),
		      &hErr,
		      0,
		      TRUE,
		      DUPLICATE_SAME_ACCESS) == FALSE) {
    fatal (NILF, _("create_child_process: DuplicateHandle(Err) failed (e=%ld)\n"),
	   GetLastError());
  }

  if (!CreatePipe(&hChildOutRd, &hChildOutWr, &saAttr, 0))
    fatal (NILF, _("CreatePipe() failed (e=%ld)\n"), GetLastError());

  hProcess = process_init_fd(hIn, hChildOutWr, hErr);

  if (!hProcess)
    fatal (NILF, _("windows32_openpipe (): process_init_fd() failed\n"));

  /* make sure that CreateProcess() has Path it needs */
  sync_Path_environment();

  if (!process_begin(hProcess, command_argv, envp, command_argv[0], NULL)) {
    /* register process for wait */
    process_register(hProcess);

    /* set the pid for returning to caller */
    *pid_p = (int) hProcess;

  /* set up to read data from child */
  pipedes[0] = _open_osfhandle((long) hChildOutRd, O_RDONLY);

  /* this will be closed almost right away */
  pipedes[1] = _open_osfhandle((long) hChildOutWr, O_APPEND);
  } else {
    /* reap/cleanup the failed process */
	process_cleanup(hProcess);

    /* close handles which were duplicated, they weren't used */
	CloseHandle(hIn);
	CloseHandle(hErr);

	/* close pipe handles, they won't be used */
	CloseHandle(hChildOutRd);
	CloseHandle(hChildOutWr);

    /* set status for return */
    pipedes[0] = pipedes[1] = -1;
    *pid_p = -1;
  }
}
#endif


#ifdef __MSDOS__
FILE *
msdos_openpipe (int* pipedes, int *pidp, char *text)
{
  FILE *fpipe=0;
  /* MSDOS can't fork, but it has `popen'.  */
  struct variable *sh = lookup_variable ("SHELL", 5);
  int e;
  extern int dos_command_running, dos_status;

  /* Make sure not to bother processing an empty line.  */
  while (isblank ((unsigned char)*text))
    ++text;
  if (*text == '\0')
    return 0;

  if (sh)
    {
      char buf[PATH_MAX + 7];
      /* This makes sure $SHELL value is used by $(shell), even
	 though the target environment is not passed to it.  */
      sprintf (buf, "SHELL=%s", sh->value);
      putenv (buf);
    }

  e = errno;
  errno = 0;
  dos_command_running = 1;
  dos_status = 0;
  /* If dos_status becomes non-zero, it means the child process
     was interrupted by a signal, like SIGINT or SIGQUIT.  See
     fatal_error_signal in commands.c.  */
  fpipe = popen (text, "rt");
  dos_command_running = 0;
  if (!fpipe || dos_status)
    {
      pipedes[0] = -1;
      *pidp = -1;
      if (dos_status)
	errno = EINTR;
      else if (errno == 0)
	errno = ENOMEM;
      shell_function_completed = -1;
    }
  else
    {
      pipedes[0] = fileno (fpipe);
      *pidp = 42; /* Yes, the Meaning of Life, the Universe, and Everything! */
      errno = e;
      shell_function_completed = 1;
    }
  return fpipe;
}
#endif

/*
  Do shell spawning, with the naughty bits for different OSes.
 */

#ifdef VMS

/* VMS can't do $(shell ...)  */
#define func_shell 0

#else
#ifndef _AMIGA
static char *
func_shell (char *o, char **argv, const char *funcname UNUSED)
{
  char* batch_filename = NULL;

#ifdef __MSDOS__
  FILE *fpipe;
#endif
  char **command_argv;
  char *error_prefix;
  char **envp;
  int pipedes[2];
  int pid;

#ifndef __MSDOS__
  /* Construct the argument list.  */
  command_argv = construct_command_argv (argv[0],
					 (char **) NULL, (struct file *) 0,
                                         &batch_filename);
  if (command_argv == 0)
    return o;
#endif

  /* Using a target environment for `shell' loses in cases like:
     export var = $(shell echo foobie)
     because target_environment hits a loop trying to expand $(var)
     to put it in the environment.  This is even more confusing when
     var was not explicitly exported, but just appeared in the
     calling environment.

  envp = target_environment (NILF);
  */

  envp = environ;

  /* For error messages.  */
  if (reading_file && reading_file->filenm)
    {
      error_prefix = (char *) alloca (strlen (reading_file->filenm)+11+4);
      sprintf (error_prefix,
	       "%s:%lu: ", reading_file->filenm, reading_file->lineno);
    }
  else
    error_prefix = "";

#ifdef WINDOWS32

  windows32_openpipe (pipedes, &pid, command_argv, envp);

  if (pipedes[0] < 0) {
	/* open of the pipe failed, mark as failed execution */
    shell_function_completed = -1;

	return o;
  } else

#elif defined(__MSDOS__)

  fpipe = msdos_openpipe (pipedes, &pid, argv[0]);
  if (pipedes[0] < 0)
    {
      perror_with_name (error_prefix, "pipe");
      return o;
    }

#else

  if (pipe (pipedes) < 0)
    {
      perror_with_name (error_prefix, "pipe");
      return o;
    }

# ifdef __EMX__

  /* close some handles that are unnecessary for the child process */
  CLOSE_ON_EXEC(pipedes[1]);
  CLOSE_ON_EXEC(pipedes[0]);
  /* Never use fork()/exec() here! Use spawn() instead in exec_command() */
  pid = child_execute_job (0, pipedes[1], command_argv, envp);
  if (pid < 0)
    perror_with_name (error_prefix, "spawn");

# else /* ! __EMX__ */

  pid = vfork ();
  if (pid < 0)
    perror_with_name (error_prefix, "fork");
  else if (pid == 0)
    child_execute_job (0, pipedes[1], command_argv, envp);
  else

# endif

#endif
    {
      /* We are the parent.  */
      char *buffer;
      unsigned int maxlen, i;
      int cc;

      /* Record the PID for reap_children.  */
      shell_function_pid = pid;
#ifndef  __MSDOS__
      shell_function_completed = 0;

      /* Free the storage only the child needed.  */
      free (command_argv[0]);
      free ((char *) command_argv);

      /* Close the write side of the pipe.  */
      (void) close (pipedes[1]);
#endif

      /* Set up and read from the pipe.  */

      maxlen = 200;
      buffer = (char *) xmalloc (maxlen + 1);

      /* Read from the pipe until it gets EOF.  */
      for (i = 0; ; i += cc)
	{
	  if (i == maxlen)
	    {
	      maxlen += 512;
	      buffer = (char *) xrealloc (buffer, maxlen + 1);
	    }

	  EINTRLOOP (cc, read (pipedes[0], &buffer[i], maxlen - i));
	  if (cc <= 0)
	    break;
	}
      buffer[i] = '\0';

      /* Close the read side of the pipe.  */
#ifdef  __MSDOS__
      if (fpipe)
	(void) pclose (fpipe);
#else
      (void) close (pipedes[0]);
#endif

      /* Loop until child_handler or reap_children()  sets
         shell_function_completed to the status of our child shell.  */
      while (shell_function_completed == 0)
	reap_children (1, 0);

      if (batch_filename) {
	DB (DB_VERBOSE, (_("Cleaning up temporary batch file %s\n"),
                       batch_filename));
	remove (batch_filename);
	free (batch_filename);
      }
      shell_function_pid = 0;

      /* The child_handler function will set shell_function_completed
	 to 1 when the child dies normally, or to -1 if it
	 dies with status 127, which is most likely an exec fail.  */

      if (shell_function_completed == -1)
	{
	  /* This likely means that the execvp failed, so we should just
	     write the error message in the pipe from the child.  */
	  fputs (buffer, stderr);
	  fflush (stderr);
	}
      else
	{
	  /* The child finished normally.  Replace all newlines in its output
	     with spaces, and put that in the variable output buffer.  */
	  fold_newlines (buffer, &i);
	  o = variable_buffer_output (o, buffer, i);
	}

      free (buffer);
    }

  return o;
}

#else	/* _AMIGA */

/* Do the Amiga version of func_shell.  */

static char *
func_shell (char *o, char **argv, const char *funcname)
{
  /* Amiga can't fork nor spawn, but I can start a program with
     redirection of my choice.  However, this means that we
     don't have an opportunity to reopen stdout to trap it.  Thus,
     we save our own stdout onto a new descriptor and dup a temp
     file's descriptor onto our stdout temporarily.  After we
     spawn the shell program, we dup our own stdout back to the
     stdout descriptor.  The buffer reading is the same as above,
     except that we're now reading from a file.  */

#include <dos/dos.h>
#include <proto/dos.h>

  BPTR child_stdout;
  char tmp_output[FILENAME_MAX];
  unsigned int maxlen = 200, i;
  int cc;
  char * buffer, * ptr;
  char ** aptr;
  int len = 0;
  char* batch_filename = NULL;

  /* Construct the argument list.  */
  command_argv = construct_command_argv (argv[0], (char **) NULL,
                                         (struct file *) 0, &batch_filename);
  if (command_argv == 0)
    return o;

  /* Note the mktemp() is a security hole, but this only runs on Amiga.
     Ideally we would use main.c:open_tmpfile(), but this uses a special
     Open(), not fopen(), and I'm not familiar enough with the code to mess
     with it.  */
  strcpy (tmp_output, "t:MakeshXXXXXXXX");
  mktemp (tmp_output);
  child_stdout = Open (tmp_output, MODE_NEWFILE);

  for (aptr=command_argv; *aptr; aptr++)
    len += strlen (*aptr) + 1;

  buffer = xmalloc (len + 1);
  ptr = buffer;

  for (aptr=command_argv; *aptr; aptr++)
    {
      strcpy (ptr, *aptr);
      ptr += strlen (ptr) + 1;
      *ptr ++ = ' ';
      *ptr = 0;
    }

  ptr[-1] = '\n';

  Execute (buffer, NULL, child_stdout);
  free (buffer);

  Close (child_stdout);

  child_stdout = Open (tmp_output, MODE_OLDFILE);

  buffer = xmalloc (maxlen);
  i = 0;
  do
    {
      if (i == maxlen)
	{
	  maxlen += 512;
	  buffer = (char *) xrealloc (buffer, maxlen + 1);
	}

      cc = Read (child_stdout, &buffer[i], maxlen - i);
      if (cc > 0)
	i += cc;
    } while (cc > 0);

  Close (child_stdout);

  fold_newlines (buffer, &i);
  o = variable_buffer_output (o, buffer, i);
  free (buffer);
  return o;
}
#endif  /* _AMIGA */
#endif  /* !VMS */

#ifdef EXPERIMENTAL

/*
  equality. Return is string-boolean, ie, the empty string is false.
 */
static char *
func_eq (char *o, char **argv, char *funcname)
{
  int result = ! strcmp (argv[0], argv[1]);
  o = variable_buffer_output (o,  result ? "1" : "", result);
  return o;
}


/*
  string-boolean not operator.
 */
static char *
func_not (char *o, char **argv, char *funcname)
{
  char *s = argv[0];
  int result = 0;
  while (isspace ((unsigned char)*s))
    s++;
  result = ! (*s);
  o = variable_buffer_output (o,  result ? "1" : "", result);
  return o;
}
#endif


/* Return the absolute name of file NAME which does not contain any `.',
   `..' components nor any repeated path separators ('/').   */

static char *
abspath (const char *name, char *apath)
{
  char *dest;
  const char *start, *end, *apath_limit;

  if (name[0] == '\0' || apath == NULL)
    return NULL;

  apath_limit = apath + GET_PATH_MAX;

  if (name[0] != '/')
    {
      /* It is unlikely we would make it until here but just to make sure. */
      if (!starting_directory)
	return NULL;

      strcpy (apath, starting_directory);

      dest = strchr (apath, '\0');
    }
  else
    {
      apath[0] = '/';
      dest = apath + 1;
    }

  for (start = end = name; *start != '\0'; start = end)
    {
      unsigned long len;

      /* Skip sequence of multiple path-separators.  */
      while (*start == '/')
	++start;

      /* Find end of path component.  */
      for (end = start; *end != '\0' && *end != '/'; ++end)
        ;

      len = end - start;

      if (len == 0)
	break;
      else if (len == 1 && start[0] == '.')
	/* nothing */;
      else if (len == 2 && start[0] == '.' && start[1] == '.')
	{
	  /* Back up to previous component, ignore if at root already.  */
	  if (dest > apath + 1)
	    while ((--dest)[-1] != '/');
	}
      else
	{
	  if (dest[-1] != '/')
            *dest++ = '/';

	  if (dest + len >= apath_limit)
            return NULL;

	  dest = memcpy (dest, start, len);
          dest += len;
	  *dest = '\0';
	}
    }

  /* Unless it is root strip trailing separator.  */
  if (dest > apath + 1 && dest[-1] == '/')
    --dest;

  *dest = '\0';

  return apath;
}


static char *
func_realpath (char *o, char **argv, const char *funcname UNUSED)
{
  /* Expand the argument.  */
  char *p = argv[0];
  char *path = 0;
  int doneany = 0;
  unsigned int len = 0;
  PATH_VAR (in);
  PATH_VAR (out);

  while ((path = find_next_token (&p, &len)) != 0)
    {
      if (len < GET_PATH_MAX)
        {
          strncpy (in, path, len);
          in[len] = '\0';

          if
          (
#ifdef HAVE_REALPATH
            realpath (in, out)
#else
            abspath (in, out)
#endif
          )
            {
              o = variable_buffer_output (o, out, strlen (out));
              o = variable_buffer_output (o, " ", 1);
              doneany = 1;
            }
        }
    }

  /* Kill last space.  */
  if (doneany)
    --o;

 return o;
}

static char *
func_abspath (char *o, char **argv, const char *funcname UNUSED)
{
  /* Expand the argument.  */
  char *p = argv[0];
  char *path = 0;
  int doneany = 0;
  unsigned int len = 0;
  PATH_VAR (in);
  PATH_VAR (out);

  while ((path = find_next_token (&p, &len)) != 0)
    {
      if (len < GET_PATH_MAX)
        {
          strncpy (in, path, len);
          in[len] = '\0';

          if (abspath (in, out))
            {
              o = variable_buffer_output (o, out, strlen (out));
              o = variable_buffer_output (o, " ", 1);
              doneany = 1;
            }
        }
    }

  /* Kill last space.  */
  if (doneany)
    --o;

 return o;
}

/* Lookup table for builtin functions.

   This doesn't have to be sorted; we use a straight lookup.  We might gain
   some efficiency by moving most often used functions to the start of the
   table.

   If MAXIMUM_ARGS is 0, that means there is no maximum and all
   comma-separated values are treated as arguments.

   EXPAND_ARGS means that all arguments should be expanded before invocation.
   Functions that do namespace tricks (foreach) don't automatically expand.  */

static char *func_call PARAMS ((char *o, char **argv, const char *funcname));


static struct function_table_entry function_table_init[] =
{
 /* Name/size */                    /* MIN MAX EXP? Function */
  { STRING_SIZE_TUPLE("abspath"),       0,  1,  1,  func_abspath},
  { STRING_SIZE_TUPLE("addprefix"),     2,  2,  1,  func_addsuffix_addprefix},
  { STRING_SIZE_TUPLE("addsuffix"),     2,  2,  1,  func_addsuffix_addprefix},
  { STRING_SIZE_TUPLE("basename"),      0,  1,  1,  func_basename_dir},
  { STRING_SIZE_TUPLE("dir"),           0,  1,  1,  func_basename_dir},
  { STRING_SIZE_TUPLE("notdir"),        0,  1,  1,  func_notdir_suffix},
  { STRING_SIZE_TUPLE("subst"),         3,  3,  1,  func_subst},
  { STRING_SIZE_TUPLE("suffix"),        0,  1,  1,  func_notdir_suffix},
  { STRING_SIZE_TUPLE("filter"),        2,  2,  1,  func_filter_filterout},
  { STRING_SIZE_TUPLE("filter-out"),    2,  2,  1,  func_filter_filterout},
  { STRING_SIZE_TUPLE("findstring"),    2,  2,  1,  func_findstring},
  { STRING_SIZE_TUPLE("firstword"),     0,  1,  1,  func_firstword},
  { STRING_SIZE_TUPLE("flavor"),        0,  1,  1,  func_flavor},
  { STRING_SIZE_TUPLE("join"),          2,  2,  1,  func_join},
  { STRING_SIZE_TUPLE("lastword"),      0,  1,  1,  func_lastword},
  { STRING_SIZE_TUPLE("patsubst"),      3,  3,  1,  func_patsubst},
  { STRING_SIZE_TUPLE("realpath"),      0,  1,  1,  func_realpath},
  { STRING_SIZE_TUPLE("shell"),         0,  1,  1,  func_shell},
  { STRING_SIZE_TUPLE("sort"),          0,  1,  1,  func_sort},
  { STRING_SIZE_TUPLE("strip"),         0,  1,  1,  func_strip},
  { STRING_SIZE_TUPLE("wildcard"),      0,  1,  1,  func_wildcard},
  { STRING_SIZE_TUPLE("word"),          2,  2,  1,  func_word},
  { STRING_SIZE_TUPLE("wordlist"),      3,  3,  1,  func_wordlist},
  { STRING_SIZE_TUPLE("words"),         0,  1,  1,  func_words},
  { STRING_SIZE_TUPLE("origin"),        0,  1,  1,  func_origin},
  { STRING_SIZE_TUPLE("foreach"),       3,  3,  0,  func_foreach},
  { STRING_SIZE_TUPLE("call"),          1,  0,  1,  func_call},
  { STRING_SIZE_TUPLE("info"),          0,  1,  1,  func_error},
  { STRING_SIZE_TUPLE("error"),         0,  1,  1,  func_error},
  { STRING_SIZE_TUPLE("warning"),       0,  1,  1,  func_error},
  { STRING_SIZE_TUPLE("if"),            2,  3,  0,  func_if},
  { STRING_SIZE_TUPLE("or"),            1,  0,  0,  func_or},
  { STRING_SIZE_TUPLE("and"),           1,  0,  0,  func_and},
  { STRING_SIZE_TUPLE("value"),         0,  1,  1,  func_value},
  { STRING_SIZE_TUPLE("eval"),          0,  1,  1,  func_eval},
#ifdef EXPERIMENTAL
  { STRING_SIZE_TUPLE("eq"),            2,  2,  1,  func_eq},
  { STRING_SIZE_TUPLE("not"),           0,  1,  1,  func_not},
#endif
};

#define FUNCTION_TABLE_ENTRIES (sizeof (function_table_init) / sizeof (struct function_table_entry))


/* These must come after the definition of function_table.  */

static char *
expand_builtin_function (char *o, int argc, char **argv,
                         const struct function_table_entry *entry_p)
{
  if (argc < (int)entry_p->minimum_args)
    fatal (*expanding_var,
           _("insufficient number of arguments (%d) to function `%s'"),
           argc, entry_p->name);

  /* I suppose technically some function could do something with no
     arguments, but so far none do, so just test it for all functions here
     rather than in each one.  We can change it later if necessary.  */

  if (!argc)
    return o;

  if (!entry_p->func_ptr)
    fatal (*expanding_var,
           _("unimplemented on this platform: function `%s'"), entry_p->name);

  return entry_p->func_ptr (o, argv, entry_p->name);
}

/* Check for a function invocation in *STRINGP.  *STRINGP points at the
   opening ( or { and is not null-terminated.  If a function invocation
   is found, expand it into the buffer at *OP, updating *OP, incrementing
   *STRINGP past the reference and returning nonzero.  If not, return zero.  */

int
handle_function (char **op, char **stringp)
{
  const struct function_table_entry *entry_p;
  char openparen = (*stringp)[0];
  char closeparen = openparen == '(' ? ')' : '}';
  char *beg;
  char *end;
  int count = 0;
  register char *p;
  char **argv, **argvp;
  int nargs;

  beg = *stringp + 1;

  entry_p = lookup_function (beg);

  if (!entry_p)
    return 0;

  /* We found a builtin function.  Find the beginning of its arguments (skip
     whitespace after the name).  */

  beg = next_token (beg + entry_p->len);

  /* Find the end of the function invocation, counting nested use of
     whichever kind of parens we use.  Since we're looking, count commas
     to get a rough estimate of how many arguments we might have.  The
     count might be high, but it'll never be low.  */

  for (nargs=1, end=beg; *end != '\0'; ++end)
    if (*end == ',')
      ++nargs;
    else if (*end == openparen)
      ++count;
    else if (*end == closeparen && --count < 0)
      break;

  if (count >= 0)
    fatal (*expanding_var,
	   _("unterminated call to function `%s': missing `%c'"),
	   entry_p->name, closeparen);

  *stringp = end;

  /* Get some memory to store the arg pointers.  */
  argvp = argv = (char **) alloca (sizeof (char *) * (nargs + 2));

  /* Chop the string into arguments, then a nul.  As soon as we hit
     MAXIMUM_ARGS (if it's >0) assume the rest of the string is part of the
     last argument.

     If we're expanding, store pointers to the expansion of each one.  If
     not, make a duplicate of the string and point into that, nul-terminating
     each argument.  */

  if (!entry_p->expand_args)
    {
      int len = end - beg;

      p = xmalloc (len+1);
      memcpy (p, beg, len);
      p[len] = '\0';
      beg = p;
      end = beg + len;
    }

  for (p=beg, nargs=0; p <= end; ++argvp)
    {
      char *next;

      ++nargs;

      if (nargs == entry_p->maximum_args
          || (! (next = find_next_argument (openparen, closeparen, p, end))))
        next = end;

      if (entry_p->expand_args)
        *argvp = expand_argument (p, next);
      else
        {
          *argvp = p;
          *next = '\0';
        }

      p = next + 1;
    }
  *argvp = NULL;

  /* Finally!  Run the function...  */
  *op = expand_builtin_function (*op, nargs, argv, entry_p);

  /* Free memory.  */
  if (entry_p->expand_args)
    for (argvp=argv; *argvp != 0; ++argvp)
      free (*argvp);
  else
    free (beg);

  return 1;
}


/* User-defined functions.  Expand the first argument as either a builtin
   function or a make variable, in the context of the rest of the arguments
   assigned to $1, $2, ... $N.  $0 is the name of the function.  */

static char *
func_call (char *o, char **argv, const char *funcname UNUSED)
{
  static int max_args = 0;
  char *fname;
  char *cp;
  char *body;
  int flen;
  int i;
  int saved_args;
  const struct function_table_entry *entry_p;
  struct variable *v;

  /* There is no way to define a variable with a space in the name, so strip
     leading and trailing whitespace as a favor to the user.  */
  fname = argv[0];
  while (*fname != '\0' && isspace ((unsigned char)*fname))
    ++fname;

  cp = fname + strlen (fname) - 1;
  while (cp > fname && isspace ((unsigned char)*cp))
    --cp;
  cp[1] = '\0';

  /* Calling nothing is a no-op */
  if (*fname == '\0')
    return o;

  /* Are we invoking a builtin function?  */

  entry_p = lookup_function (fname);

  if (entry_p)
    {
      /* How many arguments do we have?  */
      for (i=0; argv[i+1]; ++i)
  	;

      return expand_builtin_function (o, i, argv+1, entry_p);
    }

  /* Not a builtin, so the first argument is the name of a variable to be
     expanded and interpreted as a function.  Find it.  */
  flen = strlen (fname);

  v = lookup_variable (fname, flen);

  if (v == 0)
    warn_undefined (fname, flen);

  if (v == 0 || *v->value == '\0')
    return o;

  body = (char *) alloca (flen + 4);
  body[0] = '$';
  body[1] = '(';
  memcpy (body + 2, fname, flen);
  body[flen+2] = ')';
  body[flen+3] = '\0';

  /* Set up arguments $(1) .. $(N).  $(0) is the function name.  */

  push_new_variable_scope ();

  for (i=0; *argv; ++i, ++argv)
    {
      char num[11];

      sprintf (num, "%d", i);
      define_variable (num, strlen (num), *argv, o_automatic, 0);
    }

  /* If the number of arguments we have is < max_args, it means we're inside
     a recursive invocation of $(call ...).  Fill in the remaining arguments
     in the new scope with the empty value, to hide them from this
     invocation.  */

  for (; i < max_args; ++i)
    {
      char num[11];

      sprintf (num, "%d", i);
      define_variable (num, strlen (num), "", o_automatic, 0);
    }

  /* Expand the body in the context of the arguments, adding the result to
     the variable buffer.  */

  v->exp_count = EXP_COUNT_MAX;

  saved_args = max_args;
  max_args = i;
  o = variable_expand_string (o, body, flen+3);
  max_args = saved_args;

  v->exp_count = 0;

  pop_variable_scope ();

  return o + strlen (o);
}

void
hash_init_function_table (void)
{
  hash_init (&function_table, FUNCTION_TABLE_ENTRIES * 2,
	     function_table_entry_hash_1, function_table_entry_hash_2,
	     function_table_entry_hash_cmp);
  hash_load (&function_table, function_table_init,
	     FUNCTION_TABLE_ENTRIES, sizeof (struct function_table_entry));
}
