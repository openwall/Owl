# $Id: Owl/packages/tar/tar.spec,v 1.2 2000/08/09 03:38:59 solar Exp $

Summary: A GNU file archiving program.
Name: 		tar
Version:	1.13.17
Release: 	6owl
Copyright: 	GPL
Group: 		Applications/Archiving
Source: 	ftp://alpha.gnu.org/pub/gnu/tar/tar-%{version}.tar.gz
Patch0: 	tar-1.13.14-rh-manpage.diff
Patch1: 	tar-1.13.17-rh-fnmatch.diff
Patch2: 	tar-1.3.17-rh-excluded_name.diff
Prereq: 	/sbin/install-info
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
The GNU tar program saves many files together into one archive and can
restore individual files (or all of the files) from the archive.  Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you'll also need to install
the rmt package.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%ifos linux
unset LINGUAS || :
%define optflags $RPM_OPT_FLAGS -DHAVE_STRERROR -D_GNU_SOURCE
%configure --bindir=/bin --libexecdir=/sbin
make LIBS=-lbsd
%else
%configure
make
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ifos linux
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
    bindir=${RPM_BUILD_ROOT}/bin \
    libexecdir=${RPM_BUILD_ROOT}/sbin \
    mandir=${RPM_BUILD_ROOT}%{_mandir} \
    infodir=${RPM_BUILD_ROOT}%{_infodir} \
	install
ln -s tar ${RPM_BUILD_ROOT}/bin/gtar
%else
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
    localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale \
    mandir=${RPM_BUILD_ROOT}%{_mandir} \
    infodir=${RPM_BUILD_ROOT}%{_infodir} \
	install
%endif

( cd $RPM_BUILD_ROOT
  for dir in ./bin ./sbin .%{_prefix}/bin .%{_prefix}/libexec
  do
    [ -d $dir ] || continue
    strip $dir/* || :
  done
  gzip -9nf .%{_infodir}/tar.info*
  rm -f .%{_infodir}/dir
)

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
install -c -m644 tar.1 ${RPM_BUILD_ROOT}%{_mandir}/man1

%post
/sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%ifos linux
/bin/tar
/bin/gtar
%{_mandir}/man1/tar.1*
%else
%{_prefix}/bin/*
%{_prefix}/libexec/*
%{_mandir}/man*/*
%endif

%{_infodir}/tar.info*
%{_prefix}/share/locale/*/LC_MESSAGES/*

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevsiy <kad@owl.openwall.com>
- import from RH
- fix URL

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix for ia64

* Wed Feb  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix the exclude bug (#9201)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- fix fnmatch build problems

* Sun Jan  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.17
- remove dotbug patch (fixed in base)
- update download URL

* Fri Jan  7 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix a severe bug (tar xf any_package_containing_. would delete the
  current directory)

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.3.16
- unset LINGUAS before running configure

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.14
- Update man page to know about -I / --bzip
- Remove dependancy on rmt - tar can be used for anything local
  without it.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.13.11.

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.9.

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.6.
- support -y --bzip2 options for bzip2 compression (#2415).

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.5.

* Tue Jul 13 1999 Bill Nottingham <notting@redhat.com>
- update to 1.13

* Sat Jun 26 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.12.64014.
- pipe patch corrected for remote tars now merged in.

* Sun Jun 20 1999 Jeff Johnson <jbj@redhat.com>
- update to tar-1.12.64013.
- subtract (and reopen #2415) bzip2 support using -y.
- move gtar to /bin.

* Tue Jun 15 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to tar-1.12.64011 to
-   add bzip2 support (#2415)
-   fix filename bug (#3479)

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- fix suspended tar with compression over pipe produces error (#390).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Michael Maher <mike@redhat.com>
- added patch for bad name cache. 
- FIXES BUG 320

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/gtar symlink (change #421)

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump.
- Turn on nls.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.11.8 to 1.12
- various spec file cleanups
- /sbin/install-info support

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu May 29 1997 Michael Fulbright <msf@redhat.com>
- Fixed to include rmt
