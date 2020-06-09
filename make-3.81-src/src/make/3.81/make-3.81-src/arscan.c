/* Library function for scanning an archive file.
Copyright (C) 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997,
1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006 Free Software Foundation,
Inc.
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

#ifdef HAVE_FCNTL_H
#include <fcntl.h>
#else
#include <sys/file.h>
#endif

#ifndef	NO_ARCHIVES

#ifdef VMS
#include <lbrdef.h>
#include <mhddef.h>
#include <credef.h>
#include <descrip.h>
#include <ctype.h>
#if __DECC
#include <unixlib.h>
#include <lbr$routines.h>
#endif

static void *VMS_lib_idx;

static char *VMS_saved_memname;

static time_t VMS_member_date;

static long int (*VMS_function) ();

static int
VMS_get_member_info (struct dsc$descriptor_s *module, unsigned long *rfa)
{
  int status, i;
  long int fnval;

  time_t val;

  static struct dsc$descriptor_s bufdesc =
    { 0, DSC$K_DTYPE_T, DSC$K_CLASS_S, NULL };

  struct mhddef *mhd;
  char filename[128];

  bufdesc.dsc$a_pointer = filename;
  bufdesc.dsc$w_length = sizeof (filename);

  status = lbr$set_module (&VMS_lib_idx, rfa, &bufdesc,
			   &bufdesc.dsc$w_length, 0);
  if (! (status & 1))
    {
      error (NILF, _("lbr$set_module failed to extract module info, status = %d"),
	     status);

      lbr$close (&VMS_lib_idx);

      return 0;
    }

  mhd = (struct mhddef *) filename;

#ifdef __DECC
  /* John Fowler <jfowler@nyx.net> writes this is needed in his environment,
   * but that decc$fix_time() isn't documented to work this way.  Let me
   * know if this causes problems in other VMS environments.
   */
  val = decc$fix_time (&mhd->mhd$l_datim) + timezone - daylight*3600;
#endif

  for (i = 0; i < module->dsc$w_length; i++)
    filename[i] = _tolower ((unsigned char)module->dsc$a_pointer[i]);

  filename[i] = '\0';

  VMS_member_date = (time_t) -1;

  fnval =
    (*VMS_function) (-1, filename, 0, 0, 0, 0, val, 0, 0, 0,
		     VMS_saved_memname);

  if (fnval)
    {
      VMS_member_date = fnval;
      return 0;
    }
  else
    return 1;
}

/* Takes three arguments ARCHIVE, FUNCTION and ARG.

   Open the archive named ARCHIVE, find its members one by one,
   and for each one call FUNCTION with the following arguments:
     archive file descriptor for reading the data,
     member name,
     member name might be truncated flag,
     member header position in file,
     member data position in file,
     member data size,
     member date,
     member uid,
     member gid,
     member protection mode,
     ARG.

   NOTE: on VMS systems, only name, date, and arg are meaningful!

   The descriptor is poised to read the data of the member
   when FUNCTION is called.  It does not matter how much
   data FUNCTION reads.

   If FUNCTION returns nonzero, we immediately return
   what FUNCTION returned.

   Returns -1 if archive does not exist,
   Returns -2 if archive has invalid format.
   Returns 0 if have scanned successfully.  */

long int
ar_scan (char *archive, long int (*function) PARAMS ((void)), long int arg)
{
  char *p;

  static struct dsc$descriptor_s libdesc =
    { 0, DSC$K_DTYPE_T, DSC$K_CLASS_S, NULL };

  unsigned long func = LBR$C_READ;
  unsigned long type = LBR$C_TYP_UNK;
  unsigned long index = 1;

  int status;

  status = lbr$ini_control (&VMS_lib_idx, &func, &type, 0);

  if (! (status & 1))
    {
      error (NILF, _("lbr$ini_control failed with status = %d"),status);
      return -2;
    }

  libdesc.dsc$a_pointer = archive;
  libdesc.dsc$w_length = strlen (archive);

  status = lbr$open (&VMS_lib_idx, &libdesc, 0, 0, 0, 0, 0);

  if (! (status & 1))
    {
      error (NILF, _("unable to open library `%s' to lookup member `%s'"),
	     archive, (char *)arg);
      return -1;
    }

  VMS_saved_memname = (char *)arg;

  /* For comparison, delete .obj from arg name.  */

  p = strrchr (VMS_saved_memname, '.');
  if (p)
    *p = '\0';

  VMS_function = function;

  VMS_member_date = (time_t) -1;
  lbr$get_index (&VMS_lib_idx, &index, VMS_get_member_info, 0);

  /* Undo the damage.  */
  if (p)
    *p = '.';

  lbr$close (&VMS_lib_idx);

  return VMS_member_date > 0 ? VMS_member_date : 0;
}

