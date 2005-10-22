# $Id: Owl/packages/m4/m4.spec,v 1.15 2005/10/22 08:34:15 solar Exp $

Summary: The GNU macro processor.
Name: m4
Version: 1.4.4
Release: owl1
License: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/m4/m4-%version.tar.bz2
Source1: m4.m4
Patch0: m4-1.4.3-owl-info.diff
Patch1: m4-1.4.3-alt-glibc.diff
Patch2: m4-1.4.3-alt-error.diff
Patch3: m4-1.4.4-owl-warnings.diff
PreReq: /sbin/install-info
# due to sed -i
BuildRequires: sed >= 4.1.1
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
A GNU implementation of the traditional Unix macro processor.  m4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  m4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# use prototypes from glibc
rm lib/*.h
# fix tmp file handling in test suite
sed -i -e s,/tmp,., checks/check-them

%{expand:%%define optflags %optflags -Wall}

%build
autoreconf -fisv
export ac_cv_func_mkstemp=yes \
%configure
%__make CFLAGS="%optflags" LDFLAGS=-s
%__make -k check

%install
rm -rf %buildroot
%makeinstall INSTALL_DATA="install -c -m 644"
install -pD -m644 %_sourcedir/m4.m4 %buildroot%_datadir/aclocal/m4.m4

%post
/sbin/install-info %_infodir/m4.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/m4.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc NEWS README
%_bindir/m4
%_infodir/*.info*
%_datadir/aclocal/m4.m4

%changelog
* Sat Oct 22 2005 Dmitry V. Levin <ldv@owl.openwall.com> 1.4.4-owl1
- Updated to 1.4.4.
- Corrected info files installation.
- Packaged %_datadir/aclocal/m4.m4 from autoconf-2.59 sources.
- Applied ALT's build change to use getopt, error, libintl, and obstack
implementations from glibc rather than build them statically in this package.

* Fri Oct 21 2005 Alexandr D. Kanevskiy <kad@owl.openwall.com> 1.4.3-owl1
- Updated to 1.4.3.

* Thu Feb 26 2004 Michail Litvak <mci@owl.openwall.com> 1.4-owl17
- Fixed building with new auto* tools.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 1.4-owl16
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Feb 06 2001 Michail Litvak <mci@owl.openwall.com>
- Fixed format bug in error
- added __attribute__ ((format(...))) for error

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
