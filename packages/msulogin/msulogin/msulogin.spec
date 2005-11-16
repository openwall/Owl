# $Owl: Owl/packages/msulogin/msulogin/msulogin.spec,v 1.7 2005/11/16 13:16:56 solar Exp $

Summary: The single user mode login program (sulogin).
Name: msulogin
Version: 0.9.1
Release: owl1
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Base
URL: http://www.openwall.com/msulogin/
Source: ftp://ftp.openwall.com/pub/projects/msulogin/%name-%version.tar.gz
Conflicts: SysVinit < 2.85-owl4
BuildRoot: /override/%name-%version

%description
sulogin is a program to force the console user to login under a root
account before a shell is started.  Unlike other implementations of
sulogin, this one supports having multiple root accounts on a system.

%prep
%setup -q

%build
make CFLAGS="-c -Wall %optflags"

%install
rm -rf %buildroot
make install DESTDIR=%buildroot MANDIR=%_mandir

%files
%defattr(-,root,root)
%doc LICENSE
/sbin/sulogin
%_mandir/man8/sulogin.8*

%changelog
* Fri May 23 2003 Solar Designer <solar-at-owl.openwall.com> 0.9.1-owl1
- Avoid a race condition in the handling of timeout pointed out by
Pavel Kankovsky on owl-devel.

* Sun Apr 27 2003 Solar Designer <solar-at-owl.openwall.com> 0.9-owl1
- Wrote this program and the accompanying files.
