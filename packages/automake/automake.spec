# $Id: Owl/packages/automake/automake.spec,v 1.1 2000/08/09 00:51:27 kad Exp $

Summary: A GNU tool for automatically creating Makefiles.
Name: 		automake
Version: 	1.4
Release: 	8owl
Copyright: 	GPL
Group: 		Development/Tools
Source: 	ftp://ftp.gnu.org/pub/gnu/automake/automake-%{version}.tar.gz
Patch: 		automake-1.4-rh-copytosourcedir.diff
URL: 		http://sourceware.cygnus.com/automake
Requires: 	perl
Prereq: 	/sbin/install-info
BuildArchitectures: noarch
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
Automake is an experimental Makefile generator. Automake was inspired
by the 4.4BSD make and include files, but aims to be portable and to
conform to the GNU standards for Makefile variables and targets.

You should install Automake if you are developing software and would
like to use its capabilities of automatically generating GNU
standard Makefiles. if you install Automake, you will also need to
install GNU's Autoconf package.

%prep
%setup -q
%patch -p0 -b .copytosourcedir

%build

%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/automake*

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/automake.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/automake.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake
%{_datadir}/aclocal

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bug #8870

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- revert to pristine automake-1.4.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- arm netwinder patch

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- add patches from CVS for 6.0beta1

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.4.

* Mon Nov 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.3b.
- add URL.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to 1.3

* Tue Oct 28 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot; added aclocal files

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- made it a noarch package

* Thu Oct 16 1997 Michael Fulbright <msf@redhat.com>
- Fixed some tag lines to conform to 5.0 guidelines.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- updated to 1.2

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- first version (1.0)