#else /* !VMS */

/* SCO Unix's compiler defines both of these.  */
#ifdef	M_UNIX
#undef	M_XENIX
#endif

/* On the sun386i and in System V rel 3, ar.h defines two different archive
   formats depending upon whether you have defined PORTAR (normal) or PORT5AR
   (System V Release 1).  There is no default, one or the other must be defined
   to have a nonzero value.  */

#if (!defined (PORTAR) || PORTAR == 0) && (!defined (PORT5AR) || PORT5AR == 0)
#undef	PORTAR
#ifdef M_XENIX
/* According to Jim Sievert <jas1@rsvl.unisys.com>, for SCO XENIX defining
   PORTAR to 1 gets the wrong archive format, and defining it to 0 gets the
   right one.  */
#define PORTAR 0
#else
#define PORTAR 1
#endif
#endif

/* On AIX, define these symbols to be sure to get both archive formats.
   AIX 4.3 introduced the "big" archive format to support 64-bit object
   files, so on AIX 4.3 systems we need to support both the "normal" and
   "big" archive formats.  An archive's format is indicated in the
   "fl_magic" field of the "FL_HDR" structure.  For a normal archive,
   this field will be the string defined by the AIAMAG symbol.  For a
   "big" archive, it will be the string defined by the AIAMAGBIG symbol
   (at least on AIX it works this way).

   Note: we'll define these symbols regardless of which AIX version
   we're compiling on, but this is okay since we'll use the new symbols
   only if they're present.  */
#ifdef _AIX
# define __AR_SMALL__
# define __AR_BIG__
#endif

#ifndef WINDOWS32
# ifndef __BEOS__
#  include <ar.h>
# else
   /* BeOS 5 doesn't have <ar.h> but has archives in the same format
    * as many other Unices.  This was taken from GNU binutils for BeOS.
    */
#  define ARMAG	"!<arch>\n"	/* String that begins an archive file.  */
#  define SARMAG 8		/* Size of that string.  */
#  define ARFMAG "`\n"		/* String in ar_fmag at end of each header.  */
struct ar_hdr
  {
    char ar_name[16];		/* Member file name, sometimes / terminated. */
    char ar_date[12];		/* File date, decimal seconds since Epoch.  */
    char ar_uid[6], ar_gid[6];	/* User and group IDs, in ASCII decimal.  */
    char ar_mode[8];		/* File mode, in ASCII octal.  */
    char ar_size[10];		/* File size, in ASCII decimal.  */
    char ar_fmag[2];		/* Always contains ARFMAG.  */
  };
# endif
#else
/* These should allow us to read Windows (VC++) libraries (according to Frank
 * Libbrecht <frankl@abzx.belgium.hp.com>)
 */
# include <windows.h>
# include <windef.h>
# include <io.h>
# define ARMAG      IMAGE_ARCHIVE_START
# define SARMAG     IMAGE_ARCHIVE_START_SIZE
# define ar_hdr     _IMAGE_ARCHIVE_MEMBER_HEADER
# define ar_name    Name
# define ar_mode    Mode
# define ar_size    Size
# define ar_date    Date
# define ar_uid     UserID
# define ar_gid     GroupID
#endif

/* Cray's <ar.h> apparently defines this.  */
#ifndef	AR_HDR_SIZE
# define   AR_HDR_SIZE	(sizeof (struct ar_hdr))
#endif

