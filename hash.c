/* hash.c -- hash table maintenance
   Copyright (C) 1995, 1999, 2002 Free Software Foundation, Inc.
   Written by Greg McGary <gkm@gnu.org> <greg@mcgary.org>

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

#include "make.h"
#include "hash.h"

#define	CALLOC(t, n) ((t *) calloc (sizeof (t), (n)))
#define MALLOC(t, n) ((t *) xmalloc (sizeof (t) * (n)))
#define REALLOC(o, t, n) ((t *) xrealloc ((o), sizeof (t) * (n)))
#define CLONE(o, t, n) ((t *) memcpy (MALLOC (t, (n)), (o), sizeof (t) * (n)))

static void hash_rehash __P((struct hash_table* ht));
static unsigned long round_up_2 __P((unsigned long rough));

/* Implement double hashing with open addressing.  The table size is
   always a power of two.  The secondary (`increment') hash function
   is forced to return an odd-value, in order to be relatively prime
   to the table size.  This guarantees that the increment can
   potentially hit every slot in the table during collision
   resolution.  */

void *hash_deleted_item = &hash_deleted_item;

/* Force the table size to be a power of two, possibly rounding up the
   given size.  */

void
hash_init (struct hash_table *ht, unsigned long size,
           hash_func_t hash_1, hash_func_t hash_2, hash_cmp_func_t hash_cmp)
{
  ht->ht_size = round_up_2 (size);
  ht->ht_empty_slots = ht->ht_size;
  ht->ht_vec = (void**) CALLOC (struct token *, ht->ht_size);
  if (ht->ht_vec == 0)
    {
      fprintf (stderr, _("can't allocate %ld bytes for hash table: memory exhausted"),
	       ht->ht_size * sizeof(struct token *));
      exit (1);
    }

  ht->ht_capacity = ht->ht_size - (ht->ht_size / 16); /* 93.75% loading factor */
  ht->ht_fill = 0;
  ht->ht_collisions = 0;
  ht->ht_lookups = 0;
  ht->ht_rehashes = 0;
  ht->ht_hash_1 = hash_1;
  ht->ht_hash_2 = hash_2;
  ht->ht_compare = hash_cmp;
}

/* Load an array of items into `ht'.  */

void
hash_load (struct hash_table *ht, void *item_table,
           unsigned long cardinality, unsigned long size)
{
  char *items = (char *) item_table;
  while (cardinality--)
    {
      hash_insert (ht, items);
      items += size;
    }
}

/* Returns the address of the table slot matching `key'.  If `key' is
   not found, return the address of an empty slot suitable for
   inserting `key'.  The caller is responsible for incrementing
   ht_fill on insertion.  */

void **
hash_find_slot (struct hash_table *ht, const void *key)
{
  void **slot;
  void **deleted_slot = 0;
  unsigned int hash_2 = 0;
  unsigned int hash_1 = (*ht->ht_hash_1) (key);

  ht->ht_lookups++;
  for (;;)
    {
      hash_1 &= (ht->ht_size - 1);
      slot = &ht->ht_vec[hash_1];

      if (*slot == 0)
	return (deleted_slot ? deleted_slot : slot);
      if (*slot == hash_deleted_item)
	{
	  if (deleted_slot == 0)
	    deleted_slot = slot;
	}
      else
	{
	  if (key == *slot)
	    return slot;
	  if ((*ht->ht_compare) (key, *slot) == 0)
	    return slot;
	  ht->ht_collisions++;
	}
      if (!hash_2)
	  hash_2 = (*ht->ht_hash_2) (key) | 1;
      hash_1 += hash_2;
    }
}

void *
hash_find_item (struct hash_table *ht, const void *key)
{
  void **slot = hash_find_slot (ht, key);
  return ((HASH_VACANT (*slot)) ? 0 : *slot);
}

void *
hash_insert (struct hash_table *ht, const void *item)
{
  void **slot = hash_find_slot (ht, item);
  const void *old_item = slot ? *slot : 0;
  hash_insert_at (ht, item, slot);
  return (void *)((HASH_VACANT (old_item)) ? 0 : old_item);
}

void *
hash_insert_at (struct hash_table *ht, const void *item, const void *slot)
{
  const void *old_item = *(void **) slot;
  if (HASH_VACANT (old_item))
    {
      ht->ht_fill++;
      if (old_item == 0)
	ht->ht_empty_slots--;
      old_item = item;
    }
  *(void const **) slot = item;
  if (ht->ht_empty_slots < ht->ht_size - ht->ht_capacity)
    {
      hash_rehash (ht);
      return (void *) hash_find_slot (ht, item);
    }
  else
    return (void *) slot;
}

void *
hash_delete (struct hash_table *ht, const void *item)
{
  void **slot = hash_find_slot (ht, item);
  return hash_delete_at (ht, slot);
}

