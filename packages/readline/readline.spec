# $Id: Owl/packages/readline/readline.spec,v 1.7 2001/07/06 03:22:42 solar Exp $

Summary: A library for editing typed in command lines.
Name: readline
Version: 4.1
Release: 8owl
Copyright: GPL
Group: System Environment/Libraries
Source: ftp://ftp.gnu.org/gnu/readline-%{version}.tar.gz
Patch0: readline-4.1-rh-guard.diff
Patch1: readline-4.1-deb-doc_makefile.diff
Patch2: readline-4.1-deb-inputrc.diff
Patch3: readline-4.1-deb-del_bcksp.diff
Patch4: readline-4.1-deb-char.diff
Prereq: /sbin/install-info /sbin/ldconfig
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root
BuildRequires: sed
Provides: libreadline.so.3 libreadline.so.3.0

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}


%description
The readline library reads a line from the terminal and returns it,
allowing the user to edit the line with standard emacs editing keys.
The readline library allows programmers to provide an easy to use and
more intuitive interface for users.

If you want to develop programs that will use the readline library,
you'll also need to install the readline-devel package.

%package devel
Summary: Files needed to develop programs which use the readline library.
Group: Development/Libraries
Requires: readline = %{version}

%description devel
The readline library will read a line from the terminal and return it.
Use of the readline library allows programmers to provide an easy
to use and more intuitive interface for users.

If you want to develop programs which will use the readline library,
you'll need to have the readline-devel package installed.  You'll also
need to have the readline package installed.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure
make all shared CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall install install-shared

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/examples
install -m 644 examples/* ${RPM_BUILD_ROOT}%{_docdir}/examples

chmod 755 ${RPM_BUILD_ROOT}/%{prefix}/lib/*.so*

cd ${RPM_BUILD_ROOT}
ln -sf libreadline.so.%{version} .%{_libdir}/libreadline.so
ln -sf libhistory.so.%{version} .%{_libdir}/libhistory.so
ln -sf libreadline.so.%{version} \
	.%{_libdir}/libreadline.so.`echo %{version} | sed 's^\..*^^g'`
ln -sf libhistory.so.%{version} \
  	.%{_libdir}/libhistory.so.`echo %{version} | sed 's^\..*^^g'`

# Hack !
ln -s libreadline.so.%{version} .%{_libdir}/libreadline.so.3
ln -s libreadline.so.%{version} .%{_libdir}/libreadline.so.3.0

%clean
rm -rf ${RPM_BUILD_ROOT}

%post 
/sbin/ldconfig
/sbin/install-info %{_infodir}/history.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/readline.info.gz %{_infodir}/dir

%postun -p /sbin/ldconfig

%preun
if [ "$1" -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/history.info.gz %{_infodir}/dir
  /sbin/install-info --delete %{_infodir}/readline.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/readline
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%doc %{_docdir}/examples/*

%changelog
* Fri Dec 08 2000 Michail Litvak <mci@owl.openwall.com>
- optflags_lib support.

* Wed Dec 06 2000 Michail Litvak <mci@owl.openwall.com>
- hack for compatibility with readline2  
- spec file cleanups

* Tue Dec 05 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- added Debian patches

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Wed Aug  2 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- use "rm -f" in specfile

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Tue Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.1

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0

* Fri Apr 09 1999 Michael K. Johnson <johnsonm@redhat.com>
- added guard patch from Taneli Huuskonen <huuskone@cc.helsinki.fi>

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.2.1

* Wed May 06 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- don't package /usr/info/dir

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- devel package moved to Development/Libraries

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- added proper sonames

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- updated to readline 2.1

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc
