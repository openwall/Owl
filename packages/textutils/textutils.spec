# $Id: Owl/packages/textutils/Attic/textutils.spec,v 1.5 2001/01/26 05:46:07 solar Exp $

Summary: A set of GNU text file modifying utilities.
Name: 		textutils
Version: 	2.0.11
Release: 	2owl
Copyright: 	GPL
Group: 		Applications/Text
Source: 	ftp://alpha.gnu.org/gnu/fetish/textutils-%{version}.tar.gz
Patch0:		textutils-2.0.11-owl-tmp.diff
Patch1:		textutils-2.0.11-owl-sort-size.diff
Prereq: 	/sbin/install-info
BuildPrereq: 	libtool
BuildRoot:      /var/rpm-buildroot/%{name}-root

%description
A set of GNU utilities for modifying the contents of files, including
programs for splitting, joining, comparing and modifying files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
unset LINGUAS || :
export ac_cv_sys_long_file_names=yes \
%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=$RPM_BUILD_ROOT

%ifos linux
    mkdir -p $RPM_BUILD_ROOT/bin
    for f in cat sort; do
	mv $RPM_BUILD_ROOT/usr/bin/$f $RPM_BUILD_ROOT/bin/$f
    done
%endif

gzip -9nf $RPM_BUILD_ROOT/%{_infodir}/textutils*

%post
/sbin/install-info %{_infodir}/textutils.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete \
		%{_infodir}/textutils.info.gz %{_infodir}/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README
%ifos linux
/bin/*
%endif
/usr/bin/*
%{_mandir}/*/*
%{_infodir}/textutils*
/usr/share/locale/*/*/*

%changelog
* Fri Jan 26 2001 Solar Designer <solar@owl.openwall.com>
- Patched the flawed memory allocation strategy in sort(1) introduced
with 2.0.11.

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- 2.0.11
- DoS attack fixes for tac and sort (O_EXCL -> mkstemp).

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.0.8 (+sha1sum)

* Sun Jul 30 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- imported from RH

* Thu Jun 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 6.2 release, which doesn't use %%makeinstall

* Thu Jun 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
- minor cleanup for errata release
- lose %%{_prefix}
- don't include the broken patches

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Wed May  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- BuildPreqeq: libtool (Bug #11106)

* Mon Apr 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disabled patches, to make "-n" work. This may cause some problems
  due to glibc sorting weirdness which Cristian is fixing seperately.

* Sun Apr  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 2.0e

* Mon Jan  7 2000 Jakub Jelinek <jakub@redhat.com>
- Revert comm and join to old behaviour (binary sorting).
  Add new switch "-l" to both. If sort -l is used to generate
  input, comm -l/join -l should be used on that, otherwise
  -l should not be specified.

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 2.0a
- Revert sort to old behavior (binary sorting).
  Add new switch "-l" to handle locales (the way 2.0 did)
  (Bugs #7020, #7828, #8021, #8125)
- unset LINGUAS before running configure
- fix a bug in the spec file (it's rm -rf, not rm -f)

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 2.0.
- fix tsort conflicts (by eliminating tsort from util-linux).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan rebuild

* Fri Mar 06 1998 Michael K. Johnson <johnsonm@redhat.com>
- made tmpfile creation safe (even for root) in sort and tac.

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- added patch for glibc 2.1

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- Rebuilt against glibc
