/* Get the system load averages.
Copyright (C) 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994,
1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006 Free
Software Foundation, Inc.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; see the file COPYING.  If not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.  */

/* Compile-time symbols that this file uses:

   HAVE_PSTAT_GETDYNAMIC	Define this if your system has the
                                pstat_getdynamic function.  I think it
				is unique to HPUX9.  The best way to get the
				definition is through the AC_FUNC_GETLOADAVG
				macro that comes with autoconf 2.13 or newer.
				If that isn't an option, then just put
				AC_CHECK_FUNCS(pstat_getdynamic) in your
				configure.in file.
   FIXUP_KERNEL_SYMBOL_ADDR()	Adjust address in returned struct nlist.
   KERNEL_FILE			Pathname of the kernel to nlist.
   LDAV_CVT()			Scale the load average from the kernel.
				Returns a double.
   LDAV_SYMBOL			Name of kernel symbol giving load average.
   LOAD_AVE_TYPE		Type of the load average array in the kernel.
				Must be defined unless one of
				apollo, DGUX, NeXT, or UMAX is defined;
                                or we have libkstat;
				otherwise, no load average is available.
   NLIST_STRUCT			Include nlist.h, not a.out.h, and
				the nlist n_name element is a pointer,
				not an array.
   HAVE_STRUCT_NLIST_N_UN_N_NAME struct nlist has an n_un member, not n_name.
   LINUX_LDAV_FILE		[__linux__]: File containing load averages.

   Specific system predefines this file uses, aside from setting
   default values if not emacs:

   apollo
   BSD				Real BSD, not just BSD-like.
   convex
   DGUX
   eunice			UNIX emulator under VMS.
   hpux
   __MSDOS__			No-op for MSDOS.
   NeXT
   sgi
   sequent			Sequent Dynix 3.x.x (BSD)
   _SEQUENT_			Sequent DYNIX/ptx 1.x.x (SYSV)
   sony_news                    NEWS-OS (works at least for 4.1C)
   UMAX
   UMAX4_3
   VMS
   WINDOWS32			No-op for Windows95/NT.
   __linux__			Linux: assumes /proc filesystem mounted.
   				Support from Michael K. Johnson.
   __NetBSD__			NetBSD: assumes /kern filesystem mounted.

   In addition, to avoid nesting many #ifdefs, we internally set
   LDAV_DONE to indicate that the load average has been computed.

   We also #define LDAV_PRIVILEGED if a program will require
   special installation to be able to call getloadavg.  */

/* This should always be first.  */
#ifdef HAVE_CONFIG_H
# include <config.h>
#endif

#include <sys/types.h>

/* Both the Emacs and non-Emacs sections want this.  Some
   configuration files' definitions for the LOAD_AVE_CVT macro (like
   sparc.h's) use macros like FSCALE, defined here.  */
#if defined (unix) || defined (__unix)
# include <sys/param.h>
#endif


/* Exclude all the code except the test program at the end
   if the system has its own `getloadavg' function.

   The declaration of `errno' is needed by the test program
   as well as the function itself, so it comes first.  */

#include <errno.h>

#ifndef errno
extern int errno;
#endif

#if HAVE_LOCALE_H
# include <locale.h>
#endif
#if !HAVE_SETLOCALE
# define setlocale(Category, Locale) /* empty */
#endif

#ifndef HAVE_GETLOADAVG


/* The existing Emacs configuration files define a macro called
   LOAD_AVE_CVT, which accepts a value of type LOAD_AVE_TYPE, and
   returns the load average multiplied by 100.  What we actually want
   is a macro called LDAV_CVT, which returns the load average as an
   unmultiplied double.

   For backwards compatibility, we'll define LDAV_CVT in terms of
   LOAD_AVE_CVT, but future machine config files should just define
   LDAV_CVT directly.  */

# if !defined(LDAV_CVT) && defined(LOAD_AVE_CVT)
#  define LDAV_CVT(n) (LOAD_AVE_CVT (n) / 100.0)
# endif

