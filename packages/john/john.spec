# $Id: Owl/packages/john/john.spec,v 1.2 2002/04/10 14:22:50 solar Exp $

Summary: John the Ripper password cracker.
Name: john
Version: 1.6.31.1
Release: owl1
License: GPL
Group: Applications/System
Source0: ftp://ftp.openwall.com/pub/projects/john/john-%{version}.tar.gz
Source1: ftp://ftp.openwall.com/pub/projects/john/john-1.6.tar.gz
BuildRoot: /override/%{name}-%{version}

%description
John the Ripper is a fast password cracker (password security auditing
tool).  Its primary purpose is to detect weak Unix passwords, but a number
of other hash types are supported as well. 

%prep
%setup -q -a 1

%define cflags -c %optflags -Wall -DJOHN_SYSTEMWIDE=1

%build
cd src
%ifarch i686 i786 i886 i986
make linux-x86-mmx-elf CFLAGS='%cflags'
%else
%ifarch %ix86
make linux-x86-any-elf CFLAGS='%cflags'
%endif
%endif
%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
make linux-alpha CFLAGS='%cflags'
%endif
%ifarch sparc sparcv9
make linux-sparc CFLAGS='%cflags'
%endif
%ifarch ppc
make linux-ppc CFLAGS='%cflags'
%endif

%install
mkdir -p $RPM_BUILD_ROOT{%_bindir,%_datadir/john}
install -m 700 run/john $RPM_BUILD_ROOT%_bindir/
cp -a run/un* $RPM_BUILD_ROOT%_bindir/
install -m 644 run/{john.conf,password.lst} john-1.6/run/*.chr \
	$RPM_BUILD_ROOT%_datadir/john/
install -m 644 -p run/mailer doc/
mkdir doc/john-1.6
cp -a john-1.6/doc/* doc/john-1.6/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/*
%attr(750,root,wheel) %_bindir/john
%_bindir/un*
%dir %_datadir/john
%attr(640,root,wheel) %config(noreplace) %_datadir/john/john.conf
%attr(644,root,root) %_datadir/john/password.lst
%attr(644,root,root) %_datadir/john/*.chr

%changelog
* Wed Apr 10 2002 Solar Designer <solar@owl.openwall.com>
- Packaged 1.6.31-dev for Owl, with minor modifications.
