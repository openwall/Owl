/*
 * This file has been generated automatically
 * by CMake commands. Do not edit.
 *
 * Original contents from @(#)align_test.c	1.19 03/11/25 Copyright 1995 J. Schilling
 *
 */

#ifndef	_UTYPES_H
#include <utypes.h>
#endif

#define ALIGN_SHORT 2
#define ALIGN_INT 4
#define ALIGN_LONG 4
#define ALIGN_LLONG 8
#define ALIGN_FLOAT 4
#define ALIGN_DOUBLE 8
#define ALIGN_PTR 4

#define SIZE_SHORT 2
#define SIZE_INT 4
#define SIZE_LONG 4
#define SIZE_LLONG 8
#define SIZE_FLOAT 4
#define SIZE_DOUBLE 8
#define SIZE_PTR 4


#define ALIGN_SMASK 1
#define ALIGN_IMASK 3
#define ALIGN_LMASK 3
#define ALIGN_LLMASK 7
#define ALIGN_FMASK 3
#define ALIGN_DMASK 7
#define ALIGN_PMASK 3


/*
 * There used to be a cast to an int but we get a warning from GCC.
 * This warning message from GCC is wrong.
 * Believe me that this macro would even be usable if I would cast to short.
 * In order to avoid this warning, we are now using UIntptr_t
 */
#define	xaligned(a, s)		((((UIntptr_t)(a)) & (s)) == 0 )
#define	x2aligned(a, b, s)	(((((UIntptr_t)(a)) | ((UIntptr_t)(b))) & (s)) == 0 )

#define	saligned(a)		xaligned(a, ALIGN_SMASK)
#define	s2aligned(a, b)		x2aligned(a, b, ALIGN_SMASK)

#define	ialigned(a)		xaligned(a, ALIGN_IMASK)
#define	i2aligned(a, b)		x2aligned(a, b, ALIGN_IMASK)

#define	laligned(a)		xaligned(a, ALIGN_LMASK)
#define	l2aligned(a, b)		x2aligned(a, b, ALIGN_LMASK)

#define	llaligned(a)		xaligned(a, ALIGN_LLMASK)
#define	ll2aligned(a, b)	x2aligned(a, b, ALIGN_LLMASK)

#define	faligned(a)		xaligned(a, ALIGN_FMASK)
#define	f2aligned(a, b)		x2aligned(a, b, ALIGN_FMASK)

#define	daligned(a)		xaligned(a, ALIGN_DMASK)
#define	d2aligned(a, b)		x2aligned(a, b, ALIGN_DMASK)

#define	paligned(a)		xaligned(a, ALIGN_PMASK)
#define	p2aligned(a, b)		x2aligned(a, b, ALIGN_PMASK)


/*
 * There used to be a cast to an int but we get a warning from GCC.
 * This warning message from GCC is wrong.
 * Believe me that this macro would even be usable if I would cast to short.
 * In order to avoid this warning, we are now using UIntptr_t
 */
#define	xalign(x, a, m)		( ((char *)(x)) + ( (a) - 1 - ((((UIntptr_t)(x))-1)&(m))) )

#define	salign(x)		xalign((x), ALIGN_SHORT, ALIGN_SMASK)
#define	ialign(x)		xalign((x), ALIGN_INT, ALIGN_IMASK)
#define	lalign(x)		xalign((x), ALIGN_LONG, ALIGN_LMASK)
#define	llalign(x)		xalign((x), ALIGN_LLONG, ALIGN_LLMASK)
#define	falign(x)		xalign((x), ALIGN_FLOAT, ALIGN_FMASK)
#define	dalign(x)		xalign((x), ALIGN_DOUBLE, ALIGN_DMASK)
#define	palign(x)		xalign((x), ALIGN_PTR, ALIGN_PMASK)