# if !defined (BSD) && defined (ultrix)
/* Ultrix behaves like BSD on Vaxen.  */
#  define BSD
# endif

# ifdef NeXT
/* NeXT in the 2.{0,1,2} releases defines BSD in <sys/param.h>, which
   conflicts with the definition understood in this file, that this
   really is BSD. */
#  undef BSD

/* NeXT defines FSCALE in <sys/param.h>.  However, we take FSCALE being
   defined to mean that the nlist method should be used, which is not true.  */
#  undef FSCALE
# endif

/* Same issues as for NeXT apply to the HURD-based GNU system.  */
# ifdef __GNU__
#  undef BSD
#  undef FSCALE
# endif /* __GNU__ */

/* Set values that are different from the defaults, which are
   set a little farther down with #ifndef.  */


/* Some shorthands.  */

# if defined (HPUX) && !defined (hpux)
#  define hpux
# endif

# if defined (__hpux) && !defined (hpux)
#  define hpux
# endif

# if defined (__sun) && !defined (sun)
#  define sun
# endif

# if defined(hp300) && !defined(hpux)
#  define MORE_BSD
# endif

# if defined(ultrix) && defined(mips)
#  define decstation
# endif

# if defined (__SVR4) && !defined (SVR4)
#  define SVR4
# endif

# if (defined(sun) && defined(SVR4)) || defined (SOLARIS2)
#  define SUNOS_5
# endif

# if defined (__osf__) && (defined (__alpha) || defined (__alpha__))
#  define OSF_ALPHA
#  include <sys/mbuf.h>
#  include <sys/socket.h>
#  include <net/route.h>
#  include <sys/table.h>
# endif

# if defined (__osf__) && (defined (mips) || defined (__mips__))
#  define OSF_MIPS
#  include <sys/table.h>
# endif

/* UTek's /bin/cc on the 4300 has no architecture specific cpp define by
   default, but _MACH_IND_SYS_TYPES is defined in <sys/types.h>.  Combine
   that with a couple of other things and we'll have a unique match.  */
# if !defined (tek4300) && defined (unix) && defined (m68k) && defined (mc68000) && defined (mc68020) && defined (_MACH_IND_SYS_TYPES)
#  define tek4300			/* Define by emacs, but not by other users.  */
# endif

/* AC_FUNC_GETLOADAVG thinks QNX is SVR4, but it isn't. */
# if defined(__QNX__)
#  undef SVR4
# endif

/* VAX C can't handle multi-line #ifs, or lines longer than 256 chars.  */
# ifndef LOAD_AVE_TYPE

#  ifdef MORE_BSD
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef sun
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef decstation
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef _SEQUENT_
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef sgi
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef SVR4
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef sony_news
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef sequent
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef OSF_ALPHA
#   define LOAD_AVE_TYPE long
#  endif

#  if defined (ardent) && defined (titan)
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef tek4300
#   define LOAD_AVE_TYPE long
#  endif

#  if defined(alliant) && defined(i860) /* Alliant FX/2800 */
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef _AIX
#   define LOAD_AVE_TYPE long
#  endif

#  ifdef convex
#   define LOAD_AVE_TYPE double
#   ifndef LDAV_CVT
#    define LDAV_CVT(n) (n)
#   endif
#  endif

# endif /* No LOAD_AVE_TYPE.  */

# ifdef OSF_ALPHA
/* <sys/param.h> defines an incorrect value for FSCALE on Alpha OSF/1,
   according to ghazi@noc.rutgers.edu.  */
#  undef FSCALE
#  define FSCALE 1024.0
# endif

# if defined(alliant) && defined(i860) /* Alliant FX/2800 */
/* <sys/param.h> defines an incorrect value for FSCALE on an
   Alliant FX/2800 Concentrix 2.2, according to ghazi@noc.rutgers.edu.  */
#  undef FSCALE
#  define FSCALE 100.0
# endif


# ifndef	FSCALE

/* SunOS and some others define FSCALE in sys/param.h.  */

#  ifdef MORE_BSD
#   define FSCALE 2048.0
#  endif

