/* Directory hashing for GNU Make.
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
#include "hash.h"

#ifdef	HAVE_DIRENT_H
# include <dirent.h>
# define NAMLEN(dirent) strlen((dirent)->d_name)
# ifdef VMS
extern char *vmsify PARAMS ((char *name, int type));
# endif
#else
# define dirent direct
# define NAMLEN(dirent) (dirent)->d_namlen
# ifdef HAVE_SYS_NDIR_H
#  include <sys/ndir.h>
# endif
# ifdef HAVE_SYS_DIR_H
#  include <sys/dir.h>
# endif
# ifdef HAVE_NDIR_H
#  include <ndir.h>
# endif
# ifdef HAVE_VMSDIR_H
#  include "vmsdir.h"
# endif /* HAVE_VMSDIR_H */
#endif

/* In GNU systems, <dirent.h> defines this macro for us.  */
#ifdef _D_NAMLEN
# undef NAMLEN
# define NAMLEN(d) _D_NAMLEN(d)
#endif

#if (defined (POSIX) || defined (VMS) || defined (WINDOWS32)) && !defined (__GNU_LIBRARY__)
/* Posix does not require that the d_ino field be present, and some
   systems do not provide it. */
# define REAL_DIR_ENTRY(dp) 1
# define FAKE_DIR_ENTRY(dp)
#else
# define REAL_DIR_ENTRY(dp) (dp->d_ino != 0)
# define FAKE_DIR_ENTRY(dp) (dp->d_ino = 1)
#endif /* POSIX */

#ifdef __MSDOS__
#include <ctype.h>
#include <fcntl.h>

/* If it's MSDOS that doesn't have _USE_LFN, disable LFN support.  */
#ifndef _USE_LFN
#define _USE_LFN 0
#endif

static char *
dosify (char *filename)
{
  static char dos_filename[14];
  char *df;
  int i;

  if (filename == 0 || _USE_LFN)
    return filename;

  /* FIXME: what about filenames which violate
     8+3 constraints, like "config.h.in", or ".emacs"?  */
  if (strpbrk (filename, "\"*+,;<=>?[\\]|") != 0)
    return filename;

  df = dos_filename;

  /* First, transform the name part.  */
  for (i = 0; *filename != '\0' && i < 8 && *filename != '.'; ++i)
    *df++ = tolower ((unsigned char)*filename++);

  /* Now skip to the next dot.  */
  while (*filename != '\0' && *filename != '.')
    ++filename;
  if (*filename != '\0')
    {
      *df++ = *filename++;
      for (i = 0; *filename != '\0' && i < 3 && *filename != '.'; ++i)
	*df++ = tolower ((unsigned char)*filename++);
    }

  /* Look for more dots.  */
  while (*filename != '\0' && *filename != '.')
    ++filename;
  if (*filename == '.')
    return filename;
  *df = 0;
  return dos_filename;
}
#endif /* __MSDOS__ */

#ifdef WINDOWS32
#include "pathstuff.h"
#endif

#ifdef _AMIGA
#include <ctype.h>
#endif

#ifdef HAVE_CASE_INSENSITIVE_FS
static char *
downcase (char *filename)
{
  static PATH_VAR (new_filename);
  char *df;
  int i;

  if (filename == 0)
    return 0;

  df = new_filename;

  /* First, transform the name part.  */
  for (i = 0; *filename != '\0'; ++i)
  {
    *df++ = tolower ((unsigned char)*filename);
    ++filename;
  }

  *df = 0;

  return new_filename;
}
#endif /* HAVE_CASE_INSENSITIVE_FS */

#ifdef VMS

static int
vms_hash (char *name)
{
  int h = 0;
  int g;

  while (*name)
    {
      unsigned char uc = *name;
#ifdef HAVE_CASE_INSENSITIVE_FS
      h = (h << 4) + (isupper (uc) ? tolower (uc) : uc);
#else
      h = (h << 4) + uc;
#endif
      name++;
      g = h & 0xf0000000;
      if (g)
	{
	  h = h ^ (g >> 24);
	  h = h ^ g;
	}
    }
  return h;
}

