/* Definition of target file data structures for GNU Make.
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


/* Structure that represents the info on one file
   that the makefile says how to make.
   All of these are chained together through `next'.  */

#include "hash.h"

struct file
  {
    char *name;
    char *hname;                /* Hashed filename */
    char *vpath;                /* VPATH/vpath pathname */
    struct dep *deps;		/* all dependencies, including duplicates */
    struct commands *cmds;	/* Commands to execute for this target.  */
    int command_flags;		/* Flags OR'd in for cmds; see commands.h.  */
    char *stem;			/* Implicit stem, if an implicit
    				   rule has been used */
    struct dep *also_make;	/* Targets that are made by making this.  */
    FILE_TIMESTAMP last_mtime;	/* File's modtime, if already known.  */
    FILE_TIMESTAMP mtime_before_update;	/* File's modtime before any updating
                                           has been performed.  */
    struct file *prev;		/* Previous entry for same file name;
				   used when there are multiple double-colon
				   entries for the same file.  */
    struct file *last;          /* Last entry for the same file name.  */

    /* File that this file was renamed to.  After any time that a
       file could be renamed, call `check_renamed' (below).  */
    struct file *renamed;

    /* List of variable sets used for this file.  */
    struct variable_set_list *variables;

    /* Pattern-specific variable reference for this target, or null if there
       isn't one.  Also see the pat_searched flag, below.  */
    struct variable_set_list *pat_variables;

    /* Immediate dependent that caused this target to be remade,
       or nil if there isn't one.  */
    struct file *parent;

    /* For a double-colon entry, this is the first double-colon entry for
       the same file.  Otherwise this is null.  */
    struct file *double_colon;

    short int update_status;	/* Status of the last attempt to update,
				   or -1 if none has been made.  */

    enum cmd_state		/* State of the commands.  */
      {		/* Note: It is important that cs_not_started be zero.  */
	cs_not_started,		/* Not yet started.  */
	cs_deps_running,	/* Dep commands running.  */
	cs_running,		/* Commands running.  */
	cs_finished		/* Commands finished.  */
      } command_state ENUM_BITFIELD (2);

    unsigned int precious:1;	/* Non-0 means don't delete file on quit */
    unsigned int low_resolution_time:1;	/* Nonzero if this file's time stamp
					   has only one-second resolution.  */
    unsigned int tried_implicit:1; /* Nonzero if have searched
				      for implicit rule for making
				      this file; don't search again.  */
    unsigned int updating:1;	/* Nonzero while updating deps of this file */
    unsigned int updated:1;	/* Nonzero if this file has been remade.  */
    unsigned int is_target:1;	/* Nonzero if file is described as target.  */
    unsigned int cmd_target:1;	/* Nonzero if file was given on cmd line.  */
    unsigned int phony:1;	/* Nonzero if this is a phony file
				   i.e., a prerequisite of .PHONY.  */
    unsigned int intermediate:1;/* Nonzero if this is an intermediate file.  */
    unsigned int secondary:1;   /* Nonzero means remove_intermediates should
                                   not delete it.  */
    unsigned int dontcare:1;	/* Nonzero if no complaint is to be made if
				   this target cannot be remade.  */
    unsigned int ignore_vpath:1;/* Nonzero if we threw out VPATH name.  */
    unsigned int pat_searched:1;/* Nonzero if we already searched for
                                   pattern-specific variables.  */
    unsigned int considered:1;  /* equal to 'considered' if file has been
                                   considered on current scan of goal chain */
  };


extern struct file *default_goal_file, *suffix_file, *default_file;
extern char **default_goal_name;


extern struct file *lookup_file PARAMS ((char *name));
extern struct file *enter_file PARAMS ((char *name));
extern struct dep *parse_prereqs PARAMS ((char *prereqs));
extern void remove_intermediates PARAMS ((int sig));
extern void snap_deps PARAMS ((void));
extern void rename_file PARAMS ((struct file *file, char *name));
extern void rehash_file PARAMS ((struct file *file, char *name));
extern void set_command_state PARAMS ((struct file *file, enum cmd_state state));
extern void notice_finished_file PARAMS ((struct file *file));
extern void init_hash_files PARAMS ((void));
extern char *build_target_list PARAMS ((char *old_list));

#if FILE_TIMESTAMP_HI_RES
# define FILE_TIMESTAMP_STAT_MODTIME(fname, st) \
    file_timestamp_cons (fname, (st).st_mtime, (st).st_mtim.ST_MTIM_NSEC)
#else
# define FILE_TIMESTAMP_STAT_MODTIME(fname, st) \
    file_timestamp_cons (fname, (st).st_mtime, 0)
