#ifdef __hpux__
.SPACE $PRIVATE$
.SUBSPA $UNWIND_END$,ACCESS=0
.EXPORT $UNWIND_END
$UNWIND_END
.SUBSPA $RECOVER_END$,ACCESS=0
.EXPORT $RECOVER_END
$RECOVER_END
.SPACE $TEXT$
.SUBSPA $CODE$,ALIGN=8,ACCESS=44
.EXPORT $START$
$START$
#else
.text
.globl _start, __start
_start:
__start:
#endif
#if defined(__linux__) && (defined(__i386__) || defined(__x86_64__))
	movl $1,%eax
	movl $STATUS,%ebx
	int $0x80
#elif defined(__linux__) && defined(__sparc__)
	or %g0,1,%g1
	or %g0,STATUS,%o0
	ta 0x10
#elif defined(__linux__) && defined(__alpha__)
	bis $31,1,$0
	bis $31,STATUS,$16
	callsys
#elif defined(__sun__) && defined(__sparc__)
	or %g0,1,%g1
	or %g0,STATUS,%o0
	ta 0
#elif defined(__hpux__)
	ldi STATUS,%r26
	ldil -0x80000,%r1
	ble 4(%sr7,%r1)
	ldi 1,%r22
#else
#error Sorry, your platform is not supported
#endif
