%define NEED_PYTHON 'no'
%define version 3.0.5

Summary: The Red Hat package management system.
Name: 		rpm
Version: 	%{version}
Release: 	7.0.8owl
Group: 		System Environment/Base
Source: 	ftp://ftp.rpm.org/pub/rpm/dist/rpm-3.0.x/rpm-%{version}.tar.gz
Copyright: 	GPL
Conflicts: 	patch < 2.5
%ifos linux
Prereq: 	gawk fileutils textutils sh-utils mktemp
BuildRequires: 	bzip2 >= 0.9.0c-2
Requires: 	popt, bzip2 >= 0.9.0c-2
%endif
%if "%{NEED_PYTHON}"=="'yes'"
BuildRequires: 	python-devel >= 1.5.2
%endif
BuildRoot: /var/tmp/%{name}-root

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages.  Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package devel
Summary: Development files for applications which will manipulate RPM packages.
Group: Development/Libraries
Requires: rpm = %{version}, popt

%description devel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs which
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages.
Group: Development/Tools
Requires: rpm = %{version}

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.

%if "%{NEED_PYTHON}"=="'yes'"
%package python
Summary: Python bindings for apps which will manipulate RPM packages.
Group: Development/Libraries
BuildRequires: popt >= 1.5
Requires: popt >= 1.5
Requires: python >= 1.5.2

%description python
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.
%endif

%package -n popt
Summary: A C library for parsing command line parameters.
Group: Development/Libraries
Version: 1.5

%description -n popt
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

Install popt if you're a C programmer and you'd like to use its
capabilities.

%prep
%setup -q

%build
unset LINGUAS || :
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
make
%if "%{NEED_PYTHON}"=="'yes'"
make -C python
%endif

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install
%if "%{NEED_PYTHON}"=="'yes'"
make DESTDIR="$RPM_BUILD_ROOT" install -C python
%endif
%ifos linux
mkdir -p $RPM_BUILD_ROOT/etc/rpm
%endif

{ cd $RPM_BUILD_ROOT
  strip ./bin/rpm
  strip ./usr/bin/rpm2cpio
  strip ./usr/lib/rpm/rpmputtext ./usr/lib/rpm/rpmgettext
}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/rpm --initdb
%ifos linux
if [ ! -e /etc/rpm/macros -a -e /etc/rpmrc -a -f /usr/lib/rpm/convertrpmrc.sh ] 
then
	sh /usr/lib/rpm/convertrpmrc.sh > /dev/null 2>&1
fi
%endif

%ifos linux
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%post -n popt -p /sbin/ldconfig
%postun -n popt -p /sbin/ldconfig
%endif