#  if defined(MIPS) || defined(SVR4) || defined(decstation)
#   define FSCALE 256
#  endif

#  if defined (sgi) || defined (sequent)
/* Sometimes both MIPS and sgi are defined, so FSCALE was just defined
   above under #ifdef MIPS.  But we want the sgi value.  */
#   undef FSCALE
#   define	FSCALE 1000.0
#  endif

#  if defined (ardent) && defined (titan)
#   define FSCALE 65536.0
#  endif

#  ifdef tek4300
#   define FSCALE 100.0
#  endif

#  ifdef _AIX
#   define FSCALE 65536.0
#  endif

# endif	/* Not FSCALE.  */

# if !defined (LDAV_CVT) && defined (FSCALE)
#  define	LDAV_CVT(n) (((double) (n)) / FSCALE)
# endif


# if defined(sgi) || (defined(mips) && !defined(BSD))
#  define FIXUP_KERNEL_SYMBOL_ADDR(nl) ((nl)[0].n_value &= ~(1 << 31))
# endif


# if !defined (KERNEL_FILE) && defined (sequent)
#  define KERNEL_FILE "/dynix"
# endif

# if !defined (KERNEL_FILE) && defined (hpux)
#  define KERNEL_FILE "/hp-ux"
# endif

# if !defined(KERNEL_FILE) && (defined(_SEQUENT_) || defined(MIPS) || defined(SVR4) || defined(ISC) || defined (sgi) || (defined (ardent) && defined (titan)))
#  define KERNEL_FILE "/unix"
# endif


# if !defined (LDAV_SYMBOL) && defined (alliant)
#  define LDAV_SYMBOL "_Loadavg"
# endif

# if !defined(LDAV_SYMBOL) && ((defined(hpux) && !defined(hp9000s300)) || defined(_SEQUENT_) || defined(SVR4) || defined(ISC) || defined(sgi) || (defined (ardent) && defined (titan)) || defined (_AIX))
#  define LDAV_SYMBOL "avenrun"
# endif

# ifdef HAVE_UNISTD_H
#  include <unistd.h>
# endif

# include <stdio.h>

/* LOAD_AVE_TYPE should only get defined if we're going to use the
   nlist method.  */
# if !defined(LOAD_AVE_TYPE) && (defined(BSD) || defined(LDAV_CVT) || defined(KERNEL_FILE) || defined(LDAV_SYMBOL)) && !defined(__riscos__)
#  define LOAD_AVE_TYPE double
# endif

# ifdef LOAD_AVE_TYPE

#  ifndef VMS
#   ifndef __linux__
#    ifdef HAVE_NLIST_H
#     include <nlist.h>
#    else
#     include <a.out.h>
#    endif

#    ifdef SUNOS_5
#     include <fcntl.h>
#     include <kvm.h>
#     include <kstat.h>
#    endif

#    if defined (hpux) && defined (HAVE_PSTAT_GETDYNAMIC)
#     include <sys/pstat.h>
#    endif

#    ifndef KERNEL_FILE
#     define KERNEL_FILE "/vmunix"
#    endif /* KERNEL_FILE */

#    ifndef LDAV_SYMBOL
#     define LDAV_SYMBOL "_avenrun"
#    endif /* LDAV_SYMBOL */
#   endif /* __linux__ */

#  else /* VMS */

#   ifndef eunice
#    include <iodef.h>
#    include <descrip.h>
#   else /* eunice */
#    include <vms/iodef.h>
#   endif /* eunice */
#  endif /* VMS */

#  ifndef LDAV_CVT
#   define LDAV_CVT(n) ((double) (n))
#  endif /* !LDAV_CVT */

# endif /* LOAD_AVE_TYPE */

# if defined(__GNU__) && !defined (NeXT)
/* Note that NeXT Openstep defines __GNU__ even though it should not.  */
/* GNU system acts much like NeXT, for load average purposes,
   but not exactly.  */
#  define NeXT
#  define host_self mach_host_self
# endif

