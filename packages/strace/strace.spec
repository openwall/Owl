# $Id: Owl/packages/strace/strace.spec,v 1.11 2004/09/10 07:31:56 galaxy Exp $

Summary: Tracks and displays system calls associated with a running process.
Name: strace
Version: 4.5.1
Release: owl2
License: BSD
Group: Development/Debuggers
URL: http://www.liacs.nl/~wichert/strace/
Source: http://prdownloads.sourceforge.net/%name/%name-%version.tar.bz2
Patch0: strace-4.5.1-owl-alt-fixes.diff
Patch1: strace-4.5.1-owl-man.diff
Patch2: strace-4.5.1-alt-pipe-setlinebuf.diff
Patch3: strace-4.5.1-alt-trace-coredump.diff
Patch4: strace-4.5.1-alt-keep_status.diff
Patch5: strace-4.5.1-owl-quota.diff
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%GNUconfigure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_mandir/man1
mkdir -p $RPM_BUILD_ROOT%_prefix/bin
%makeinstall man1dir=$RPM_BUILD_ROOT%_mandir/man1

%files
%defattr(-,root,root)
%doc COPYRIGHT CREDITS PORTING README README-linux TODO
%doc ChangeLog NEWS
%_prefix/bin/strace
%_mandir/man1/strace.1*

%files graph
%defattr(-,root,root)
%_prefix/bin/strace-graph

%changelog
* Wed Mar 10 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 4.5.1-owl2
- Added a dirty patch to switch strace to using kernel version of quota.h
(this allows to recognize both types of quota version). This patch must be
reviewed and cleaned, but for now it has necessary functionality.

* Fri Feb 27 2004 Michail Litvak <mci@owl.openwall.com> 4.5.1-owl1
- 4.5.1
- Added patches from ALT.

* Fri May 16 2003 Solar Designer <solar@owl.openwall.com> 4.4-owl3
- Additional fixes to build with Linux 2.4.21-rc1 headers.

* Sat Jun 08 2002 Solar Designer <solar@owl.openwall.com>
- Updated to today's CVS version (post-4.4) with an additional fix for
displaying all possible ioctl names when there's more than one match,
some build fixes, and a Red Hat Linux derived patch for detaches from
multi-threaded programs.
- Package strace-graph (in its own subpackage due to the Perl requirement).

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