/* Takes three arguments ARCHIVE, FUNCTION and ARG.

   Open the archive named ARCHIVE, find its members one by one,
   and for each one call FUNCTION with the following arguments:
     archive file descriptor for reading the data,
     member name,
     member name might be truncated flag,
     member header position in file,
     member data position in file,
     member data size,
     member date,
     member uid,
     member gid,
     member protection mode,
     ARG.

   The descriptor is poised to read the data of the member
   when FUNCTION is called.  It does not matter how much
   data FUNCTION reads.

   If FUNCTION returns nonzero, we immediately return
   what FUNCTION returned.

   Returns -1 if archive does not exist,
   Returns -2 if archive has invalid format.
   Returns 0 if have scanned successfully.  */

long int
ar_scan (char *archive, long int (*function)(), long int arg)
{
#ifdef AIAMAG
  FL_HDR fl_header;
#ifdef AIAMAGBIG
  int big_archive = 0;
  FL_HDR_BIG fl_header_big;
#endif
#else
  int long_name = 0;
#endif
  char *namemap = 0;
  register int desc = open (archive, O_RDONLY, 0);
  if (desc < 0)
    return -1;
#ifdef SARMAG
  {
    char buf[SARMAG];
    register int nread = read (desc, buf, SARMAG);
    if (nread != SARMAG || bcmp (buf, ARMAG, SARMAG))
      {
	(void) close (desc);
	return -2;
      }
  }
#else
#ifdef AIAMAG
  {
    register int nread = read (desc, (char *) &fl_header, FL_HSZ);

    if (nread != FL_HSZ)
      {
	(void) close (desc);
	return -2;
      }
#ifdef AIAMAGBIG
    /* If this is a "big" archive, then set the flag and
       re-read the header into the "big" structure. */
    if (!bcmp (fl_header.fl_magic, AIAMAGBIG, SAIAMAG))
      {
	big_archive = 1;

	/* seek back to beginning of archive */
	if (lseek (desc, 0, 0) < 0)
	  {
	    (void) close (desc);
	    return -2;
	  }

	/* re-read the header into the "big" structure */
	nread = read (desc, (char *) &fl_header_big, FL_HSZ_BIG);
	if (nread != FL_HSZ_BIG)
	  {
	    (void) close (desc);
	    return -2;
	  }
      }
    else
#endif
       /* Check to make sure this is a "normal" archive. */
      if (bcmp (fl_header.fl_magic, AIAMAG, SAIAMAG))
	{
          (void) close (desc);
          return -2;
	}
  }
#else
  {
#ifndef M_XENIX
    int buf;
#else
    unsigned short int buf;
#endif
    register int nread = read(desc, &buf, sizeof (buf));
    if (nread != sizeof (buf) || buf != ARMAG)
      {
	(void) close (desc);
	return -2;
      }
  }
#endif
#endif

  /* Now find the members one by one.  */
  {
#ifdef SARMAG
    register long int member_offset = SARMAG;
#else
#ifdef AIAMAG
    long int member_offset;
    long int last_member_offset;

#ifdef AIAMAGBIG
    if ( big_archive )
      {
	sscanf (fl_header_big.fl_fstmoff, "%20ld", &member_offset);
	sscanf (fl_header_big.fl_lstmoff, "%20ld", &last_member_offset);
      }
    else
#endif
      {
	sscanf (fl_header.fl_fstmoff, "%12ld", &member_offset);
	sscanf (fl_header.fl_lstmoff, "%12ld", &last_member_offset);
      }

    if (member_offset == 0)
      {
	/* Empty archive.  */
	close (desc);
	return 0;
      }
#else
#ifndef	M_XENIX
    register long int member_offset = sizeof (int);
#else	/* Xenix.  */
    register long int member_offset = sizeof (unsigned short int);
#endif	/* Not Xenix.  */
#endif
#endif

    while (1)
      {
	register int nread;
	struct ar_hdr member_header;
#ifdef AIAMAGBIG
	struct ar_hdr_big member_header_big;
#endif
#ifdef AIAMAG
	char name[256];
	int name_len;
	long int dateval;
	int uidval, gidval;
	long int data_offset;
#else
	char namebuf[sizeof member_header.ar_name + 1];
	char *name;
	int is_namemap;		/* Nonzero if this entry maps long names.  */
#endif
	long int eltsize;
	int eltmode;
	long int fnval;

	if (lseek (desc, member_offset, 0) < 0)
	  {
	    (void) close (desc);
	    return -2;
	  }

#ifdef AIAMAG
#define       AR_MEMHDR_SZ(x) (sizeof(x) - sizeof (x._ar_name))

#ifdef AIAMAGBIG
	if (big_archive)
	  {
	    nread = read (desc, (char *) &member_header_big,
			  AR_MEMHDR_SZ(member_header_big) );

	    if (nread != AR_MEMHDR_SZ(member_header_big))
	      {
		(void) close (desc);
		return -2;
	      }

	    sscanf (member_header_big.ar_namlen, "%4d", &name_len);
	    nread = read (desc, name, name_len);

	    if (nread != name_len)
	      {
		(void) close (desc);
		return -2;
	      }

	    name[name_len] = 0;

	    sscanf (member_header_big.ar_date, "%12ld", &dateval);
	    sscanf (member_header_big.ar_uid, "%12d", &uidval);
	    sscanf (member_header_big.ar_gid, "%12d", &gidval);
	    sscanf (member_header_big.ar_mode, "%12o", &eltmode);
	    sscanf (member_header_big.ar_size, "%20ld", &eltsize);

	    data_offset = (member_offset + AR_MEMHDR_SZ(member_header_big)
			   + name_len + 2);
	  }
	else
#endif
	  {
	    nread = read (desc, (char *) &member_header,
			  AR_MEMHDR_SZ(member_header) );

	    if (nread != AR_MEMHDR_SZ(member_header))
	      {
		(void) close (desc);
		return -2;
	      }

	    sscanf (member_header.ar_namlen, "%4d", &name_len);
	    nread = read (desc, name, name_len);

	    if (nread != name_len)
	      {
		(void) close (desc);
		return -2;
	      }

	    name[name_len] = 0;

	    sscanf (member_header.ar_date, "%12ld", &dateval);
	    sscanf (member_header.ar_uid, "%12d", &uidval);
	    sscanf (member_header.ar_gid, "%12d", &gidval);
	    sscanf (member_header.ar_mode, "%12o", &eltmode);
	    sscanf (member_header.ar_size, "%12ld", &eltsize);

	    data_offset = (member_offset + AR_MEMHDR_SZ(member_header)
			   + name_len + 2);
	  }
	data_offset += data_offset % 2;

	fnval =
	  (*function) (desc, name, 0,
		       member_offset, data_offset, eltsize,
		       dateval, uidval, gidval,
		       eltmode, arg);

#else	/* Not AIAMAG.  */
	nread = read (desc, (char *) &member_header, AR_HDR_SIZE);
	if (nread == 0)
	  /* No data left means end of file; that is OK.  */
	  break;

	if (nread != AR_HDR_SIZE
#if defined(ARFMAG) || defined(ARFZMAG)
	    || (
# ifdef ARFMAG
                bcmp (member_header.ar_fmag, ARFMAG, 2)
# else
                1
# endif
                &&
# ifdef ARFZMAG
                bcmp (member_header.ar_fmag, ARFZMAG, 2)
# else
                1
# endif
               )
#endif
	    )
	  {
	    (void) close (desc);
	    return -2;
	  }

	name = namebuf;
	bcopy (member_header.ar_name, name, sizeof member_header.ar_name);
	{
	  register char *p = name + sizeof member_header.ar_name;
	  do
	    *p = '\0';
	  while (p > name && *--p == ' ');

#ifndef AIAMAG
	  /* If the member name is "//" or "ARFILENAMES/" this may be
	     a list of file name mappings.  The maximum file name
 	     length supported by the standard archive format is 14
 	     characters.  This member will actually always be the
 	     first or second entry in the archive, but we don't check
 	     that.  */
 	  is_namemap = (!strcmp (name, "//")
			|| !strcmp (name, "ARFILENAMES/"));
#endif	/* Not AIAMAG. */
	  /* On some systems, there is a slash after each member name.  */
	  if (*p == '/')
	    *p = '\0';

#ifndef AIAMAG
 	  /* If the member name starts with a space or a slash, this
 	     is an index into the file name mappings (used by GNU ar).
 	     Otherwise if the member name looks like #1/NUMBER the
 	     real member name appears in the element data (used by
 	     4.4BSD).  */
 	  if (! is_namemap
 	      && (name[0] == ' ' || name[0] == '/')
 	      && namemap != 0)
	    {
	      name = namemap + atoi (name + 1);
	      long_name = 1;
	    }
 	  else if (name[0] == '#'
 		   && name[1] == '1'
 		   && name[2] == '/')
 	    {
 	      int namesize = atoi (name + 3);

 	      name = (char *) alloca (namesize + 1);
 	      nread = read (desc, name, namesize);
 	      if (nread != namesize)
 		{
 		  close (desc);
 		  return -2;
 		}
 	      name[namesize] = '\0';

	      long_name = 1;
 	    }
#endif /* Not AIAMAG. */
	}

#ifndef	M_XENIX
	sscanf (member_header.ar_mode, "%o", &eltmode);
	eltsize = atol (member_header.ar_size);
#else	/* Xenix.  */
	eltmode = (unsigned short int) member_header.ar_mode;
	eltsize = member_header.ar_size;
#endif	/* Not Xenix.  */

	fnval =
	  (*function) (desc, name, ! long_name, member_offset,
		       member_offset + AR_HDR_SIZE, eltsize,
#ifndef	M_XENIX
		       atol (member_header.ar_date),
		       atoi (member_header.ar_uid),
		       atoi (member_header.ar_gid),
#else	/* Xenix.  */
		       member_header.ar_date,
		       member_header.ar_uid,
		       member_header.ar_gid,
#endif	/* Not Xenix.  */
		       eltmode, arg);

#endif  /* AIAMAG.  */

	if (fnval)
	  {
	    (void) close (desc);
	    return fnval;
	  }

#ifdef AIAMAG
	if (member_offset == last_member_offset)
	  /* End of the chain.  */
	  break;

#ifdef AIAMAGBIG
	if (big_archive)
          sscanf (member_header_big.ar_nxtmem, "%20ld", &member_offset);
	else
#endif
	  sscanf (member_header.ar_nxtmem, "%12ld", &member_offset);

	if (lseek (desc, member_offset, 0) != member_offset)
	  {
	    (void) close (desc);
	    return -2;
	  }
#else

 	/* If this member maps archive names, we must read it in.  The
 	   name map will always precede any members whose names must
 	   be mapped.  */
	if (is_namemap)
 	  {
 	    char *clear;
 	    char *limit;

 	    namemap = (char *) alloca (eltsize);
 	    nread = read (desc, namemap, eltsize);
 	    if (nread != eltsize)
 	      {
 		(void) close (desc);
 		return -2;
 	      }

 	    /* The names are separated by newlines.  Some formats have
 	       a trailing slash.  Null terminate the strings for
 	       convenience.  */
 	    limit = namemap + eltsize;
 	    for (clear = namemap; clear < limit; clear++)
 	      {
 		if (*clear == '\n')
 		  {
 		    *clear = '\0';
 		    if (clear[-1] == '/')
 		      clear[-1] = '\0';
 		  }
 	      }

	    is_namemap = 0;
 	  }

	member_offset += AR_HDR_SIZE + eltsize;
	if (member_offset % 2 != 0)
	  member_offset++;
#endif
      }
  }

  close (desc);
  return 0;
}
#endif /* !VMS */