# ifdef NeXT
#  ifdef HAVE_MACH_MACH_H
#   include <mach/mach.h>
#  else
#   include <mach.h>
#  endif
# endif /* NeXT */

# ifdef sgi
#  include <sys/sysmp.h>
# endif /* sgi */

# ifdef UMAX
#  include <stdio.h>
#  include <signal.h>
#  include <sys/time.h>
#  include <sys/wait.h>
#  include <sys/syscall.h>

#  ifdef UMAX_43
#   include <machine/cpu.h>
#   include <inq_stats/statistics.h>
#   include <inq_stats/sysstats.h>
#   include <inq_stats/cpustats.h>
#   include <inq_stats/procstats.h>
#  else /* Not UMAX_43.  */
#   include <sys/sysdefs.h>
#   include <sys/statistics.h>
#   include <sys/sysstats.h>
#   include <sys/cpudefs.h>
#   include <sys/cpustats.h>
#   include <sys/procstats.h>
#  endif /* Not UMAX_43.  */
# endif /* UMAX */

# ifdef DGUX
#  include <sys/dg_sys_info.h>
# endif

# if defined(HAVE_FCNTL_H) || defined(_POSIX_VERSION)
#  include <fcntl.h>
# else
#  include <sys/file.h>
# endif


/* Avoid static vars inside a function since in HPUX they dump as pure.  */

# ifdef NeXT
static processor_set_t default_set;
static int getloadavg_initialized;
# endif /* NeXT */

# ifdef UMAX
static unsigned int cpus = 0;
static unsigned int samples;
# endif /* UMAX */

# ifdef DGUX
static struct dg_sys_info_load_info load_info;	/* what-a-mouthful! */
# endif /* DGUX */

#if !defined(HAVE_LIBKSTAT) && defined(LOAD_AVE_TYPE)
/* File descriptor open to /dev/kmem or VMS load ave driver.  */
static int channel;
/* Nonzero iff channel is valid.  */
static int getloadavg_initialized;
/* Offset in kmem to seek to read load average, or 0 means invalid.  */
static long offset;

#if !defined(VMS) && !defined(sgi) && !defined(__linux__)
static struct nlist nl[2];
#endif /* Not VMS or sgi */

#ifdef SUNOS_5
static kvm_t *kd;
#endif /* SUNOS_5 */

#endif /* LOAD_AVE_TYPE && !HAVE_LIBKSTAT */

/* Put the 1 minute, 5 minute and 15 minute load averages
   into the first NELEM elements of LOADAVG.
   Return the number written (never more than 3, but may be less than NELEM),
   or -1 if an error occurred.  */

