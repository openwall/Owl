# $Owl: Owl/packages/strace/strace.spec,v 1.24 2007/01/18 11:28:42 ldv Exp $

Summary: Tracks and displays system calls associated with a running process.
Name: strace
Version: 4.5.15
Release: owl1
License: BSD
Group: Development/Debuggers
URL: http://sourceforge.net/projects/strace/
Source: http://prdownloads.sourceforge.net/%name/%name-%version.tar.bz2
Patch0: strace-4.5.15-alt.diff
BuildRequires: automake, autoconf
BuildRoot: /override/%name-%version

%package graph
Summary: Processes strace output and displays a graph of invoked subprocesses.
Group: Development/Debuggers
Requires: %name = %version-%release

%description
The strace program intercepts and records the system calls invoked by
a running process.  strace can print a record of each system call, its
arguments, and its return value.  strace is useful for diagnosing
problems and debugging, as well as for instructional purposes.

%description graph
The strace-graph Perl script processes strace -f output and displays a
graph of invoked subprocesses.  It is useful for finding out what complex
commands do.

%prep
%setup -q
%patch0 -p2
bzip2 -9k ChangeLog

%{expand:%%define optflags %optflags -Wall}

%build
autoreconf -fisv
%configure
%__make

%install
rm -rf %buildroot
%makeinstall man1dir=%buildroot%_mandir/man1

%files
%defattr(-,root,root)
%doc COPYRIGHT CREDITS PORTING README README-linux TODO
%doc ChangeLog.bz2 NEWS
%_bindir/strace
%_mandir/man1/strace.1*

%files graph
%defattr(-,root,root)
%_bindir/strace-graph

%changelog
* Thu Jan 18 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.5.15-owl1
- Updated to 4.5.15.

* Fri Apr 21 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.5.14-owl2
- Fixed race condition in tcb allocation code.
- Fixed build on x86_64.

* Wed Jan 18 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.5.14-owl1
- Updated to 4.5.14.

* Mon Oct 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.5.13-owl2
- Applied upstream fix for potential buffer overflow in printpathn().

* Wed Aug 10 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.5.13-owl1
- Updated to 4.5.13.
- Synced set of patches with ALT's strace-4.5.13-alt1 package.

* Sat Jun 18 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.5.12-owl2
- Implemented more elaborate quotactl(2) deparser.

* Sat Jun 11 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.5.12-owl1
- Updated to 4.5.12.
- Reviewed Owl patches, removed obsolete ones.
- Imported a bunch of patches from ALT's strace-4.5.12-alt1 package.

* Wed Mar 10 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.5.1-owl2
- Added a dirty patch to switch strace to using kernel version of quota.h
(this allows to recognize both types of quota version). This patch must be
reviewed and cleaned, but for now it has necessary functionality.

* Fri Feb 27 2004 Michail Litvak <mci-at-owl.openwall.com> 4.5.1-owl1
- 4.5.1
- Added patches from ALT.

* Fri May 16 2003 Solar Designer <solar-at-owl.openwall.com> 4.4-owl3
- Additional fixes to build with Linux 2.4.21-rc1 headers.

* Sat Jun 08 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to today's CVS version (post-4.4) with an additional fix for
displaying all possible ioctl names when there's more than one match,
some build fixes, and a Red Hat Linux derived patch for detaches from
multi-threaded programs.
- Package strace-graph (in its own subpackage due to the Perl requirement).

* Tue Feb 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.
- Package most of the documentation.

* Tue Aug 21 2001 Michail Litvak <mci-at-owl.openwall.com>
- man page fix

* Thu Jan 25 2001 Michail Litvak <mci-at-owl.openwall.com>
- Added patch to fix printsock

* Mon Jan 23 2001 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH
- Removed most of 2.4 related patches...
- Added patch to compile on 2.2 kernels (strace-4.2-owl-timex.diff)
