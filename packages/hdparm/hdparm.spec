# $Id: Owl/packages/hdparm/hdparm.spec,v 1.1 2001/03/27 09:35:33 mci Exp $

Summary: A utility for displaying and/or setting hard disk parameters.
Name: hdparm
Version: 4.1
Release: 1owl
Copyright: BSD
Group: Applications/System
Source: http://www.ibiblio.org/pub/Linux/system/hardware/%{name}-%{version}.tar.gz
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root

%description
hdparm - get/set hard disk parameters for Linux IDE drives.

%prep
%setup -q

%build
perl -pi -e "s,-O2,$RPM_OPT_FLAGS,g" Makefile
make

%install
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/usr/doc
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
install -c -s -m 755 hdparm $RPM_BUILD_ROOT/sbin/hdparm
install -c -m 644 hdparm.8 $RPM_BUILD_ROOT/%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc hdparm.lsm Changelog
/sbin/hdparm
%{_mandir}/man8/hdparm.8*

%changelog
* Tue Mar 27 2001 Michail Litvak <mci@owl.openwall.com>
- Import spec from RH.
- version 4.1

* Wed Jul 19 2000 Bernhard Rosenkränzer <bero@redhat.com>
- disable readahead (#14268)
- add comment in /etc/sysconfig/harddisks about possible extra parameters

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable 32 bit interfacing (#13730)

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- add /etc/sysconfig/harddisks, a new file for hardisk 
  optimization parameters

* Mon Jun 18 2000 Bernhard Rosenkränzer <bero@redhat.com>
- FHSify

* Sun Apr  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix compilation with kernel 2.3.*

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 3.9
- handle RPM_OPT_FLAGS

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Use O_NONBLOCK when opening devices so we can manipulate CD-ROM drives
  with no media inserted, even when running a current kernel (Bug #6457)

* Sat Feb  5 2000 Bill Nottingham <notting@redhat.com>
- build as non-root user (#6458)

* Fri Feb  4 2000 Bernhard Rosenkränzer <bero@redhat.com>
- deal with RPM compressing man pages

* Fri Nov 19 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.6

* Thu Aug 12 1999 Cristian Gafton <gafton@redhat.com>
- version 3.5

* Wed Mar 24 1999 Cristian Gafton <gafton@redhat.com>
- added patches from UP

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 3.3
- build rooted

* Fri Oct 31 1997 Donnie Barnes <djb@redhat.com>
- fixed spelling error in summary

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