void *
hash_delete_at (struct hash_table *ht, const void *slot)
{
  void *item = *(void **) slot;
  if (!HASH_VACANT (item))
    {
      *(void const **) slot = hash_deleted_item;
      ht->ht_fill--;
      return item;
    }
  else
    return 0;
}

void
hash_free_items (struct hash_table *ht)
{
  void **vec = ht->ht_vec;
  void **end = &vec[ht->ht_size];
  for (; vec < end; vec++)
    {
      void *item = *vec;
      if (!HASH_VACANT (item))
	free (item);
      *vec = 0;
    }
  ht->ht_fill = 0;
  ht->ht_empty_slots = ht->ht_size;
}

void
hash_delete_items (struct hash_table *ht)
{
  void **vec = ht->ht_vec;
  void **end = &vec[ht->ht_size];
  for (; vec < end; vec++)
    *vec = 0;
  ht->ht_fill = 0;
  ht->ht_collisions = 0;
  ht->ht_lookups = 0;
  ht->ht_rehashes = 0;
  ht->ht_empty_slots = ht->ht_size;
}

void
hash_free (struct hash_table *ht, int free_items)
{
  if (free_items)
    hash_free_items (ht);
  else
    {
      ht->ht_fill = 0;
      ht->ht_empty_slots = ht->ht_size;
    }
  free (ht->ht_vec);
  ht->ht_vec = 0;
  ht->ht_capacity = 0;
}

void
hash_map (struct hash_table *ht, hash_map_func_t map)
{
  void **slot;
  void **end = &ht->ht_vec[ht->ht_size];

  for (slot = ht->ht_vec; slot < end; slot++)
    {
      if (!HASH_VACANT (*slot))
	(*map) (*slot);
    }
}

void
hash_map_arg (struct hash_table *ht, hash_map_arg_func_t map, void *arg)
{
  void **slot;
  void **end = &ht->ht_vec[ht->ht_size];

  for (slot = ht->ht_vec; slot < end; slot++)
    {
      if (!HASH_VACANT (*slot))
	(*map) (*slot, arg);
    }
}

/* Double the size of the hash table in the event of overflow... */

static void
hash_rehash (struct hash_table *ht)
{
  unsigned long old_ht_size = ht->ht_size;
  void **old_vec = ht->ht_vec;
  void **ovp;

  if (ht->ht_fill >= ht->ht_capacity)
    {
      ht->ht_size *= 2;
      ht->ht_capacity = ht->ht_size - (ht->ht_size >> 4);
    }
  ht->ht_rehashes++;
  ht->ht_vec = (void **) CALLOC (struct token *, ht->ht_size);

  for (ovp = old_vec; ovp < &old_vec[old_ht_size]; ovp++)
    {
      if (! HASH_VACANT (*ovp))
	{
	  void **slot = hash_find_slot (ht, *ovp);
	  *slot = *ovp;
	}
    }
  ht->ht_empty_slots = ht->ht_size - ht->ht_fill;
  free (old_vec);
}

void
hash_print_stats (struct hash_table *ht, FILE *out_FILE)
{
  /* GKM FIXME: honor NO_FLOAT */
  fprintf (out_FILE, _("Load=%ld/%ld=%.0f%%, "), ht->ht_fill, ht->ht_size,
	   100.0 * (double) ht->ht_fill / (double) ht->ht_size);
  fprintf (out_FILE, _("Rehash=%d, "), ht->ht_rehashes);
  fprintf (out_FILE, _("Collisions=%ld/%ld=%.0f%%"), ht->ht_collisions, ht->ht_lookups,
	   (ht->ht_lookups
	    ? (100.0 * (double) ht->ht_collisions / (double) ht->ht_lookups)
	    : 0));
}

/* Dump all items into a NULL-terminated vector.  Use the
   user-supplied vector, or malloc one.  */

void **
hash_dump (struct hash_table *ht, void **vector_0, qsort_cmp_t compare)
{
  void **vector;
  void **slot;
  void **end = &ht->ht_vec[ht->ht_size];

  if (vector_0 == 0)
    vector_0 = MALLOC (void *, ht->ht_fill + 1);
  vector = vector_0;

  for (slot = ht->ht_vec; slot < end; slot++)
    if (!HASH_VACANT (*slot))
      *vector++ = *slot;
  *vector = 0;

  if (compare)
    qsort (vector_0, ht->ht_fill, sizeof (void *), compare);
  return vector_0;
}

/* Round a given number up to the nearest power of 2. */

static unsigned long
round_up_2 (unsigned long n)
{
  n |= (n >> 1);
  n |= (n >> 2);
  n |= (n >> 4);
  n |= (n >> 8);
  n |= (n >> 16);

#if !defined(HAVE_LIMITS_H) || ULONG_MAX > 4294967295
  /* We only need this on systems where unsigned long is >32 bits.  */
  n |= (n >> 32);
#endif

  return n + 1;
}