/* fake stat entry for a directory */
static int
vmsstat_dir (char *name, struct stat *st)
{
  char *s;
  int h;
  DIR *dir;

  dir = opendir (name);
  if (dir == 0)
    return -1;
  closedir (dir);
  s = strchr (name, ':');	/* find device */
  if (s)
    {
      *s++ = 0;
      st->st_dev = (char *)vms_hash (name);
      h = vms_hash (s);
      *(s-1) = ':';
    }
  else
    {
      st->st_dev = 0;
      s = name;
      h = vms_hash (s);
    }

  st->st_ino[0] = h & 0xff;
  st->st_ino[1] = h & 0xff00;
  st->st_ino[2] = h >> 16;

  return 0;
}
#endif /* VMS */

/* Hash table of directories.  */

#ifndef	DIRECTORY_BUCKETS
#define DIRECTORY_BUCKETS 199
#endif

struct directory_contents
  {
    dev_t dev;			/* Device and inode numbers of this dir.  */
#ifdef WINDOWS32
    /*
     * Inode means nothing on WINDOWS32. Even file key information is
     * unreliable because it is random per file open and undefined
     * for remote filesystems. The most unique attribute I can
     * come up with is the fully qualified name of the directory. Beware
     * though, this is also unreliable. I'm open to suggestion on a better
     * way to emulate inode.
     */
    char *path_key;
    int   ctime;
    int   mtime;        /* controls check for stale directory cache */
    int   fs_flags;     /* FS_FAT, FS_NTFS, ... */
#define FS_FAT      0x1
#define FS_NTFS     0x2
#define FS_UNKNOWN  0x4
#else
#ifdef VMS
    ino_t ino[3];
#else
    ino_t ino;
#endif
#endif /* WINDOWS32 */
    struct hash_table dirfiles;	/* Files in this directory.  */
    DIR *dirstream;		/* Stream reading this directory.  */
  };

static unsigned long
directory_contents_hash_1 (const void *key_0)
{
  struct directory_contents const *key = (struct directory_contents const *) key_0;
  unsigned long hash;

#ifdef WINDOWS32
  hash = 0;
  ISTRING_HASH_1 (key->path_key, hash);
  hash ^= ((unsigned int) key->dev << 4) ^ (unsigned int) key->ctime;
#else
# ifdef VMS
  hash = (((unsigned int) key->dev << 4)
	  ^ ((unsigned int) key->ino[0]
	     + (unsigned int) key->ino[1]
	     + (unsigned int) key->ino[2]));
# else
  hash = ((unsigned int) key->dev << 4) ^ (unsigned int) key->ino;
# endif
#endif /* WINDOWS32 */
  return hash;
}

static unsigned long
directory_contents_hash_2 (const void *key_0)
{
  struct directory_contents const *key = (struct directory_contents const *) key_0;
  unsigned long hash;

#ifdef WINDOWS32
  hash = 0;
  ISTRING_HASH_2 (key->path_key, hash);
  hash ^= ((unsigned int) key->dev << 4) ^ (unsigned int) ~key->ctime;
#else
# ifdef VMS
  hash = (((unsigned int) key->dev << 4)
	  ^ ~((unsigned int) key->ino[0]
	      + (unsigned int) key->ino[1]
	      + (unsigned int) key->ino[2]));
# else
  hash = ((unsigned int) key->dev << 4) ^ (unsigned int) ~key->ino;
# endif
#endif /* WINDOWS32 */

  return hash;
}

/* Sometimes it's OK to use subtraction to get this value:
     result = X - Y;
   But, if we're not sure of the type of X and Y they may be too large for an
   int (on a 64-bit system for example).  So, use ?: instead.
   See Savannah bug #15534.

   NOTE!  This macro has side-effects!
*/

#define MAKECMP(_x,_y)  ((_x)<(_y)?-1:((_x)==(_y)?0:1))

static int
directory_contents_hash_cmp (const void *xv, const void *yv)
{
  struct directory_contents const *x = (struct directory_contents const *) xv;
  struct directory_contents const *y = (struct directory_contents const *) yv;
  int result;

#ifdef WINDOWS32
  ISTRING_COMPARE (x->path_key, y->path_key, result);
  if (result)
    return result;
  result = MAKECMP(x->ctime, y->ctime);
  if (result)
    return result;
#else
# ifdef VMS
  result = MAKECMP(x->ino[0], y->ino[0]);
  if (result)
    return result;
  result = MAKECMP(x->ino[1], y->ino[1]);
  if (result)
    return result;
  result = MAKECMP(x->ino[2], y->ino[2]);
  if (result)
    return result;
# else
  result = MAKECMP(x->ino, y->ino);
  if (result)
    return result;
# endif
#endif /* WINDOWS32 */

  return MAKECMP(x->dev, y->dev);
}

