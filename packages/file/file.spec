# $Id: Owl/packages/file/file.spec,v 1.1 2000/11/29 12:01:01 mci Exp $

Summary: A utility for determining file types.
Name: file
Version: 3.33
Release: 1owl
Copyright: distributable
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Patch0: file-3.33-rh-fnovfl.diff
Patch1: file-3.33-rh-ia64.diff
Patch2: file-3.33-deb-magic.diff
Patch3: file-3.33-deb-magi2mime.diff
Patch4: file-3.33-deb-make.diff
Prefix: %{_prefix}
BuildRoot: /var/rpm-buildroot/%{name}-root

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

automake
%configure
make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/magic*
%{_mandir}/man*/*

%changelog

* Thu Nov 29 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH and updated to 3.33
- added some patches from Debian and RH

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- Bill made the patch but didn't apply it. :)

* Mon Aug 14 2000 Bill Nottingham <notting@redhat.com>
- 'ASCII text', not 'ASCII test' (#16168)

* Mon Jul 31 2000 Jeff Johnson <jbj@redhat.com>
- fix off-by-1 error when creating filename for use with -i.
- include a copy of GNOME /etc/mime-types in %{_datadir}/magic.mime (#14741).

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- install magic as man5/magic.5 with other formats (#11172).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 14 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Tue Apr 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.30

* Wed Feb 16 2000 Cristian Gafton <gafton@redhat.com>
- add ia64 patch from rth

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages
- update to 3.28

* Mon Aug 23 1999 Jeff Johnson <jbj@redhat.com>
- identify ELF stripped files correctly (#4665).
- use SPARC (not sparc) consistently throughout (#4665).
- add entries for MS Office files (#4665).

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- diddle magic so that *.tfm files are identified correctly.

* Tue Jul  6 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.27.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- experimental support for realmedia files added

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binary.

* Fri Nov 27 1998 Jakub Jelinek <jj@ultra.linux.cz>
- add SPARC V9 magic.

* Tue Nov 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.26.

* Mon Aug 24 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.25.
- detect gimp XCF versions.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 3.24
- buildrooted

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Mon Mar 31 1997 Erik Troan <ewt@redhat.com>
- Fixed problems caused by 64 bit time_t.

* Thu Mar 06 1997 Michael K. Johnson <johnsonm@redhat.com>
- Improved recognition of Linux kernel images.
