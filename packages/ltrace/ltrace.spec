# $Id: Owl/packages/ltrace/ltrace.spec,v 1.19 2005/06/14 14:32:39 mci Exp $

Summary: Tracks runtime library calls from dynamically linked executables.
Name: ltrace
Version: 0.3.36
Release: owl1
License: GPL
Group: Development/Debuggers
Source: ftp://ftp.debian.org/debian/pool/main/l/ltrace/ltrace_%version.orig.tar.gz
Patch0: ltrace-0.3.36-alt-install-no-root.diff
Patch1: ltrace-0.3.36-owl-version.diff
Prefix: %_prefix
BuildRequires: elfutils-libelf-devel
ExclusiveArch: %ix86 alpha sparc sparcv9
BuildRoot: /override/%name-%version

%description
ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls invoked by the executed process
and the signals received by the executed process.  ltrace can also
intercept and print system calls invoked by the process.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
%__make

%install
%__make DESTDIR=%buildroot mandir=%_mandir install
rm -rf %buildroot%_prefix/doc

%files
%defattr(-,root,root)
%doc COPYING README TODO BUGS ChangeLog
%_prefix/bin/ltrace
%_mandir/man1/ltrace.1*
%config /etc/ltrace.conf

%changelog
* Mon Jun 13 2005 Michail Litvak <mci@owl.openwall.com> 0.3.36-owl1
- 0.3.36
- Dropped outdated patches, imported -no-root-install patch from ALT.
- Patch to correct version reported by ltrace -V.

* Fri Jan 07 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 0.3.10-owl9
- Added a patch to deal with "label at end of compound statement" issue.
- Cleaned up the spec.

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com> 0.3.10-owl8
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
