# $Owl: Owl/packages/ltrace/ltrace.spec,v 1.30 2014/07/12 14:09:31 galaxy Exp $

Summary: Tracks runtime library calls from dynamically linked executables.
Name: ltrace
Version: 0.5.3
Release: owl2
License: GPL
Group: Development/Debuggers
Source: ftp://ftp.debian.org/debian/pool/main/l/ltrace/ltrace_%version.orig.tar.gz
Patch0: %name-0.5.3-deb-2.1.diff
Patch1: %name-0.5.3-owl-ptrace.diff
Patch2: %name-0.5.3-owl-warnings.diff
Patch3: %name-0.5.3-owl-configure.diff
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
%patch2 -p1
%patch3 -p1
bzip2 -9k ChangeLog

# Build with -D_GNU_SOURCE to get off64_t definition
# which is necessary for libelf >= 0.130.
%{expand:%%define optflags %optflags -D_GNU_SOURCE}

%build
%configure
%__make

%install
%makeinstall
rm -r %buildroot%_docdir

%files
%defattr(-,root,root)
%doc BUGS COPYING ChangeLog.bz2 README TODO
%_bindir/ltrace
%_mandir/man1/ltrace.1*
%config(noreplace) /etc/ltrace.conf

%changelog
* Sat Jun 28 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.5.3-owl3
- Patched configure to be more GNU configure compatible.

* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 0.5.3-owl2
- Dropped an obsoleted iquote patch.

* Fri Aug 27 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 0.5.3-owl1
- Updated to 0.5.3-2.1.
- Dropped obsoleted patches (fixed in upstream).

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
