/* VMS functions
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

#include "make.h"
#include "debug.h"
#include "job.h"

#ifdef __DECC
#include <starlet.h>
#endif
#include <descrip.h>
#include <rms.h>
#include <iodef.h>
#include <atrdef.h>
#include <fibdef.h>
#include "vmsdir.h"

#ifdef HAVE_VMSDIR_H

DIR *
opendir (char *dspec)
{
  struct DIR *dir  = (struct DIR *)xmalloc (sizeof (struct DIR));
  struct NAM *dnam = (struct NAM *)xmalloc (sizeof (struct NAM));
  struct FAB *dfab = &dir->fab;
  char *searchspec = (char *)xmalloc (MAXNAMLEN + 1);

  memset (dir, 0, sizeof *dir);

  *dfab = cc$rms_fab;
  *dnam = cc$rms_nam;
  sprintf (searchspec, "%s*.*;", dspec);

  dfab->fab$l_fna = searchspec;
  dfab->fab$b_fns = strlen (searchspec);
  dfab->fab$l_nam = dnam;

  *dnam = cc$rms_nam;
  dnam->nam$l_esa = searchspec;
  dnam->nam$b_ess = MAXNAMLEN;

  if (! (sys$parse (dfab) & 1))
    {
      free (dir);
      free (dnam);
      free (searchspec);
      return (NULL);
    }

  return dir;
}

#define uppercasify(str) \
  do \
    { \
      char *tmp; \
      for (tmp = (str); *tmp != '\0'; tmp++) \
        if (islower ((unsigned char)*tmp)) \
          *tmp = toupper ((unsigned char)*tmp); \
    } \
  while (0)

struct direct *
readdir (DIR *dir)
{
  struct FAB *dfab = &dir->fab;
  struct NAM *dnam = (struct NAM *)(dfab->fab$l_nam);
  struct direct *dentry = &dir->dir;
  int i;

  memset (dentry, 0, sizeof *dentry);

  dnam->nam$l_rsa = dir->d_result;
  dnam->nam$b_rss = MAXNAMLEN;

  DB (DB_VERBOSE, ("."));

  if (!((i = sys$search (dfab)) & 1))
    {
      DB (DB_VERBOSE, (_("sys$search failed with %d\n"), i));
      return (NULL);
    }

  dentry->d_off = 0;
  if (dnam->nam$w_fid == 0)
    dentry->d_fileno = 1;
  else
    dentry->d_fileno = dnam->nam$w_fid[0] + (dnam->nam$w_fid[1] << 16);

  dentry->d_reclen = sizeof (struct direct);
  dentry->d_namlen = dnam->nam$b_name + dnam->nam$b_type;
  strncpy (dentry->d_name, dnam->nam$l_name, dentry->d_namlen);
  dentry->d_name[dentry->d_namlen] = '\0';

#ifdef HAVE_CASE_INSENSITIVE_FS
  uppercasify (dentry->d_name);
#endif

  return (dentry);
}

int
closedir (DIR *dir)
{
  if (dir != NULL)
    {
      struct FAB *dfab = &dir->fab;
      struct NAM *dnam = (struct NAM *)(dfab->fab$l_nam);
      if (dnam != NULL)
	free (dnam->nam$l_esa);
      free (dnam);
      free (dir);
    }

  return 0;
}
#endif /* compiled for OpenVMS prior to V7.x */

char *
getwd (char *cwd)
{
  static char buf[512];

  if (cwd)
    return (getcwd (cwd, 512));
  else
    return (getcwd (buf, 512));
}

