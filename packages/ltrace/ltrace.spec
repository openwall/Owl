# $Id: Owl/packages/ltrace/ltrace.spec,v 1.13 2002/02/06 16:27:42 solar Exp $

Summary: Tracks runtime library calls from dynamically linked executables.
Name: ltrace
Version: 0.3.10
Release: owl8
License: GPL
Group: Development/Debuggers
Source: ftp://ftp.debian.org/debian/dists/potato/main/source/utils/ltrace_%{version}.tar.gz
Patch0: ltrace-0.3.10-rh-sparc.diff
Patch1: ltrace-0.3.10-rh-mandir.diff
Patch2: ltrace-0.3.10-rh-nsyscals0.diff
Patch3: ltrace-0.3.10-rh-strlen.diff
Prefix: %{_prefix}
ExclusiveArch: %ix86 sparc sparcv9
BuildRoot: /override/%{name}-%{version}

%description
ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls invoked by the executed process
and the signals received by the executed process.  ltrace can also
intercept and print system calls invoked by the process.

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
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/doc
mv -f debian/changelog ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING README TODO BUGS ChangeLog
%{_prefix}/bin/ltrace
%{_mandir}/man1/ltrace.1*
%config /etc/ltrace.conf

%changelog
* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Thu Oct 25 2001 Michail Litvak <mci@owl.openwall.com>
- fix dangling symlink

* Sun Jan 14 2001 Michail Litvak <mci@owl.openwall.com>
- extracted from sparc patch - ltrace-0.3.10-rh-strlen.diff
  (it useful for any arch)
- fixed some type cast in sparc patch

* Sun Jan 14 2001 Solar Designer <solar@owl.openwall.com>
- Use the ix86 macro.

* Sun Jan 14 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