/* Return nonzero iff NAME matches MEM.
   If TRUNCATED is nonzero, MEM may be truncated to
   sizeof (struct ar_hdr.ar_name) - 1.  */

int
ar_name_equal (char *name, char *mem, int truncated)
{
  char *p;

  p = strrchr (name, '/');
  if (p != 0)
    name = p + 1;

#ifndef VMS
  if (truncated)
    {
#ifdef AIAMAG
      /* TRUNCATED should never be set on this system.  */
      abort ();
#else
      struct ar_hdr hdr;
#if !defined (__hpux) && !defined (cray)
      return strneq (name, mem, sizeof(hdr.ar_name) - 1);
#else
      return strneq (name, mem, sizeof(hdr.ar_name) - 2);
#endif /* !__hpux && !cray */
#endif /* !AIAMAG */
    }
#endif /* !VMS */

  return !strcmp (name, mem);
}

#ifndef VMS
/* ARGSUSED */
static long int
ar_member_pos (int desc UNUSED, char *mem, int truncated,
	       long int hdrpos, long int datapos UNUSED, long int size UNUSED,
               long int date UNUSED, int uid UNUSED, int gid UNUSED,
               int mode UNUSED, char *name)
{
  if (!ar_name_equal (name, mem, truncated))
    return 0;
  return hdrpos;
}