int
vms_stat (char *name, struct stat *buf)
{
  int status;
  int i;

  static struct FAB Fab;
  static struct NAM Nam;
  static struct fibdef Fib;	/* short fib */
  static struct dsc$descriptor FibDesc =
  { sizeof (Fib), DSC$K_DTYPE_Z, DSC$K_CLASS_S, (char *) &Fib };
  static struct dsc$descriptor_s DevDesc =
  { 0, DSC$K_DTYPE_T, DSC$K_CLASS_S, &Nam.nam$t_dvi[1] };
  static char EName[NAM$C_MAXRSS];
  static char RName[NAM$C_MAXRSS];
  static struct dsc$descriptor_s FileName =
  { 0, DSC$K_DTYPE_T, DSC$K_CLASS_S, 0 };
  static struct dsc$descriptor_s string =
  { 0, DSC$K_DTYPE_T, DSC$K_CLASS_S, 0 };
  static unsigned long Rdate[2];
  static unsigned long Cdate[2];
  static struct atrdef Atr[] =
  {
#if defined(VAX)
    /* Revision date */
    { sizeof (Rdate), ATR$C_REVDATE, (unsigned int) &Rdate[0] },
    /* Creation date */
    { sizeof (Cdate), ATR$C_CREDATE, (unsigned int) &Cdate[0] },
#else
    /* Revision date */
    { sizeof (Rdate), ATR$C_REVDATE, &Rdate[0] },
    /* Creation date */
    { sizeof (Cdate), ATR$C_CREDATE, &Cdate[0]},
#endif
    { 0, 0, 0 }
  };
  static short int DevChan;
  static short int iosb[4];

  name = vmsify (name, 0);

  /* initialize RMS structures, we need a NAM to retrieve the FID */
  Fab = cc$rms_fab;
  Fab.fab$l_fna = name;		/* name of file */
  Fab.fab$b_fns = strlen (name);
  Fab.fab$l_nam = &Nam;		/* FAB has an associated NAM */

  Nam = cc$rms_nam;
  Nam.nam$l_esa = EName;	/* expanded filename */
  Nam.nam$b_ess = sizeof (EName);
  Nam.nam$l_rsa = RName;	/* resultant filename */
  Nam.nam$b_rss = sizeof (RName);

  /* do $PARSE and $SEARCH here */
  status = sys$parse (&Fab);
  if (!(status & 1))
    return -1;

  DevDesc.dsc$w_length = Nam.nam$t_dvi[0];
  status = sys$assign (&DevDesc, &DevChan, 0, 0);
  if (!(status & 1))
    return -1;

  FileName.dsc$a_pointer = Nam.nam$l_name;
  FileName.dsc$w_length = Nam.nam$b_name + Nam.nam$b_type + Nam.nam$b_ver;

  /* Initialize the FIB */
  for (i = 0; i < 3; i++)
    {
#ifndef __VAXC
      Fib.fib$w_fid[i] = Nam.nam$w_fid[i];
      Fib.fib$w_did[i] = Nam.nam$w_did[i];
#else
      Fib.fib$r_fid_overlay.fib$w_fid[i] = Nam.nam$w_fid[i];
      Fib.fib$r_did_overlay.fib$w_did[i] = Nam.nam$w_did[i];
#endif
    }

  status = sys$qiow (0, DevChan, IO$_ACCESS, &iosb, 0, 0,
		     &FibDesc, &FileName, 0, 0, &Atr, 0);
  sys$dassgn (DevChan);
  if (!(status & 1))
    return -1;
  status = iosb[0];
  if (!(status & 1))
    return -1;

  status = stat (name, buf);
  if (status)
    return -1;

  buf->st_mtime = ((Rdate[0] >> 24) & 0xff) + ((Rdate[1] << 8) & 0xffffff00);
  buf->st_ctime = ((Cdate[0] >> 24) & 0xff) + ((Cdate[1] << 8) & 0xffffff00);

  return 0;
}

char *
cvt_time (unsigned long tval)
{
  static long int date[2];
  static char str[27];
  static struct dsc$descriptor date_str =
  { 26, DSC$K_DTYPE_T, DSC$K_CLASS_S, str };

  date[0] = (tval & 0xff) << 24;
  date[1] = ((tval >> 8) & 0xffffff);

  if ((date[0] == 0) && (date[1] == 0))
    return ("never");

  sys$asctim (0, &date_str, date, 0);
  str[26] = '\0';

  return (str);
}

int
strcmpi (const char *s1, const char *s2)
{
  while (*s1 != '\0' && toupper(*s1) == toupper(*s2))
    {
      s1++;
      s2++;
    }

  return toupper(*(unsigned char *) s1) - toupper(*(unsigned char *) s2);
}
