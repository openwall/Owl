# $Id: Owl/packages/procmail/procmail.spec,v 1.3 2002/02/07 18:42:15 solar Exp $

Summary: The procmail mail processing program.
Name: procmail
Version: 3.15
Release: owl2
License: GPL or Artistic License
Group: System Environment/Daemons
Source: ftp://ftp.procmail.org/pub/procmail/procmail-%{version}.tar.gz
Patch0: procmail-3.15-owl-config.diff
Patch1: procmail-3.15-owl-fixes.diff
BuildRoot: /override/%{name}-%{version}

%description
procmail is a mail processing program which can be used to filter,
sort, or selectively forward e-mail messages.  Optionally, procmail
may be installed as the local delivery agent.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make \
	LOCKINGTEST=100 \
	SEARCHLIBS="-lm -lnsl -ldl" \
	CC=gcc \
	CFLAGS0="$RPM_OPT_FLAGS -Wall -Wno-comment -Wno-parentheses"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,5}

make install \
	BASENAME=${RPM_BUILD_ROOT}%{_prefix} \
	MANDIR=${RPM_BUILD_ROOT}%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc FAQ HISTORY README KNOWN_BUGS FEATURES COPYING Artistic examples
%attr(755,root,root) %{_bindir}/formail
%attr(755,root,root) %{_bindir}/lockfile
%attr(755,root,root) %{_bindir}/mailstat
%attr(755,root,root) %{_bindir}/procmail
%{_mandir}/man[15]/*

%changelog
* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu May 10 2001 Solar Designer <solar@owl.openwall.com>
- Don't let procmail get linked against -lnet (our libnet isn't what
procmail thinks it is).

* Wed Nov 15 2000 Solar Designer <solar@owl.openwall.com>
- Checked procmail for a number of possible problems in the handling of
.procmailrc files, produced a patch.
- Decided against installing anything SGID by default (fcntl locking is
sufficient most of the time); owl-control files are to be added.
- Based this spec file on Red Hat's, but changed it heavily.
