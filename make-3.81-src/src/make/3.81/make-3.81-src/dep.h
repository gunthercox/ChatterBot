/* Definitions of dependency data structures for GNU Make.
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

/* Flag bits for the second argument to `read_makefile'.
   These flags are saved in the `changed' field of each
   `struct dep' in the chain returned by `read_all_makefiles'.  */

#define RM_NO_DEFAULT_GOAL	(1 << 0) /* Do not set default goal.  */
#define RM_INCLUDED		(1 << 1) /* Search makefile search path.  */
#define RM_DONTCARE		(1 << 2) /* No error if it doesn't exist.  */
#define RM_NO_TILDE		(1 << 3) /* Don't expand ~ in file name.  */
#define RM_NOFLAG		0

/* Structure representing one dependency of a file.
   Each struct file's `deps' points to a chain of these,
   chained through the `next'. `stem' is the stem for this
   dep line of static pattern rule or NULL.

   Note that the first two words of this match a struct nameseq.  */

struct dep
  {
    struct dep *next;
    char *name;
    char *stem;
    struct file *file;
    unsigned int changed : 8;
    unsigned int ignore_mtime : 1;
    unsigned int staticpattern : 1;
    unsigned int need_2nd_expansion : 1;
  };


/* Structure used in chains of names, for parsing and globbing.  */

struct nameseq
  {
    struct nameseq *next;
    char *name;
  };


extern struct nameseq *multi_glob PARAMS ((struct nameseq *chain, unsigned int size));
#ifdef VMS
extern struct nameseq *parse_file_seq ();
#else
extern struct nameseq *parse_file_seq PARAMS ((char **stringp, int stopchar, unsigned int size, int strip));
#endif
extern char *tilde_expand PARAMS ((char *name));

#ifndef NO_ARCHIVES
extern struct nameseq *ar_glob PARAMS ((char *arname, char *member_pattern, unsigned int size));
#endif

#ifndef	iAPX286
#define dep_name(d) ((d)->name == 0 ? (d)->file->name : (d)->name)
#else
/* Buggy compiler can't hack this.  */
extern char *dep_name ();
#endif

extern struct dep *alloc_dep PARAMS ((void));
extern void free_dep PARAMS ((struct dep *d));
extern struct dep *copy_dep_chain PARAMS ((const struct dep *d));
extern void free_dep_chain PARAMS ((struct dep *d));
extern void free_ns_chain PARAMS ((struct nameseq *n));
extern struct dep *read_all_makefiles PARAMS ((char **makefiles));
extern int eval_buffer PARAMS ((char *buffer));
extern int update_goal_chain PARAMS ((struct dep *goals));
extern void uniquize_deps PARAMS ((struct dep *));
