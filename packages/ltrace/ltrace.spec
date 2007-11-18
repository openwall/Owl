# $Owl: Owl/packages/ltrace/ltrace.spec,v 1.25 2007/11/18 00:51:19 ldv Exp $

Summary: Tracks runtime library calls from dynamically linked executables.
Name: ltrace
Version: 0.5
Release: owl1
License: GPL
Group: Development/Debuggers
Source: ftp://ftp.debian.org/debian/pool/main/l/ltrace/ltrace_%version.orig.tar.gz
Patch0: ltrace-0.3.36-alt-install-no-root.diff
Patch1: ltrace-0.5-deb.diff
BuildRequires: elfutils-libelf-devel
ExclusiveArch: %ix86 x86_64 sparc sparcv9
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
bzip2 -9k ChangeLog

# Build with -D_GNU_SOURCE to get off64_t definition
# which is necessary for libelf >= 0.130.
%{expand:%%define optflags %optflags -D_GNU_SOURCE}

%build
%configure
%__make

%install
%__make DESTDIR=%buildroot mandir=%_mandir install
rm -r %buildroot%_docdir

%files
%defattr(-,root,root)
%doc BUGS COPYING ChangeLog.bz2 README TODO
%_bindir/ltrace
%_mandir/man1/ltrace.1*
%config(noreplace) /etc/ltrace.conf

%changelog
* Sun Nov 18 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.5-owl1
- Updated to 0.5.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.3.36-owl2
- Compressed ChangeLog file.

* Mon Jun 13 2005 Michail Litvak <mci-at-owl.openwall.com> 0.3.36-owl1
- 0.3.36
- Dropped outdated patches, imported -no-root-install patch from ALT.
- Patch to correct version reported by ltrace -V.

* Fri Jan 07 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.3.10-owl9
- Added a patch to deal with "label at end of compound statement" issue.
- Cleaned up the spec.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com> 0.3.10-owl8
- Enforce our new spec file conventions

* Thu Oct 25 2001 Michail Litvak <mci-at-owl.openwall.com>
- fix dangling symlink

* Sun Jan 14 2001 Michail Litvak <mci-at-owl.openwall.com>
- extracted from sparc patch - ltrace-0.3.10-rh-strlen.diff
  (it useful for any arch)
- fixed some type cast in sparc patch

* Sun Jan 14 2001 Solar Designer <solar-at-owl.openwall.com>
- Use the ix86 macro.

* Sun Jan 14 2001 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH
