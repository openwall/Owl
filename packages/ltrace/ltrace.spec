# $Id: Owl/packages/ltrace/ltrace.spec,v 1.7 2001/01/15 05:20:24 solar Exp $

Summary: Tracks runtime library calls from dynamically linked executables.
Name: ltrace
Version: 0.3.10
Release: 7owl
Copyright: GPL
Group: Development/Debuggers
ExclusiveArch: %ix86 sparc sparcv9
Source: ftp://ftp.debian.org/debian/dists/potato/main/source/utils/ltrace_%{version}.tar.gz
Patch0: ltrace-0.3.10-rh-sparc.diff
Patch1: ltrace-0.3.10-rh-mandir.diff
Patch2: ltrace-0.3.10-rh-nsyscals0.diff
Patch3: ltrace-0.3.10-rh-strlen.diff
Prefix: %{_prefix}
BuildRoot: /var/rpm-buildroot/%{name}-root

%description
ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls called by the executed process
and the signals received by the executed process.  ltrace can also
intercept and print system calls executed by the process.

You should install ltrace if you need a sysadmin tool for tracking the
execution of processes.

%prep
%setup -q

%ifarch sparc sparcv9
%patch0 -p1
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure
make

%install
make DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install
rm -rf $RPM_BUILD_ROOT/%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING README TODO BUGS ChangeLog
%{_prefix}/bin/ltrace
%{_mandir}/man1/ltrace.1*
%config /etc/ltrace.conf

%changelog
* Sun Jan 14 2001 Michail Litvak <mci@owl.openwall.com>
- extracted from sparc patch - ltrace-0.3.10-rh-strlen.diff
  (it useful for any arch)
- fixed some type cast in sparc patch

* Sun Jan 14 2001 Solar Designer <solar@owl.openwall.com>
- i386 -> %ix86

* Sun Jan 14 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH

* Thu Aug  2 2000 Tim Waugh <twaugh@redhat.com>
- fix off-by-one problem in checking syscall number

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Matt Wilson <msw@redhat.com>
- rebuilt for next release
- patched Makefile.in to take a hint on mandir (patch2)
- use %%{_mandir} and %%makeinstall

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Jan  7 2000 Jeff Johnson <jbj@redhat.com>
- update to 0.3.10.
- include (but don't apply) sparc patch from Jakub Jellinek.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 2)

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.3.6.

* Mon Sep 21 1998 Preston Brown <pbrown@redhat.com>
- upgraded to 0.3.4