/* Table of directory contents hashed by device and inode number.  */
static struct hash_table directory_contents;

struct directory
  {
    char *name;			/* Name of the directory.  */

    /* The directory's contents.  This data may be shared by several
       entries in the hash table, which refer to the same directory
       (identified uniquely by `dev' and `ino') under different names.  */
    struct directory_contents *contents;
  };

static unsigned long
directory_hash_1 (const void *key)
{
  return_ISTRING_HASH_1 (((struct directory const *) key)->name);
}

static unsigned long
directory_hash_2 (const void *key)
{
  return_ISTRING_HASH_2 (((struct directory const *) key)->name);
}

static int
directory_hash_cmp (const void *x, const void *y)
{
  return_ISTRING_COMPARE (((struct directory const *) x)->name,
			  ((struct directory const *) y)->name);
}

/* Table of directories hashed by name.  */
static struct hash_table directories;

/* Never have more than this many directories open at once.  */

#define MAX_OPEN_DIRECTORIES 10

static unsigned int open_directories = 0;


/* Hash table of files in each directory.  */

struct dirfile
  {
    char *name;			/* Name of the file.  */
    short length;
    short impossible;		/* This file is impossible.  */
  };

static unsigned long
dirfile_hash_1 (const void *key)
{
  return_ISTRING_HASH_1 (((struct dirfile const *) key)->name);
}

static unsigned long
dirfile_hash_2 (const void *key)
{
  return_ISTRING_HASH_2 (((struct dirfile const *) key)->name);
}

static int
dirfile_hash_cmp (const void *xv, const void *yv)
{
  struct dirfile const *x = ((struct dirfile const *) xv);
  struct dirfile const *y = ((struct dirfile const *) yv);
  int result = x->length - y->length;
  if (result)
    return result;
  return_ISTRING_COMPARE (x->name, y->name);
}

#ifndef	DIRFILE_BUCKETS
#define DIRFILE_BUCKETS 107
#endif

static int dir_contents_file_exists_p PARAMS ((struct directory_contents *dir, char *filename));
static struct directory *find_directory PARAMS ((char *name));

/* Find the directory named NAME and return its `struct directory'.  */

