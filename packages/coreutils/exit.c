#include <linux/version.h>

#if (defined(__i386__) && (LINUX_VERSION_CODE <= KERNEL_VERSION(2, 6, 18)))

static int errno;
#define __KERNEL__
#include <linux/unistd.h>
#undef __KERNEL__
#define __NR__exit __NR_exit
static inline _syscall1(void, _exit, int, status)

#else

#include <unistd.h>

#endif

void
_start(void)
{
	_exit(STATUS);
}
