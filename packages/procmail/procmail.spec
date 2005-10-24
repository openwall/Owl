# $Id: Owl/packages/procmail/procmail.spec,v 1.10 2005/10/24 03:06:29 solar Exp $

Summary: The procmail mail processing program.
Name: procmail
Version: 3.15.2
Release: owl3
License: GPL or Artistic License
Group: System Environment/Daemons
Source: ftp://ftp.procmail.org/pub/procmail/procmail-%version.tar.gz
Patch0: procmail-3.15.2-owl-config.diff
Patch1: procmail-3.15.2-owl-fixes.diff
BuildRequires: mktemp >= 1:1.3.1
BuildRoot: /override/%name-%version

%description
procmail is a mail processing program which can be used to filter,
sort, or selectively forward e-mail messages.  Optionally, procmail
may be installed as the local delivery agent.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{expand:%%define optflags %optflags -fno-strict-aliasing -Wall -Wno-comment -Wno-parentheses}

%build
make \
	LOCKINGTEST=100 \
	SEARCHLIBS="-lm -lnsl -ldl" \
	CC=gcc \
	CFLAGS0="%optflags"

%install
rm -rf %buildroot
mkdir -p %buildroot{%_bindir,%_mandir/man{1,5}}

make install \
	BASENAME=%buildroot%_prefix \
	MANDIR=%buildroot%_mandir

%files
%defattr(-,root,root)
%doc FAQ HISTORY README KNOWN_BUGS FEATURES COPYING Artistic examples
%attr(755,root,root) %_bindir/formail
%attr(755,root,root) %_bindir/lockfile
%attr(755,root,root) %_bindir/mailstat
%attr(755,root,root) %_bindir/procmail
%_mandir/man[15]/*

%changelog
* Tue Jun 28 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.15.2-owl3
- Build this package without optimizations based on strict aliasing rules.

* Fri Oct 04 2002 Solar Designer <solar-at-owl.openwall.com> 3.15.2-owl2
- Corrected the mansed script "fix", thanks to Dmitry V. Levin of ALT Linux
for pointing out that it was broken.

* Tue Aug 13 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 3.15.2.
- Added temporary file handling fixes to scripts used during the builds.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Thu May 10 2001 Solar Designer <solar-at-owl.openwall.com>
- Don't let procmail get linked against -lnet (our libnet isn't what
procmail thinks it is).

* Wed Nov 15 2000 Solar Designer <solar-at-owl.openwall.com>
- Checked procmail for a number of possible problems in the handling of
.procmailrc files, produced a patch.
- Decided against installing anything SGID by default (fcntl locking is
sufficient most of the time); owl-control files are to be added.
- Based this spec file on Red Hat's, but changed it heavily.