static struct directory *
find_directory (char *name)
{
  register char *p;
  register struct directory *dir;
  register struct directory **dir_slot;
  struct directory dir_key;
  int r;
#ifdef WINDOWS32
  char* w32_path;
  char  fs_label[BUFSIZ];
  char  fs_type[BUFSIZ];
  unsigned long  fs_serno;
  unsigned long  fs_flags;
  unsigned long  fs_len;
#endif
#ifdef VMS
  if ((*name == '.') && (*(name+1) == 0))
    name = "[]";
  else
    name = vmsify (name,1);
#endif

  dir_key.name = name;
  dir_slot = (struct directory **) hash_find_slot (&directories, &dir_key);
  dir = *dir_slot;

  if (HASH_VACANT (dir))
    {
      struct stat st;

      /* The directory was not found.  Create a new entry for it.  */

      p = name + strlen (name);
      dir = (struct directory *) xmalloc (sizeof (struct directory));
      dir->name = savestring (name, p - name);
      hash_insert_at (&directories, dir, dir_slot);
      /* The directory is not in the name hash table.
	 Find its device and inode numbers, and look it up by them.  */

#ifdef WINDOWS32
      /* Remove any trailing '\'.  Windows32 stat fails even on valid
         directories if they end in '\'. */
      if (p[-1] == '\\')
        p[-1] = '\0';
#endif

#ifdef VMS
      r = vmsstat_dir (name, &st);
#else
      EINTRLOOP (r, stat (name, &st));
#endif

#ifdef WINDOWS32
      /* Put back the trailing '\'.  If we don't, we're permanently
         truncating the value!  */
      if (p[-1] == '\0')
        p[-1] = '\\';
#endif

      if (r < 0)
        {
	/* Couldn't stat the directory.  Mark this by
	   setting the `contents' member to a nil pointer.  */
	  dir->contents = 0;
	}
      else
	{
	  /* Search the contents hash table; device and inode are the key.  */

	  struct directory_contents *dc;
	  struct directory_contents **dc_slot;
	  struct directory_contents dc_key;

	  dc_key.dev = st.st_dev;
#ifdef WINDOWS32
	  dc_key.path_key = w32_path = w32ify (name, 1);
	  dc_key.ctime = st.st_ctime;
#else
# ifdef VMS
	  dc_key.ino[0] = st.st_ino[0];
	  dc_key.ino[1] = st.st_ino[1];
	  dc_key.ino[2] = st.st_ino[2];
# else
	  dc_key.ino = st.st_ino;
# endif
#endif
	  dc_slot = (struct directory_contents **) hash_find_slot (&directory_contents, &dc_key);
	  dc = *dc_slot;

	  if (HASH_VACANT (dc))
	    {
	      /* Nope; this really is a directory we haven't seen before.  */

	      dc = (struct directory_contents *)
		xmalloc (sizeof (struct directory_contents));

	      /* Enter it in the contents hash table.  */
	      dc->dev = st.st_dev;
#ifdef WINDOWS32
              dc->path_key = xstrdup (w32_path);
	      dc->ctime = st.st_ctime;
              dc->mtime = st.st_mtime;

              /*
               * NTFS is the only WINDOWS32 filesystem that bumps mtime
               * on a directory when files are added/deleted from
               * a directory.
               */
              w32_path[3] = '\0';
              if (GetVolumeInformation(w32_path,
                     fs_label, sizeof (fs_label),
                     &fs_serno, &fs_len,
                     &fs_flags, fs_type, sizeof (fs_type)) == FALSE)
                dc->fs_flags = FS_UNKNOWN;
              else if (!strcmp(fs_type, "FAT"))
                dc->fs_flags = FS_FAT;
              else if (!strcmp(fs_type, "NTFS"))
                dc->fs_flags = FS_NTFS;
              else
                dc->fs_flags = FS_UNKNOWN;
#else
# ifdef VMS
	      dc->ino[0] = st.st_ino[0];
	      dc->ino[1] = st.st_ino[1];
	      dc->ino[2] = st.st_ino[2];
# else
	      dc->ino = st.st_ino;
# endif
#endif /* WINDOWS32 */
	      hash_insert_at (&directory_contents, dc, dc_slot);
	      ENULLLOOP (dc->dirstream, opendir (name));
	      if (dc->dirstream == 0)
                /* Couldn't open the directory.  Mark this by
                   setting the `files' member to a nil pointer.  */
                dc->dirfiles.ht_vec = 0;
	      else
		{
		  hash_init (&dc->dirfiles, DIRFILE_BUCKETS,
			     dirfile_hash_1, dirfile_hash_2, dirfile_hash_cmp);
		  /* Keep track of how many directories are open.  */
		  ++open_directories;
		  if (open_directories == MAX_OPEN_DIRECTORIES)
		    /* We have too many directories open already.
		       Read the entire directory and then close it.  */
		    (void) dir_contents_file_exists_p (dc, (char *) 0);
		}
	    }

	  /* Point the name-hashed entry for DIR at its contents data.  */
	  dir->contents = dc;
	}
    }

  return dir;
}

/* Return 1 if the name FILENAME is entered in DIR's hash table.
   FILENAME must contain no slashes.  */