int
getloadavg (double loadavg[], int nelem)
{
  int elem = 0;			/* Return value.  */

# ifdef NO_GET_LOAD_AVG
#  define LDAV_DONE
  /* Set errno to zero to indicate that there was no particular error;
     this function just can't work at all on this system.  */
  errno = 0;
  elem = -1;
# endif

# if !defined (LDAV_DONE) && defined (HAVE_LIBKSTAT)
/* Use libkstat because we don't have to be root.  */
#  define LDAV_DONE
  kstat_ctl_t *kc;
  kstat_t *ksp;
  kstat_named_t *kn;

  kc = kstat_open ();
  if (kc == 0)
    return -1;
  ksp = kstat_lookup (kc, "unix", 0, "system_misc");
  if (ksp == 0 )
    return -1;
  if (kstat_read (kc, ksp, 0) == -1)
    return -1;


  kn = kstat_data_lookup (ksp, "avenrun_1min");
  if (kn == 0)
    {
      /* Return -1 if no load average information is available.  */
      nelem = 0;
      elem = -1;
    }

  if (nelem >= 1)
    loadavg[elem++] = (double) kn->value.ul/FSCALE;

  if (nelem >= 2)
    {
      kn = kstat_data_lookup (ksp, "avenrun_5min");
      if (kn != 0)
	{
	  loadavg[elem++] = (double) kn->value.ul/FSCALE;

	  if (nelem >= 3)
	    {
	      kn = kstat_data_lookup (ksp, "avenrun_15min");
	      if (kn != 0)
		loadavg[elem++] = (double) kn->value.ul/FSCALE;
	    }
	}
    }

  kstat_close (kc);
# endif /* HAVE_LIBKSTAT */

# if !defined (LDAV_DONE) && defined (hpux) && defined (HAVE_PSTAT_GETDYNAMIC)
/* Use pstat_getdynamic() because we don't have to be root.  */
#  define LDAV_DONE
#  undef LOAD_AVE_TYPE

  struct pst_dynamic dyn_info;
  if (pstat_getdynamic (&dyn_info, sizeof (dyn_info), 0, 0) < 0)
    return -1;
  if (nelem > 0)
    loadavg[elem++] = dyn_info.psd_avg_1_min;
  if (nelem > 1)
    loadavg[elem++] = dyn_info.psd_avg_5_min;
  if (nelem > 2)
    loadavg[elem++] = dyn_info.psd_avg_15_min;

# endif /* hpux && HAVE_PSTAT_GETDYNAMIC */

# if !defined (LDAV_DONE) && defined (__linux__)
#  define LDAV_DONE
#  undef LOAD_AVE_TYPE

#  ifndef LINUX_LDAV_FILE
#   define LINUX_LDAV_FILE "/proc/loadavg"
#  endif

  char ldavgbuf[40];
  double load_ave[3];
  int fd, count;

  fd = open (LINUX_LDAV_FILE, O_RDONLY);
  if (fd == -1)
    return -1;
  count = read (fd, ldavgbuf, 40);
  (void) close (fd);
  if (count <= 0)
    return -1;

  /* The following sscanf must use the C locale.  */
  setlocale (LC_NUMERIC, "C");
  count = sscanf (ldavgbuf, "%lf %lf %lf",
		  &load_ave[0], &load_ave[1], &load_ave[2]);
  setlocale (LC_NUMERIC, "");
  if (count < 1)
    return -1;

  for (elem = 0; elem < nelem && elem < count; elem++)
    loadavg[elem] = load_ave[elem];

  return elem;

# endif /* __linux__ */

# if !defined (LDAV_DONE) && defined (__NetBSD__)
#  define LDAV_DONE
#  undef LOAD_AVE_TYPE

#  ifndef NETBSD_LDAV_FILE
#   define NETBSD_LDAV_FILE "/kern/loadavg"
#  endif

  unsigned long int load_ave[3], scale;
  int count;
  FILE *fp;

  fp = fopen (NETBSD_LDAV_FILE, "r");
  if (fp == NULL)
    return -1;
  count = fscanf (fp, "%lu %lu %lu %lu\n",
		  &load_ave[0], &load_ave[1], &load_ave[2],
		  &scale);
  (void) fclose (fp);
  if (count != 4)
    return -1;

  for (elem = 0; elem < nelem; elem++)
    loadavg[elem] = (double) load_ave[elem] / (double) scale;

  return elem;

# endif /* __NetBSD__ */

# if !defined (LDAV_DONE) && defined (NeXT)
#  define LDAV_DONE
  /* The NeXT code was adapted from iscreen 3.2.  */

  host_t host;
  struct processor_set_basic_info info;
  unsigned info_count;

  /* We only know how to get the 1-minute average for this system,
     so even if the caller asks for more than 1, we only return 1.  */

  if (!getloadavg_initialized)
    {
      if (processor_set_default (host_self (), &default_set) == KERN_SUCCESS)
	getloadavg_initialized = 1;
    }

  if (getloadavg_initialized)
    {
      info_count = PROCESSOR_SET_BASIC_INFO_COUNT;
      if (processor_set_info (default_set, PROCESSOR_SET_BASIC_INFO, &host,
			      (processor_set_info_t) &info, &info_count)
	  != KERN_SUCCESS)
	getloadavg_initialized = 0;
      else
	{
	  if (nelem > 0)
	    loadavg[elem++] = (double) info.load_average / LOAD_SCALE;
	}
    }

  if (!getloadavg_initialized)
    return -1;
# endif /* NeXT */

# if !defined (LDAV_DONE) && defined (UMAX)
#  define LDAV_DONE
/* UMAX 4.2, which runs on the Encore Multimax multiprocessor, does not
   have a /dev/kmem.  Information about the workings of the running kernel
   can be gathered with inq_stats system calls.
   We only know how to get the 1-minute average for this system.  */

  struct proc_summary proc_sum_data;
  struct stat_descr proc_info;
  double load;
  register unsigned int i, j;

  if (cpus == 0)
    {
      register unsigned int c, i;
      struct cpu_config conf;
      struct stat_descr desc;

      desc.sd_next = 0;
      desc.sd_subsys = SUBSYS_CPU;
      desc.sd_type = CPUTYPE_CONFIG;
      desc.sd_addr = (char *) &conf;
      desc.sd_size = sizeof conf;

      if (inq_stats (1, &desc))
	return -1;

      c = 0;
      for (i = 0; i < conf.config_maxclass; ++i)
	{
	  struct class_stats stats;
	  bzero ((char *) &stats, sizeof stats);

	  desc.sd_type = CPUTYPE_CLASS;
	  desc.sd_objid = i;
	  desc.sd_addr = (char *) &stats;
	  desc.sd_size = sizeof stats;

	  if (inq_stats (1, &desc))
	    return -1;

	  c += stats.class_numcpus;
	}
      cpus = c;
      samples = cpus < 2 ? 3 : (2 * cpus / 3);
    }

  proc_info.sd_next = 0;
  proc_info.sd_subsys = SUBSYS_PROC;
  proc_info.sd_type = PROCTYPE_SUMMARY;
  proc_info.sd_addr = (char *) &proc_sum_data;
  proc_info.sd_size = sizeof (struct proc_summary);
  proc_info.sd_sizeused = 0;

  if (inq_stats (1, &proc_info) != 0)
    return -1;

  load = proc_sum_data.ps_nrunnable;
  j = 0;
  for (i = samples - 1; i > 0; --i)
    {
      load += proc_sum_data.ps_nrun[j];
      if (j++ == PS_NRUNSIZE)
	j = 0;
    }

  if (nelem > 0)
    loadavg[elem++] = load / samples / cpus;
# endif /* UMAX */

# if !defined (LDAV_DONE) && defined (DGUX)
#  define LDAV_DONE
  /* This call can return -1 for an error, but with good args
     it's not supposed to fail.  The first argument is for no
     apparent reason of type `long int *'.  */
  dg_sys_info ((long int *) &load_info,
	       DG_SYS_INFO_LOAD_INFO_TYPE,
	       DG_SYS_INFO_LOAD_VERSION_0);

  if (nelem > 0)
    loadavg[elem++] = load_info.one_minute;
  if (nelem > 1)
    loadavg[elem++] = load_info.five_minute;
  if (nelem > 2)
    loadavg[elem++] = load_info.fifteen_minute;
# endif /* DGUX */

# if !defined (LDAV_DONE) && defined (apollo)
#  define LDAV_DONE
/* Apollo code from lisch@mentorg.com (Ray Lischner).

   This system call is not documented.  The load average is obtained as
   three long integers, for the load average over the past minute,
   five minutes, and fifteen minutes.  Each value is a scaled integer,
   with 16 bits of integer part and 16 bits of fraction part.

   I'm not sure which operating system first supported this system call,
   but I know that SR10.2 supports it.  */

  extern void proc1_$get_loadav ();
  unsigned long load_ave[3];

  proc1_$get_loadav (load_ave);

  if (nelem > 0)
    loadavg[elem++] = load_ave[0] / 65536.0;
  if (nelem > 1)
    loadavg[elem++] = load_ave[1] / 65536.0;
  if (nelem > 2)
    loadavg[elem++] = load_ave[2] / 65536.0;
# endif /* apollo */

# if !defined (LDAV_DONE) && defined (OSF_MIPS)
#  define LDAV_DONE

  struct tbl_loadavg load_ave;
  table (TBL_LOADAVG, 0, &load_ave, 1, sizeof (load_ave));
  loadavg[elem++]
    = (load_ave.tl_lscale == 0
       ? load_ave.tl_avenrun.d[0]
       : (load_ave.tl_avenrun.l[0] / (double) load_ave.tl_lscale));
# endif	/* OSF_MIPS */

# if !defined (LDAV_DONE) && (defined (__MSDOS__) || defined (WINDOWS32))
#  define LDAV_DONE

  /* A faithful emulation is going to have to be saved for a rainy day.  */
  for ( ; elem < nelem; elem++)
    {
      loadavg[elem] = 0.0;
    }
# endif  /* __MSDOS__ || WINDOWS32 */

# if !defined (LDAV_DONE) && defined (OSF_ALPHA)
#  define LDAV_DONE

  struct tbl_loadavg load_ave;
  table (TBL_LOADAVG, 0, &load_ave, 1, sizeof (load_ave));
  for (elem = 0; elem < nelem; elem++)
    loadavg[elem]
      = (load_ave.tl_lscale == 0
       ? load_ave.tl_avenrun.d[elem]
       : (load_ave.tl_avenrun.l[elem] / (double) load_ave.tl_lscale));
# endif /* OSF_ALPHA */

# if !defined (LDAV_DONE) && defined (VMS)
  /* VMS specific code -- read from the Load Ave driver.  */

  LOAD_AVE_TYPE load_ave[3];
  static int getloadavg_initialized = 0;
#  ifdef eunice
  struct
  {
    int dsc$w_length;
    char *dsc$a_pointer;
  } descriptor;
#  endif

  /* Ensure that there is a channel open to the load ave device.  */
  if (!getloadavg_initialized)
    {
      /* Attempt to open the channel.  */
#  ifdef eunice
      descriptor.dsc$w_length = 18;
      descriptor.dsc$a_pointer = "$$VMS_LOAD_AVERAGE";
#  else
      $DESCRIPTOR (descriptor, "LAV0:");
#  endif
      if (sys$assign (&descriptor, &channel, 0, 0) & 1)
	getloadavg_initialized = 1;
    }

  /* Read the load average vector.  */
  if (getloadavg_initialized
      && !(sys$qiow (0, channel, IO$_READVBLK, 0, 0, 0,
		     load_ave, 12, 0, 0, 0, 0) & 1))
    {
      sys$dassgn (channel);
      getloadavg_initialized = 0;
    }

  if (!getloadavg_initialized)
    return -1;
# endif /* VMS */

# if !defined (LDAV_DONE) && defined(LOAD_AVE_TYPE) && !defined(VMS)

  /* UNIX-specific code -- read the average from /dev/kmem.  */

#  define LDAV_PRIVILEGED		/* This code requires special installation.  */

  LOAD_AVE_TYPE load_ave[3];

  /* Get the address of LDAV_SYMBOL.  */
  if (offset == 0)
    {
#  ifndef sgi
#   ifndef NLIST_STRUCT
      strcpy (nl[0].n_name, LDAV_SYMBOL);
      strcpy (nl[1].n_name, "");
#   else /* NLIST_STRUCT */
#    ifdef HAVE_STRUCT_NLIST_N_UN_N_NAME
      nl[0].n_un.n_name = LDAV_SYMBOL;
      nl[1].n_un.n_name = 0;
#    else /* not HAVE_STRUCT_NLIST_N_UN_N_NAME */
      nl[0].n_name = LDAV_SYMBOL;
      nl[1].n_name = 0;
#    endif /* not HAVE_STRUCT_NLIST_N_UN_N_NAME */
#   endif /* NLIST_STRUCT */

#   ifndef SUNOS_5
      if (
#    if !(defined (_AIX) && !defined (ps2))
	  nlist (KERNEL_FILE, nl)
#    else  /* _AIX */
	  knlist (nl, 1, sizeof (nl[0]))
#    endif
	  >= 0)
	  /* Omit "&& nl[0].n_type != 0 " -- it breaks on Sun386i.  */
	  {
#    ifdef FIXUP_KERNEL_SYMBOL_ADDR
	    FIXUP_KERNEL_SYMBOL_ADDR (nl);
#    endif
	    offset = nl[0].n_value;
	  }
#   endif /* !SUNOS_5 */
#  else  /* sgi */
      int ldav_off;

      ldav_off = sysmp (MP_KERNADDR, MPKA_AVENRUN);
      if (ldav_off != -1)
	offset = (long) ldav_off & 0x7fffffff;
#  endif /* sgi */
    }

  /* Make sure we have /dev/kmem open.  */
  if (!getloadavg_initialized)
    {
#  ifndef SUNOS_5
      channel = open ("/dev/kmem", 0);
      if (channel >= 0)
	{
	  /* Set the channel to close on exec, so it does not
	     litter any child's descriptor table.  */
#   ifdef F_SETFD
#    ifndef FD_CLOEXEC
#     define FD_CLOEXEC 1
#    endif
	  (void) fcntl (channel, F_SETFD, FD_CLOEXEC);
#   endif
	  getloadavg_initialized = 1;
	}
#  else /* SUNOS_5 */
      /* We pass 0 for the kernel, corefile, and swapfile names
	 to use the currently running kernel.  */
      kd = kvm_open (0, 0, 0, O_RDONLY, 0);
      if (kd != 0)
	{
	  /* nlist the currently running kernel.  */
	  kvm_nlist (kd, nl);
	  offset = nl[0].n_value;
	  getloadavg_initialized = 1;
	}
#  endif /* SUNOS_5 */
    }

  /* If we can, get the load average values.  */
  if (offset && getloadavg_initialized)
    {
      /* Try to read the load.  */
#  ifndef SUNOS_5
      if (lseek (channel, offset, 0) == -1L
	  || read (channel, (char *) load_ave, sizeof (load_ave))
	  != sizeof (load_ave))
	{
	  close (channel);
	  getloadavg_initialized = 0;
	}
#  else  /* SUNOS_5 */
      if (kvm_read (kd, offset, (char *) load_ave, sizeof (load_ave))
	  != sizeof (load_ave))
        {
          kvm_close (kd);
          getloadavg_initialized = 0;
	}
#  endif /* SUNOS_5 */
    }

  if (offset == 0 || !getloadavg_initialized)
    return -1;
# endif /* LOAD_AVE_TYPE and not VMS */

# if !defined (LDAV_DONE) && defined (LOAD_AVE_TYPE) /* Including VMS.  */
  if (nelem > 0)
    loadavg[elem++] = LDAV_CVT (load_ave[0]);
  if (nelem > 1)
    loadavg[elem++] = LDAV_CVT (load_ave[1]);
  if (nelem > 2)
    loadavg[elem++] = LDAV_CVT (load_ave[2]);

#  define LDAV_DONE
# endif /* !LDAV_DONE && LOAD_AVE_TYPE */

# ifdef LDAV_DONE
  return elem;
# else
  /* Set errno to zero to indicate that there was no particular error;
     this function just can't work at all on this system.  */
  errno = 0;
  return -1;
# endif
}

#endif /* ! HAVE_GETLOADAVG */

#ifdef TEST
#include "make.h"

int
main (int argc, char **argv)
{
  int naptime = 0;

  if (argc > 1)
    naptime = atoi (argv[1]);

  while (1)
    {
      double avg[3];
      int loads;

      errno = 0;		/* Don't be misled if it doesn't set errno.  */
      loads = getloadavg (avg, 3);
      if (loads == -1)
	{
	  perror ("Error getting load average");
	  exit (1);
	}
      if (loads > 0)
	printf ("1-minute: %f  ", avg[0]);
      if (loads > 1)
	printf ("5-minute: %f  ", avg[1]);
      if (loads > 2)
	printf ("15-minute: %f  ", avg[2]);
      if (loads > 0)
	putchar ('\n');

      if (naptime == 0)
	break;
      sleep (naptime);
    }

  exit (0);
}
#endif /* TEST */
