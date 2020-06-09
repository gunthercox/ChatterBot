/* Debugging macros and interface.
Copyright (C) 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006 Free Software
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

#define DB_NONE         (0x000)
#define DB_BASIC        (0x001)
#define DB_VERBOSE      (0x002)
#define DB_JOBS         (0x004)
#define DB_IMPLICIT     (0x008)
#define DB_MAKEFILES    (0x100)

#define DB_ALL          (0xfff)

extern int db_level;

#define ISDB(_l)    ((_l)&db_level)

#define DBS(_l,_x)  do{ if(ISDB(_l)) {print_spaces (depth); \
                                      printf _x; fflush (stdout);} }while(0)

#define DBF(_l,_x)  do{ if(ISDB(_l)) {print_spaces (depth); \
                                      printf (_x, file->name); \
                                      fflush (stdout);} }while(0)

#define DB(_l,_x)   do{ if(ISDB(_l)) {printf _x; fflush (stdout);} }while(0)