static int
dir_contents_file_exists_p (struct directory_contents *dir, char *filename)
{
  unsigned int hash;
  struct dirfile *df;
  struct dirent *d;
#ifdef WINDOWS32
  struct stat st;
  int rehash = 0;
#endif

  if (dir == 0 || dir->dirfiles.ht_vec == 0)
    {
    /* The directory could not be stat'd or opened.  */
      return 0;
    }
#ifdef __MSDOS__
  filename = dosify (filename);
#endif

#ifdef HAVE_CASE_INSENSITIVE_FS
  filename = downcase (filename);
#endif

#ifdef __EMX__
  if (filename != 0)
    _fnlwr (filename); /* lower case for FAT drives */
#endif

#ifdef VMS
  filename = vmsify (filename,0);
#endif

  hash = 0;
  if (filename != 0)
    {
      struct dirfile dirfile_key;

      if (*filename == '\0')
	{
	  /* Checking if the directory exists.  */
	  return 1;
	}
      dirfile_key.name = filename;
      dirfile_key.length = strlen (filename);
      df = (struct dirfile *) hash_find_item (&dir->dirfiles, &dirfile_key);
      if (df)
	{
	  return !df->impossible;
	}
    }

  /* The file was not found in the hashed list.
     Try to read the directory further.  */

  if (dir->dirstream == 0)
    {
#ifdef WINDOWS32
      /*
       * Check to see if directory has changed since last read. FAT
       * filesystems force a rehash always as mtime does not change
       * on directories (ugh!).
       */
      if (dir->path_key)
	{
          if ((dir->fs_flags & FS_FAT) != 0)
	    {
	      dir->mtime = time ((time_t *) 0);
	      rehash = 1;
	    }
	  else if (stat(dir->path_key, &st) == 0 && st.st_mtime > dir->mtime)
	    {
	      /* reset date stamp to show most recent re-process.  */
	      dir->mtime = st.st_mtime;
	      rehash = 1;
	    }

          /* If it has been already read in, all done.  */
	  if (!rehash)
	    return 0;

          /* make sure directory can still be opened; if not return.  */
          dir->dirstream = opendir(dir->path_key);
          if (!dir->dirstream)
            return 0;
	}
      else
#endif
	/* The directory has been all read in.  */
	return 0;
    }

  while (1)
    {
      /* Enter the file in the hash table.  */
      unsigned int len;
      struct dirfile dirfile_key;
      struct dirfile **dirfile_slot;

      ENULLLOOP (d, readdir (dir->dirstream));
      if (d == 0)
        break;

#if defined(VMS) && defined(HAVE_DIRENT_H)
      /* In VMS we get file versions too, which have to be stripped off */
      {
        char *p = strrchr (d->d_name, ';');
        if (p)
          *p = '\0';
      }
#endif
      if (!REAL_DIR_ENTRY (d))
	continue;

      len = NAMLEN (d);
      dirfile_key.name = d->d_name;
      dirfile_key.length = len;
      dirfile_slot = (struct dirfile **) hash_find_slot (&dir->dirfiles, &dirfile_key);
#ifdef WINDOWS32
      /*
       * If re-reading a directory, don't cache files that have
       * already been discovered.
       */
      if (! rehash || HASH_VACANT (*dirfile_slot))
#endif
	{
	  df = (struct dirfile *) xmalloc (sizeof (struct dirfile));
	  df->name = savestring (d->d_name, len);
	  df->length = len;
	  df->impossible = 0;
	  hash_insert_at (&dir->dirfiles, df, dirfile_slot);
	}
      /* Check if the name matches the one we're searching for.  */
      if (filename != 0 && strieq (d->d_name, filename))
	{
	  return 1;
	}
    }

  /* If the directory has been completely read in,
     close the stream and reset the pointer to nil.  */
  if (d == 0)
    {
      --open_directories;
      closedir (dir->dirstream);
      dir->dirstream = 0;
    }
  return 0;
}

/* Return 1 if the name FILENAME in directory DIRNAME
   is entered in the dir hash table.
   FILENAME must contain no slashes.  */

int
dir_file_exists_p (char *dirname, char *filename)
{
  return dir_contents_file_exists_p (find_directory (dirname)->contents,
				     filename);
}

/* Return 1 if the file named NAME exists.  */

int
file_exists_p (char *name)
{
  char *dirend;
  char *dirname;
  char *slash;

#ifndef	NO_ARCHIVES
  if (ar_name (name))
    return ar_member_date (name) != (time_t) -1;
#endif

#ifdef VMS
  dirend = strrchr (name, ']');
  if (dirend == 0)
    dirend = strrchr (name, ':');
  if (dirend == (char *)0)
    return dir_file_exists_p ("[]", name);
#else /* !VMS */
  dirend = strrchr (name, '/');
#ifdef HAVE_DOS_PATHS
  /* Forward and backslashes might be mixed.  We need the rightmost one.  */
  {
    char *bslash = strrchr(name, '\\');
    if (!dirend || bslash > dirend)
      dirend = bslash;
    /* The case of "d:file".  */
    if (!dirend && name[0] && name[1] == ':')
      dirend = name + 1;
  }
#endif /* HAVE_DOS_PATHS */
  if (dirend == 0)
#ifndef _AMIGA
    return dir_file_exists_p (".", name);
#else /* !VMS && !AMIGA */
    return dir_file_exists_p ("", name);
#endif /* AMIGA */
#endif /* VMS */

  slash = dirend;
  if (dirend == name)
    dirname = "/";
  else
    {
#ifdef HAVE_DOS_PATHS
  /* d:/ and d: are *very* different...  */
      if (dirend < name + 3 && name[1] == ':' &&
	  (*dirend == '/' || *dirend == '\\' || *dirend == ':'))
	dirend++;
#endif
      dirname = (char *) alloca (dirend - name + 1);
      bcopy (name, dirname, dirend - name);
      dirname[dirend - name] = '\0';
    }
  return dir_file_exists_p (dirname, slash + 1);
}

