# $Id: Owl/packages/gdbm/gdbm.spec,v 1.1 2000/08/09 00:51:27 kad Exp $

%{expand: %%global _includedir %{_includedir}/gdbm}

Summary: A GNU set of database routines which use extensible hashing.
Name: 		gdbm
Version: 	1.8.0
Release: 	5owl
Source:		ftp://ftp.gnu.org/pub/gnu/gdbm-%{version}.tar.gz
Patch0: 	gdbm-1.8.0-rh-header.diff
Patch1: 	gdbm-1.8.0-rh-fhs.diff
Copyright: 	GPL
Group: 		System Environment/Libraries
Prefix: 	%{_prefix}
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
Gdbm is a GNU database indexing library, including routines which use
extensible hashing.  Gdbm works in a similar way to standard UNIX dbm
routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

If you're a C developer and your programs need access to simple
database routines, you should install gdbm.  You'll also need to
install gdbm-devel.

%package devel
Summary: Development libraries and header files for the gdbm library.
Group: Development/Libraries
Requires: gdbm
Prereq: /sbin/install-info

%description devel
Gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.

%prep
%setup -q
%patch0 -p 1
%patch1 -p 1 -b .fhs

%build

%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall install-compat

{ cd ${RPM_BUILD_ROOT}
  ln -sf gdbm/gdbm.h .%{_oldincludedir}/gdbm.h
  ln -sf libgdbm.so.2.0.0 .%{_libdir}/libgdbm.so
  gzip -9nf .%{_infodir}/gdbm*
  rm -f .%{_infodir}/dir
}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/gdbm.info.gz %{_infodir}/dir --entry="* gdbm: (gdbm).                   The GNU Database."

%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gdbm.info.gz %{_infodir}/dir --entry="* gdbm: (gdbm).                   The GNU Database."
fi

%files
%defattr(-,root,root)
%{_libdir}/libgdbm.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libgdbm.so
%{_libdir}/libgdbm.la
%{_libdir}/libgdbm.a
%{_oldincludedir}/gdbm.h
%{_includedir}
%{_infodir}/*.info*
%{_mandir}/man3/*

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- fix URL

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- make sure created database header is initialized (#4457).

* Tue Jun  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.8.0.
- repackage to include /usr/include/gdbm/*dbm.h compatibility includes.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 19)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- gdbm-devel moved to Development/Libraries

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- buildroot and built for Manhattan

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc
