# $Id: Owl/packages/procmail/procmail.spec,v 1.2 2001/05/10 17:48:54 solar Exp $

Summary: The procmail mail processing program.
Name: procmail
Version: 3.15
Release: 2owl
Copyright: GPL or Artistic License
Group: System Environment/Daemons
Source0: ftp://ftp.procmail.org/pub/procmail/procmail-%{version}.tar.gz
Patch0: procmail-3.15-owl-config.diff
Patch1: procmail-3.15-owl-fixes.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}

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

make \
    BASENAME=${RPM_BUILD_ROOT}%{_prefix} MANDIR=${RPM_BUILD_ROOT}%{_mandir} \
	install

strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc FAQ HISTORY README KNOWN_BUGS FEATURES COPYING Artistic examples
%attr(755,root,root)	%{_bindir}/formail
%attr(755,root,root)	%{_bindir}/lockfile
%attr(755,root,root)	%{_bindir}/mailstat
%attr(755,root,root)	%{_bindir}/procmail
%{_mandir}/man[15]/*

%changelog
* Thu May 10 2001 Solar Designer <solar@owl.openwall.com>
- Don't let procmail get linked against -lnet (our libnet isn't what
procmail thinks it is).

* Wed Nov 15 2000 Solar Designer <solar@owl.openwall.com>
- Checked procmail for a number of possible problems in the handling of
.procmailrc files, produced a patch.
- Decided against installing anything SGID by default (fcntl locking is
sufficient most of the time); owl-control files are to be added.
- Based this spec file on Red Hat's, but changed it heavily.