/* Mark FILENAME as `impossible' for `file_impossible_p'.
   This means an attempt has been made to search for FILENAME
   as an intermediate file, and it has failed.  */

void
file_impossible (char *filename)
{
  char *dirend;
  register char *p = filename;
  register struct directory *dir;
  register struct dirfile *new;

#ifdef VMS
  dirend = strrchr (p, ']');
  if (dirend == 0)
    dirend = strrchr (p, ':');
  dirend++;
  if (dirend == (char *)1)
    dir = find_directory ("[]");
#else
  dirend = strrchr (p, '/');
# ifdef HAVE_DOS_PATHS
  /* Forward and backslashes might be mixed.  We need the rightmost one.  */
  {
    char *bslash = strrchr(p, '\\');
    if (!dirend || bslash > dirend)
      dirend = bslash;
    /* The case of "d:file".  */
    if (!dirend && p[0] && p[1] == ':')
      dirend = p + 1;
  }
# endif /* HAVE_DOS_PATHS */
  if (dirend == 0)
# ifdef _AMIGA
    dir = find_directory ("");
# else /* !VMS && !AMIGA */
    dir = find_directory (".");
# endif /* AMIGA */
#endif /* VMS */
  else
    {
      char *dirname;
      char *slash = dirend;
      if (dirend == p)
	dirname = "/";
      else
	{
#ifdef HAVE_DOS_PATHS
	  /* d:/ and d: are *very* different...  */
	  if (dirend < p + 3 && p[1] == ':' &&
	      (*dirend == '/' || *dirend == '\\' || *dirend == ':'))
	    dirend++;
#endif
	  dirname = (char *) alloca (dirend - p + 1);
	  bcopy (p, dirname, dirend - p);
	  dirname[dirend - p] = '\0';
	}
      dir = find_directory (dirname);
      filename = p = slash + 1;
    }

  if (dir->contents == 0)
    {
      /* The directory could not be stat'd.  We allocate a contents
	 structure for it, but leave it out of the contents hash table.  */
      dir->contents = (struct directory_contents *)
	xmalloc (sizeof (struct directory_contents));
      bzero ((char *) dir->contents, sizeof (struct directory_contents));
    }

  if (dir->contents->dirfiles.ht_vec == 0)
    {
      hash_init (&dir->contents->dirfiles, DIRFILE_BUCKETS,
		 dirfile_hash_1, dirfile_hash_2, dirfile_hash_cmp);
    }

  /* Make a new entry and put it in the table.  */

  new = (struct dirfile *) xmalloc (sizeof (struct dirfile));
  new->name = xstrdup (filename);
  new->length = strlen (filename);
  new->impossible = 1;
  hash_insert (&dir->contents->dirfiles, new);
}

/* Return nonzero if FILENAME has been marked impossible.  */

int
file_impossible_p (char *filename)
{
  char *dirend;
  register char *p = filename;
  register struct directory_contents *dir;
  register struct dirfile *dirfile;
  struct dirfile dirfile_key;

#ifdef VMS
  dirend = strrchr (filename, ']');
  if (dirend == 0)
    dir = find_directory ("[]")->contents;
#else
  dirend = strrchr (filename, '/');
#ifdef HAVE_DOS_PATHS
  /* Forward and backslashes might be mixed.  We need the rightmost one.  */
  {
    char *bslash = strrchr(filename, '\\');
    if (!dirend || bslash > dirend)
      dirend = bslash;
    /* The case of "d:file".  */
    if (!dirend && filename[0] && filename[1] == ':')
      dirend = filename + 1;
  }
#endif /* HAVE_DOS_PATHS */
  if (dirend == 0)
#ifdef _AMIGA
    dir = find_directory ("")->contents;
#else /* !VMS && !AMIGA */
    dir = find_directory (".")->contents;
#endif /* AMIGA */
#endif /* VMS */
  else
    {
      char *dirname;
      char *slash = dirend;
      if (dirend == filename)
	dirname = "/";
      else
	{
#ifdef HAVE_DOS_PATHS
	  /* d:/ and d: are *very* different...  */
	  if (dirend < filename + 3 && filename[1] == ':' &&
	      (*dirend == '/' || *dirend == '\\' || *dirend == ':'))
	    dirend++;
#endif
	  dirname = (char *) alloca (dirend - filename + 1);
	  bcopy (p, dirname, dirend - p);
	  dirname[dirend - p] = '\0';
	}
      dir = find_directory (dirname)->contents;
      p = filename = slash + 1;
    }

  if (dir == 0 || dir->dirfiles.ht_vec == 0)
    /* There are no files entered for this directory.  */
    return 0;

#ifdef __MSDOS__
  filename = dosify (p);
#endif
#ifdef HAVE_CASE_INSENSITIVE_FS
  filename = downcase (p);
#endif
#ifdef VMS
  filename = vmsify (p, 1);
#endif

  dirfile_key.name = filename;
  dirfile_key.length = strlen (filename);
  dirfile = (struct dirfile *) hash_find_item (&dir->dirfiles, &dirfile_key);
  if (dirfile)
    return dirfile->impossible;

  return 0;
}