/* Set date of member MEMNAME in archive ARNAME to current time.
   Returns 0 if successful,
   -1 if file ARNAME does not exist,
   -2 if not a valid archive,
   -3 if other random system call error (including file read-only),
   1 if valid but member MEMNAME does not exist.  */

int
ar_member_touch (char *arname, char *memname)
{
  long int pos = ar_scan (arname, ar_member_pos, (long int) memname);
  int fd;
  struct ar_hdr ar_hdr;
  int i;
  unsigned int ui;
  struct stat statbuf;

  if (pos < 0)
    return (int) pos;
  if (!pos)
    return 1;

  fd = open (arname, O_RDWR, 0666);
  if (fd < 0)
    return -3;
  /* Read in this member's header */
  if (lseek (fd, pos, 0) < 0)
    goto lose;
  if (AR_HDR_SIZE != read (fd, (char *) &ar_hdr, AR_HDR_SIZE))
    goto lose;
  /* Write back the header, thus touching the archive file.  */
  if (lseek (fd, pos, 0) < 0)
    goto lose;
  if (AR_HDR_SIZE != write (fd, (char *) &ar_hdr, AR_HDR_SIZE))
    goto lose;
  /* The file's mtime is the time we we want.  */
  EINTRLOOP (i, fstat (fd, &statbuf));
  if (i < 0)
    goto lose;
#if defined(ARFMAG) || defined(ARFZMAG) || defined(AIAMAG) || defined(WINDOWS32)
  /* Advance member's time to that time */
  for (ui = 0; ui < sizeof ar_hdr.ar_date; ui++)
    ar_hdr.ar_date[ui] = ' ';
  sprintf (ar_hdr.ar_date, "%ld", (long int) statbuf.st_mtime);
#ifdef AIAMAG
  ar_hdr.ar_date[strlen(ar_hdr.ar_date)] = ' ';
#endif
#else
  ar_hdr.ar_date = statbuf.st_mtime;
#endif
  /* Write back this member's header */
  if (lseek (fd, pos, 0) < 0)
    goto lose;
  if (AR_HDR_SIZE != write (fd, (char *) &ar_hdr, AR_HDR_SIZE))
    goto lose;
  close (fd);
  return 0;

 lose:
  i = errno;
  close (fd);
  errno = i;
  return -3;
}
#endif

#ifdef TEST

long int
describe_member (int desc, char *name, int truncated,
		 long int hdrpos, long int datapos, long int size,
                 long int date, int uid, int gid, int mode)
{
  extern char *ctime ();

  printf (_("Member `%s'%s: %ld bytes at %ld (%ld).\n"),
	  name, truncated ? _(" (name might be truncated)") : "",
	  size, hdrpos, datapos);
  printf (_("  Date %s"), ctime (&date));
  printf (_("  uid = %d, gid = %d, mode = 0%o.\n"), uid, gid, mode);

  return 0;
}

int
main (int argc, char **argv)
{
  ar_scan (argv[1], describe_member);
  return 0;
}

#endif	/* TEST.  */
#endif	/* NO_ARCHIVES.  */