#endif

/* If FILE_TIMESTAMP is 64 bits (or more), use nanosecond resolution.
   (Multiply by 2**30 instead of by 10**9 to save time at the cost of
   slightly decreasing the number of available timestamps.)  With
   64-bit FILE_TIMESTAMP, this stops working on 2514-05-30 01:53:04
   UTC, but by then uintmax_t should be larger than 64 bits.  */
#define FILE_TIMESTAMPS_PER_S (FILE_TIMESTAMP_HI_RES ? 1000000000 : 1)
#define FILE_TIMESTAMP_LO_BITS (FILE_TIMESTAMP_HI_RES ? 30 : 0)

#define FILE_TIMESTAMP_S(ts) (((ts) - ORDINARY_MTIME_MIN) \
			      >> FILE_TIMESTAMP_LO_BITS)
#define FILE_TIMESTAMP_NS(ts) ((int) (((ts) - ORDINARY_MTIME_MIN) \
				      & ((1 << FILE_TIMESTAMP_LO_BITS) - 1)))

/* Upper bound on length of string "YYYY-MM-DD HH:MM:SS.NNNNNNNNN"
   representing a file timestamp.  The upper bound is not necessarily 19,
   since the year might be less than -999 or greater than 9999.

   Subtract one for the sign bit if in case file timestamps can be negative;
   subtract FLOOR_LOG2_SECONDS_PER_YEAR to yield an upper bound on how many
   file timestamp bits might affect the year;
   302 / 1000 is log10 (2) rounded up;
   add one for integer division truncation;
   add one more for a minus sign if file timestamps can be negative;
   add 4 to allow for any 4-digit epoch year (e.g. 1970);
   add 25 to allow for "-MM-DD HH:MM:SS.NNNNNNNNN".  */
#define FLOOR_LOG2_SECONDS_PER_YEAR 24
#define FILE_TIMESTAMP_PRINT_LEN_BOUND \
  (((sizeof (FILE_TIMESTAMP) * CHAR_BIT - 1 - FLOOR_LOG2_SECONDS_PER_YEAR) \
    * 302 / 1000) \
   + 1 + 1 + 4 + 25)

extern FILE_TIMESTAMP file_timestamp_cons PARAMS ((char const *,
						   time_t, int));
extern FILE_TIMESTAMP file_timestamp_now PARAMS ((int *));
extern void file_timestamp_sprintf PARAMS ((char *p, FILE_TIMESTAMP ts));

/* Return the mtime of file F (a struct file *), caching it.
   The value is NONEXISTENT_MTIME if the file does not exist.  */
#define file_mtime(f) file_mtime_1 ((f), 1)
/* Return the mtime of file F (a struct file *), caching it.
   Don't search using vpath for the file--if it doesn't actually exist,
   we don't find it.
   The value is NONEXISTENT_MTIME if the file does not exist.  */
#define file_mtime_no_search(f) file_mtime_1 ((f), 0)
extern FILE_TIMESTAMP f_mtime PARAMS ((struct file *file, int search));
#define file_mtime_1(f, v) \
  ((f)->last_mtime == UNKNOWN_MTIME ? f_mtime ((f), v) : (f)->last_mtime)

/* Special timestamp values.  */

/* The file's timestamp is not yet known.  */
#define UNKNOWN_MTIME 0

/* The file does not exist.  */
#define NONEXISTENT_MTIME 1

/* The file does not exist, and we assume that it is older than any
   actual file.  */
#define OLD_MTIME 2

/* The smallest and largest ordinary timestamps.  */
#define ORDINARY_MTIME_MIN (OLD_MTIME + 1)
#define ORDINARY_MTIME_MAX ((FILE_TIMESTAMP_S (NEW_MTIME) \
			     << FILE_TIMESTAMP_LO_BITS) \
			    + ORDINARY_MTIME_MIN + FILE_TIMESTAMPS_PER_S - 1)

/* Modtime value to use for `infinitely new'.  We used to get the current time
   from the system and use that whenever we wanted `new'.  But that causes
   trouble when the machine running make and the machine holding a file have
   different ideas about what time it is; and can also lose for `force'
   targets, which need to be considered newer than anything that depends on
   them, even if said dependents' modtimes are in the future.  */
#define NEW_MTIME INTEGER_TYPE_MAXIMUM (FILE_TIMESTAMP)

#define check_renamed(file) \
  while ((file)->renamed != 0) (file) = (file)->renamed /* No ; here.  */

/* Have we snapped deps yet?  */
extern int snapped_deps;