/* Return the already allocated name in the
   directory hash table that matches DIR.  */

char *
dir_name (char *dir)
{
  return find_directory (dir)->name;
}

/* Print the data base of directories.  */

void
print_dir_data_base (void)
{
  register unsigned int files;
  register unsigned int impossible;
  register struct directory **dir_slot;
  register struct directory **dir_end;

  puts (_("\n# Directories\n"));

  files = impossible = 0;

  dir_slot = (struct directory **) directories.ht_vec;
  dir_end = dir_slot + directories.ht_size;
  for ( ; dir_slot < dir_end; dir_slot++)
    {
      register struct directory *dir = *dir_slot;
      if (! HASH_VACANT (dir))
	{
	  if (dir->contents == 0)
	    printf (_("# %s: could not be stat'd.\n"), dir->name);
	  else if (dir->contents->dirfiles.ht_vec == 0)
	    {
#ifdef WINDOWS32
	      printf (_("# %s (key %s, mtime %d): could not be opened.\n"),
		      dir->name, dir->contents->path_key,dir->contents->mtime);
#else  /* WINDOWS32 */
#ifdef VMS
	      printf (_("# %s (device %d, inode [%d,%d,%d]): could not be opened.\n"),
		      dir->name, dir->contents->dev,
		      dir->contents->ino[0], dir->contents->ino[1],
		      dir->contents->ino[2]);
#else
	      printf (_("# %s (device %ld, inode %ld): could not be opened.\n"),
		      dir->name, (long int) dir->contents->dev,
		      (long int) dir->contents->ino);
#endif
#endif /* WINDOWS32 */
	    }
	  else
	    {
	      register unsigned int f = 0;
	      register unsigned int im = 0;
	      register struct dirfile **files_slot;
	      register struct dirfile **files_end;

	      files_slot = (struct dirfile **) dir->contents->dirfiles.ht_vec;
	      files_end = files_slot + dir->contents->dirfiles.ht_size;
	      for ( ; files_slot < files_end; files_slot++)
		{
		  register struct dirfile *df = *files_slot;
		  if (! HASH_VACANT (df))
		    {
		      if (df->impossible)
			++im;
		      else
			++f;
		    }
		}
#ifdef WINDOWS32
	      printf (_("# %s (key %s, mtime %d): "),
		      dir->name, dir->contents->path_key, dir->contents->mtime);
#else  /* WINDOWS32 */
#ifdef VMS
	      printf (_("# %s (device %d, inode [%d,%d,%d]): "),
		      dir->name, dir->contents->dev,
		      dir->contents->ino[0], dir->contents->ino[1],
		      dir->contents->ino[2]);
#else
	      printf (_("# %s (device %ld, inode %ld): "),
		      dir->name,
		      (long)dir->contents->dev, (long)dir->contents->ino);
#endif
#endif /* WINDOWS32 */
	      if (f == 0)
		fputs (_("No"), stdout);
	      else
		printf ("%u", f);
	      fputs (_(" files, "), stdout);
	      if (im == 0)
		fputs (_("no"), stdout);
	      else
		printf ("%u", im);
	      fputs (_(" impossibilities"), stdout);
	      if (dir->contents->dirstream == 0)
		puts (".");
	      else
		puts (_(" so far."));
	      files += f;
	      impossible += im;
	    }
	}
    }

  fputs ("\n# ", stdout);
  if (files == 0)
    fputs (_("No"), stdout);
  else
    printf ("%u", files);
  fputs (_(" files, "), stdout);
  if (impossible == 0)
    fputs (_("no"), stdout);
  else
    printf ("%u", impossible);
  printf (_(" impossibilities in %lu directories.\n"), directories.ht_fill);
}

