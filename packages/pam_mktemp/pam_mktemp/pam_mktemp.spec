# $Id: Owl/packages/pam_mktemp/pam_mktemp/pam_mktemp.spec,v 1.15 2005/03/25 20:33:45 solar Exp $

Summary: Pluggable private /tmp space support for interactive (shell) sessions.
Name: pam_mktemp
Version: 0.2.6
Release: owl1
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
URL: http://www.openwall.com/pam/
Source: ftp://ftp.openwall.com/pub/projects/pam/modules/%name/%name-%version.tar.gz
BuildRoot: /override/%name-%version

%description
pam_mktemp is a PAM module which may be used with a PAM-aware login service
to provide per-user private directories under /tmp as a part of PAM session
or account management.

%prep
%setup -q

%build
make CFLAGS="-Wall -fPIC -DLINUX_PAM $RPM_OPT_FLAGS"

%install
rm -rf %buildroot
make install DESTDIR=%buildroot

%post
mkdir -p -m 711 /tmp/.private

%triggerin -- e2fsprogs
if [ -d /tmp/.private -a -O /tmp/.private ]; then
	chattr +a /tmp/.private 2> /dev/null || :
fi

%files
%defattr(-,root,root)
%doc LICENSE README
/lib/security/pam_mktemp.so

%changelog
* Fri Mar 25 2005 Solar Designer <solar@owl.openwall.com> 0.2.6-owl1
- Corrected the source code to not break C strict aliasing rules.

* Sun Nov 02 2003 Solar Designer <solar@owl.openwall.com> 0.2.5-owl1
- Ignore errors from chattr as /tmp may be on tmpfs rather than ext[23]fs.
- When compiling with gcc, also link with gcc.
- Use "install -c" (makes a difference on some non-Linux systems).
- Moved the "-c" out of CFLAGS, renamed FAKEROOT to DESTDIR.

* Mon Jun 02 2003 Solar Designer <solar@owl.openwall.com> 0.2.4.1-owl1
- Added URL.

* Thu Apr 25 2002 Solar Designer <solar@owl.openwall.com> 0.2.4-owl1
- Use a trigger on e2fsprogs, don't assume that chattr(1) is available
at the time this package is installed.

* Tue Apr 02 2002 Solar Designer <solar@owl.openwall.com>
- Use '=' instead of '.set' to declare the alias.

* Sun Mar 31 2002 Solar Designer <solar@owl.openwall.com>
- Support running without CAP_LINUX_IMMUTABLE as long as this code is
_never_ executed with the capability; should probably switch to using
mode 511 for the directory instead of the append-only flag, this would
be sufficient against tmpwatch (will prevent it from traversing the
directory structure at all, but we now have stmpclean).

* Thu Mar 21 2002 Solar Designer <solar@owl.openwall.com>
- Deal with non-ext2fs correctly (again).

* Wed Mar 20 2002 Solar Designer <solar@owl.openwall.com>
- Don't let the append-only flag get inherited by per-user subdirectories.

* Wed Mar 13 2002 Solar Designer <solar@owl.openwall.com>
- Make the /tmp/.private directory append-only (where supported) such that
the directory or its subdirectories don't get removed by a /tmp cleaner.

* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 09 2001 Solar Designer <solar@owl.openwall.com>
- Support stacking for account management as well as for session setup.
- No longer set LYNX_TEMP_SPACE.

* Tue Dec 19 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.
