# $Id: Owl/packages/strace/strace.spec,v 1.5 2002/02/05 16:26:33 solar Exp $

Summary: Tracks and displays system calls associated with a running process.
Name: strace
Version: 4.2
Release: owl12
License: BSD
Group: Development/Debuggers
Source: http://www.liacs.nl/~wichert/strace/strace-%{version}.tar.gz
Patch0: strace-4.1-rh-sparc.diff
Patch1: strace-4.2-deb-lfs.diff
Patch2: strace-4.2-owl-timex.diff
Patch3: strace-4.2-rh-stat64.diff
Patch4: strace-4.2-rh-putmsg.diff
Patch5: strace-4.2-owl-printsock.diff
Patch6: strace-4.2-owl-man.diff
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The strace program intercepts and records the system calls invoked by
a running process.  strace can print a record of each system call, its
arguments, and its return value.  strace is useful for diagnosing
problems and debugging, as well as for instructional purposes.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
libtoolize --copy --force
aclocal
autoheader
autoconf

%configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
%makeinstall man1dir=${RPM_BUILD_ROOT}%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYRIGHT CREDITS PORTING README README-linux TODO
%doc ChangeLog NEWS
%{_prefix}/bin/strace
%{_mandir}/man1/strace.1*

%changelog
* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Package most of the documentation.

* Tue Aug 21 2001 Michail Litvak <mci@owl.openwall.com>
- man page fix

* Thu Jan 25 2001 Michail Litvak <mci@owl.openwall.com>
- Added patch to fix printsock 

* Mon Jan 23 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- Removed most of 2.4 related patches...
- Added patch to compile on 2.2 kernels (strace-4.2-owl-timex.diff)
