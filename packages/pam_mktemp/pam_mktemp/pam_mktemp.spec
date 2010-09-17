# $Owl: Owl/packages/pam_mktemp/pam_mktemp/pam_mktemp.spec,v 1.28 2010/09/17 22:32:42 solar Exp $

Summary: Pluggable private /tmp space support for interactive (shell) sessions.
Name: pam_mktemp
Version: 1.1.0
Release: owl1
License: BSD-compatible
Group: System Environment/Base
URL: http://www.openwall.com/pam/
Source: ftp://ftp.openwall.com/pub/projects/pam/modules/%name/%name-%version.tar.gz
BuildRequires: pam-devel, e2fsprogs-devel
BuildRoot: /override/%name-%version

%description
pam_mktemp is a PAM module which may be used with a PAM-aware login service
to provide per-user private directories under /tmp as a part of PAM session
or account management.

%prep
%setup -q

%build
make CFLAGS="%optflags -Wall -fPIC"

%install
rm -rf %buildroot
make install DESTDIR=%buildroot SECUREDIR=/%_lib/security

%post
mkdir -p -m 711 /tmp/.private

%if 0
# Disabled.  See the comment in pam_mktemp.c for the rationale.
%triggerin -- e2fsprogs
if [ -d /tmp/.private -a -O /tmp/.private ]; then
	chattr +a /tmp/.private 2> /dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc LICENSE README
/%_lib/security/pam_mktemp.so

%changelog
* Fri Sep 17 2010 Solar Designer <solar-at-owl.openwall.com> 1.1.0-owl1
- Documented the USE_SELINUX and USE_APPEND_FL compile-time settings.
- Added Solaris support (but GNU make and gcc are required by our Makefile).
- Updated the authorship, copyright, and licensing statements to use the
cut-down BSD license only (no public domain with a license fallback anymore,
which would be too cumbersome with significant contributions by two authors).

* Tue Sep 07 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.0.5-owl1
- Use ext2fs/ext2_fs.h instead of linux/ext2_fs.h to avoid potential
build problems with fresh kernel headers.
- Clear append-only flag from user directory iff the directory was
actually created.
- Replaced unsafe alloca(3) with malloc(3).
- Imported SELinux support from Sisyphus.

* Thu Sep 02 2010 Solar Designer <solar-at-owl.openwall.com> 1.0.4-owl1
- No longer set the append-only flag on /tmp/.private (see the comment in
pam_mktemp.c for the rationale).
- Placed the module into the public domain with fallback to a heavily cut-down
BSD license.

* Tue Apr 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.0.3-owl1
- Restricted list of global symbols exported by the PAM module
to standard set of six pam_sm_* functions.
- Changed Makefile to pass list of libraries to linker after regular
object files, to fix build with -Wl,--as-needed.
- Corrected specfile to make it build on x86_64.

* Mon Jan 09 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.0.2-owl1
- Replaced manual -DLINUX_PAM with Linux-PAM autodetection.
- Added workaround for build with Linux 2.6.x headers.

* Thu Aug 11 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.0.1-owl1
- Added support of filesystem drivers which fail with ENOSYS error code
in response to ioctl requests.

* Fri Mar 25 2005 Solar Designer <solar-at-owl.openwall.com> 1.0-owl1
- Corrected the source code to not break C strict aliasing rules.

* Sun Nov 02 2003 Solar Designer <solar-at-owl.openwall.com> 0.2.5-owl1
- Ignore errors from chattr as /tmp may be on tmpfs rather than ext[23]fs.
- When compiling with gcc, also link with gcc.
- Use "install -c" (makes a difference on some non-Linux systems).
- Moved the "-c" out of CFLAGS, renamed FAKEROOT to DESTDIR.

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 0.2.4.1-owl1
- Added URL.

* Thu Apr 25 2002 Solar Designer <solar-at-owl.openwall.com> 0.2.4-owl1
- Use a trigger on e2fsprogs, don't assume that chattr(1) is available
at the time this package is installed.

* Tue Apr 02 2002 Solar Designer <solar-at-owl.openwall.com>
- Use '=' instead of '.set' to declare the alias.

* Sun Mar 31 2002 Solar Designer <solar-at-owl.openwall.com>
- Support running without CAP_LINUX_IMMUTABLE as long as this code is
_never_ executed with the capability; should probably switch to using
mode 511 for the directory instead of the append-only flag, this would
be sufficient against tmpwatch (will prevent it from traversing the
directory structure at all, but we now have stmpclean).

* Thu Mar 21 2002 Solar Designer <solar-at-owl.openwall.com>
- Deal with non-ext2fs correctly (again).

* Wed Mar 20 2002 Solar Designer <solar-at-owl.openwall.com>
- Don't let the append-only flag get inherited by per-user subdirectories.

* Wed Mar 13 2002 Solar Designer <solar-at-owl.openwall.com>
- Make the /tmp/.private directory append-only (where supported) such that
the directory or its subdirectories don't get removed by a /tmp cleaner.

* Thu Feb 07 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 09 2001 Solar Designer <solar-at-owl.openwall.com>
- Support stacking for account management as well as for session setup.
- No longer set LYNX_TEMP_SPACE.

* Tue Dec 19 2000 Solar Designer <solar-at-owl.openwall.com>
- Initial version.
