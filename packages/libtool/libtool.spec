# $Id: Owl/packages/libtool/libtool.spec,v 1.3 2001/05/06 14:59:55 solar Exp $

Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: 		libtool
Version: 	1.3.5
Release: 	9owl
Copyright: 	GPL
Group: 		Development/Tools
Source: 	ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Patch1: 	libtool-1.2f-rh-cache.diff
Patch2: 	libtool-1.3.5-rh-mktemp.diff
Patch3: 	libtool-1.3.5-rh-nonneg.diff
Prefix: 	%{_prefix}
PreReq: 	/sbin/install-info autoconf automake m4 perl
Requires: 	libtool-libs = %{version}-%{release}, mktemp
Buildroot:      /var/rpm-buildroot/%{name}-root

%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, you
should install libtool.

%package libs
Summary: Runtime libraries for GNU libtool.
Group: System Environment/Libraries

%description libs
The libtool-libs package contains the runtime libraries from GNU
libtool.  GNU libtool uses these libraries to provide portible dynamic
loading of shared libraries.

If you are using some programs that provide shared libraries built
with GNU libtool, you should install the libtool-libs package to
provide the dynamic loading library

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
#./configure --prefix=%{_prefix}
# define libtoolize to true, in case configure calls it
%define __libtoolize /bin/true
%configure

make -k -C doc
make

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

#make prefix=${RPM_BUILD_ROOT}%{_prefix} install
%makeinstall

cp install-sh missing mkinstalldirs demo

chmod -R u=rwX,go=rX demo

cd ${RPM_BUILD_ROOT}
gzip -9nf .%{_infodir}/*.info*
# XXX remove zero length file
rm -f .%{_datadir}/libtool/libltdl/stamp-h.in
# XXX forcibly break hardlinks
mv .%{_datadir}/libtool/libltdl .%{_datadir}/libtool/libltdl-X
mkdir .%{_prefix}/share/libtool/libltdl
cp .%{_datadir}/libtool/libltdl-X/* .%{_datadir}/libtool/libltdl
rm -rf .%{_prefix}/share/libtool/libltdl-X

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/libtool.info.gz %{_infodir}/dir
# XXX hack alert
cd %{_defaultdocdir}/libtool-%{version}/demo || cd %{_prefix}/doc/libtool-%{version}/demo || exit 0
umask 022
libtoolize --copy --force
aclocal
autoheader
automake
autoconf

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/libtool.info.gz %{_infodir}/dir
# XXX hack alert
	cd %{_defaultdocdir}/libtool-%{version}/demo || cd %{_prefix}/doc/libtool-%{version}/demo || exit 0
	rm -f config.{guess,h.in,sub} lt{config,main.sh}
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
%doc THANKS TODO ChangeLog demo
%{_bindir}/*
%{_infodir}/libtool.info*
%{_includedir}/ltdl.h
%{_datadir}/libtool
%{_libdir}/libltdl.so
%{_libdir}/libltdl.*a
%{_datadir}/aclocal/libtool.m4

%files libs
%defattr(-,root,root)
%{_libdir}/libltdl.so.*

%changelog
* Sun May 06 2001 Solar Designer <solar@owl.openwall.com>
- Ensure proper permissions on demo (installed as documentation).

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Thu Jul 13 2000 Elliot Lee <sopwith@redhat.com>
- Fix recognition of ^0[0-9]+$ as a non-negative integer.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch to use mktemp to create the tempdir
- use %%configure after defining __libtoolize to /bin/true

* Mon Jul  3 2000 Matt Wilson <msw@redhat.com>
- subpackage libltdl into libtool-libs

* Sun Jun 18 2000 Bill Nottingham <notting@redhat.com>
- running libtoolize on the libtool source tree ain't right :)

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.3.5.

* Fri Mar  3 2000 Jeff Johnson <jbj@redhat.com>
- add prereqs for m4 and perl inorder to run autoconf/automake.

* Mon Feb 28 2000 Jeff Johnson <jbj@redhat.com>
- functional /usr/doc/libtool-*/demo by end-user %post procedure (#9719).

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.4.

* Mon Dec  6 1999 Jeff Johnson <jbj@redhat.com>
- change from noarch to per-arch in order to package libltdl.a (#7493).

* Thu Jul 15 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.3.

* Mon Jun 14 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.2.

* Tue May 11 1999 Jeff Johnson <jbj@redhat.com>
- explicitly disable per-arch libraries (#2210)
- undo hard links and remove zero length file (#2689)

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- disable the --cache-file passing to ltconfig; this breaks the older
  ltconfig scripts found around.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 2)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.2f

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- completed arm patch
- added patch to make it more arm-friendly
- upgrade to version 1.2d

* Thu May 07 1998 Donnie Barnes <djb@redhat.com>
- fixed busted group

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- Update to 1.0h
- added install-info support

* Tue Nov 25 1997 Elliot Lee <sopwith@redhat.com>
- Update to 1.0f
- BuildRoot it
- Make it a noarch package