/* Hooks for globbing.  */

#include <glob.h>

/* Structure describing state of iterating through a directory hash table.  */

struct dirstream
  {
    struct directory_contents *contents; /* The directory being read.  */
    struct dirfile **dirfile_slot; /* Current slot in table.  */
  };

/* Forward declarations.  */
static __ptr_t open_dirstream PARAMS ((const char *));
static struct dirent *read_dirstream PARAMS ((__ptr_t));

static __ptr_t
open_dirstream (const char *directory)
{
  struct dirstream *new;
  struct directory *dir = find_directory ((char *)directory);

  if (dir->contents == 0 || dir->contents->dirfiles.ht_vec == 0)
    /* DIR->contents is nil if the directory could not be stat'd.
       DIR->contents->dirfiles is nil if it could not be opened.  */
    return 0;

  /* Read all the contents of the directory now.  There is no benefit
     in being lazy, since glob will want to see every file anyway.  */

  (void) dir_contents_file_exists_p (dir->contents, (char *) 0);

  new = (struct dirstream *) xmalloc (sizeof (struct dirstream));
  new->contents = dir->contents;
  new->dirfile_slot = (struct dirfile **) new->contents->dirfiles.ht_vec;

  return (__ptr_t) new;
}

static struct dirent *
read_dirstream (__ptr_t stream)
{
  struct dirstream *const ds = (struct dirstream *) stream;
  struct directory_contents *dc = ds->contents;
  struct dirfile **dirfile_end = (struct dirfile **) dc->dirfiles.ht_vec + dc->dirfiles.ht_size;
  static char *buf;
  static unsigned int bufsz;

  while (ds->dirfile_slot < dirfile_end)
    {
      register struct dirfile *df = *ds->dirfile_slot++;
      if (! HASH_VACANT (df) && !df->impossible)
	{
	  /* The glob interface wants a `struct dirent',
	     so mock one up.  */
	  struct dirent *d;
	  unsigned int len = df->length + 1;
	  if (sizeof *d - sizeof d->d_name + len > bufsz)
	    {
	      if (buf != 0)
		free (buf);
	      bufsz *= 2;
	      if (sizeof *d - sizeof d->d_name + len > bufsz)
		bufsz = sizeof *d - sizeof d->d_name + len;
	      buf = xmalloc (bufsz);
	    }
	  d = (struct dirent *) buf;
#ifdef __MINGW32__
# if __MINGW32_MAJOR_VERSION < 3 || (__MINGW32_MAJOR_VERSION == 3 && \
				     __MINGW32_MINOR_VERSION == 0)
	  d->d_name = xmalloc(len);
# endif
#endif
	  FAKE_DIR_ENTRY (d);
#ifdef _DIRENT_HAVE_D_NAMLEN
	  d->d_namlen = len - 1;
#endif
#ifdef _DIRENT_HAVE_D_TYPE
	  d->d_type = DT_UNKNOWN;
#endif
	  memcpy (d->d_name, df->name, len);
	  return d;
	}
    }

  return 0;
}

static void
ansi_free (void *p)
{
  if (p)
    free(p);
}

/* On 64 bit ReliantUNIX (5.44 and above) in LFS mode, stat() is actually a
 * macro for stat64().  If stat is a macro, make a local wrapper function to
 * invoke it.
 */
#ifndef stat
# ifndef VMS
extern int stat PARAMS ((const char *path, struct stat *sbuf));
# endif
# define local_stat stat
#else
static int
local_stat (const char *path, struct stat *buf)
{
  int e;

  EINTRLOOP (e, stat (path, buf));
  return e;
}
#endif

void
dir_setup_glob (glob_t *gl)
{
  /* Bogus sunos4 compiler complains (!) about & before functions.  */
  gl->gl_opendir = open_dirstream;
  gl->gl_readdir = read_dirstream;
  gl->gl_closedir = ansi_free;
  gl->gl_stat = local_stat;
  /* We don't bother setting gl_lstat, since glob never calls it.
     The slot is only there for compatibility with 4.4 BSD.  */
}

void
hash_init_directories (void)
{
  hash_init (&directories, DIRECTORY_BUCKETS,
	     directory_hash_1, directory_hash_2, directory_hash_cmp);
  hash_init (&directory_contents, DIRECTORY_BUCKETS,
	     directory_contents_hash_1, directory_contents_hash_2, directory_contents_hash_cmp);
}