%if "%{NEED_PYTHON}"=="'yes'"
%post python -p /sbin/ldconfig
%postun python -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc RPM-PGP-KEY CHANGES GROUPS doc/manual/*
/bin/rpm
%ifos linux
%dir /etc/rpm
%endif
/usr/bin/rpm2cpio
/usr/bin/gendiff
/usr/lib/librpm.so.*
/usr/lib/librpmbuild.so.*

/usr/lib/rpm/brp-*
/usr/lib/rpm/config.guess
/usr/lib/rpm/config.sub
/usr/lib/rpm/convertrpmrc.sh
/usr/lib/rpm/find-prov.pl
/usr/lib/rpm/find-provides
/usr/lib/rpm/find-req.pl
/usr/lib/rpm/find-requires
/usr/lib/rpm/macros
/usr/lib/rpm/mkinstalldirs
/usr/lib/rpm/rpmpopt
/usr/lib/rpm/rpmrc
/usr/lib/rpm/vpkg-provides.sh
/usr/lib/rpm/vpkg-provides2.sh

%ifarch i386 i486 i586 i686
/usr/lib/rpm/i[3456]86*
%endif
%ifarch alpha
/usr/lib/rpm/alpha*
%endif
%ifarch sparc sparc64
/usr/lib/rpm/sparc*
%endif
%ifarch ia64
/usr/lib/rpm/ia64*
%endif
%ifarch powerpc ppc
/usr/lib/rpm/ppc*
%endif

%dir /usr/src/redhat
%dir /usr/src/redhat/BUILD
%dir /usr/src/redhat/SPECS
%dir /usr/src/redhat/SOURCES
%dir /usr/src/redhat/SRPMS
%dir /usr/src/redhat/RPMS
/usr/src/redhat/RPMS/*
/usr/*/locale/*/LC_MESSAGES/rpm.mo
/usr/man/man[18]/*.[18]*
%lang(pl) /usr/man/pl/man[18]/*.[18]*
%lang(ru) /usr/man/ru/man[18]/*.[18]*

%files build
%defattr(-,root,root)
/usr/lib/rpm/check-prereqs
/usr/lib/rpm/cpanflute
/usr/lib/rpm/find-lang.sh
/usr/lib/rpm/find-provides.perl
/usr/lib/rpm/find-requires.perl
/usr/lib/rpm/get_magic.pl
/usr/lib/rpm/getpo.sh
/usr/lib/rpm/http.req
/usr/lib/rpm/magic.prov
/usr/lib/rpm/magic.req
/usr/lib/rpm/perl.prov
/usr/lib/rpm/perl.req
/usr/lib/rpm/rpmdiff
/usr/lib/rpm/rpmdiff.cgi
/usr/lib/rpm/rpmgettext
/usr/lib/rpm/rpmputtext
/usr/lib/rpm/u_pkg.sh

%if "%{NEED_PYTHON}"=="'yes'"
%files python
%defattr(-,root,root)
/usr/lib/python1.5/site-packages/rpmmodule.so
%endif

%files devel
%defattr(-,root,root)
/usr/include/rpm
/usr/lib/librpm.a
/usr/lib/librpm.la
/usr/lib/librpm.so
/usr/lib/librpmbuild.a
/usr/lib/librpmbuild.la
/usr/lib/librpmbuild.so

%files -n popt
%defattr(-,root,root)
/usr/lib/libpopt.so.*
/usr/*/locale/*/LC_MESSAGES/popt.mo
/usr/man/man3/popt.3*

# XXX These may end up in popt-devel but it hardly seems worth the effort now.
/usr/lib/libpopt.a
/usr/lib/libpopt.la
/usr/lib/libpopt.so
/usr/include/popt.h

%changelog
* Sun Jul 16 2000 Jeff Johnson <jbj@redhat.com>
- remove (unused) RPMTAG_CAPABILITY.
- remove (legacy) use of RPMTAG_{OBSOLETES,PROVIDES} internally.
- remove (legacy) support for version 1 packaging.
- remove (legacy) support for converting gdbm databases.
- eliminate unused headerGz{Read,Write}.
- support for rpmlib(...) internal feature dependencies.
- display rpmlib provides when invoked with --showrc.
- fix: compare versions if doing --freshen.

* Tue Jul 11 2000 Jeff Johnson <jbj@redhat.com>
- identify package when install scriptlet fails (#12448).

* Sun Jul  9 2000 Jeff Johnson <jbj@redhat.com>
- fix: payload compression tag not nul terminated.

* Thu Jun 22 2000 Jeff Johnson <jbj@redhat.com>
- internalize --freshen (Gordon Messmer <yinyang@eburg.com>).
- support for separate source/binary compression policy.
- support for bzip payloads.

* Wed Jun 21 2000 Jeff Johnson <jbj@redhat.com>
- fix: don't expand macros in false branch of %if (kasal@suse.cz).
- fix: macro expansion problem and clean up (#11484) (kasal@suse.cz).
- uname on i370 has s390 as arch (#11456).
- python: initdb binding (Dan Burcaw <dburcaw@terraplex.com>).

* Tue Jun 20 2000 Jeff Johnson <jbj@redhat.com>
- handle version 4 packaging as input.
- builds against bzip2 1.0
- fix: resurrect symlink unique'ifying property of finger prints.
- fix: broken glob test with empty build directory (Geoff Keating).
- fix: create per-platform directories correctly.
- update brp-* scripts from rpm-4.0, enable in per-platform config.
- alpha: add -mieee to default optflags.
- add RPMTAG_OPTFLAGS, configured optflags when package was built.
- add RPMTAG_DISTURL for rpmfind-like tools (content unknown yet).
- teach brp-compress about /usr/info and /usr/share/info as well.
- update macros.in from rpm-4.0 (w/o dbi configuration).

* Thu Mar 15 2000 Jeff Johnson <jbj@redhat.com>
- portability: skip bzip2 if not available.
- portability: skip gzseek if not available (zlib-1.0.4).
- portability: skip personality if not available (linux).
- portability: always include arpa/inet.h (HP-UX).
- portability: don't use id -u (Brandon Allbery).
- portability: don't chown/chgrp -h w/o lchown.
- portability: splats in rpm.spec to find /usr/{share,local}/locale/*
- fix: better filter in linux.req to avoid ARM specific objdump output.
- fix: use glibc 2.1 glob/fnmatch everywhere.
- fix: noLibio = 0 on Red Hat 4.x and 5.x.
- fix: typo in autodeps/linux.req.

* Thu Mar  2 2000 Jeff Johnson <jbj@redhat.com>
- simpler hpux.prov script (Tim Mooney).

* Wed Mar  1 2000 Jeff Johnson <jbj@redhat.com>
- fix rpmmodule.so python bindings.

* Sun Feb 27 2000 Jeff Johnson <jbj@redhat.com>
- rpm-3.0.4 release candidate.

* Fri Feb 25 2000 Jeff Johnson <jbj@redhat.com>
- fix: filter excluded paths before adding install prefixes (#8709).
- add i18n lookaside to PO catalogue(s) for i18n strings.
- try for /etc/rpm/macros.specspo so that specspo autoconfigures rpm.
- per-platform configuration factored into /usr/lib/rpm subdir.

* Tue Feb 15 2000 Jeff Johnson <jbj@redhat.com>
- new rpm-build package to isolate rpm dependencies on perl/bash2.
- always remove duplicate identical package entries on --rebuilddb.
- add scripts for autogenerating CPAN dependencies.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- brp-compress deals with hard links correctly.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- brp-compress deals with symlinks correctly.

* Mon Jan 24 2000 Jeff Johnson <jbj@redhat.com>
- explicitly expand file lists in writeRPM for rpmputtext.
