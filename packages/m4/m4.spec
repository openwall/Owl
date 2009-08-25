# $Owl: Owl/packages/m4/m4.spec,v 1.20 2009/08/25 08:12:19 mci Exp $

Summary: The GNU macro processor.
Name: m4
Version: 1.4.13
Release: owl1
License: GPLv3+
Group: Applications/Text
URL: http://www.gnu.org/software/m4/
Source0: ftp://ftp.gnu.org/gnu/m4/m4-%version.tar.bz2
# Signature: ftp://ftp.gnu.org/gnu/m4/m4-%version.tar.bz2.sig
Source1: m4.m4
Patch0: m4-1.4.13-owl-info.diff
PreReq: /sbin/install-info
# due to sed -i
BuildRequires: sed >= 4.1.1
BuildRequires: texinfo
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
#rm lib/*.h
# fix tmp file handling in test suite
sed -i 's,/tmp,.,' checks/check-them

%{expand:%%define optflags %optflags -Wall}

%build
#autoreconf -fisv
# Build with included regex from gnulib until our glibc is updated.
# The regex.h must be kept in sync with --without-included-regex.
#install -pm644 %_includedir/regex.h gnulib/lib/
export ac_cv_func_mkstemp=yes \
%configure #--without-included-regex
%__make CFLAGS="%optflags" LDFLAGS=-s
%__make -k check

%install
rm -rf %buildroot
%makeinstall INSTALL_DATA="install -c -m 644"
install -pD -m644 %_sourcedir/m4.m4 %buildroot%_datadir/aclocal/m4.m4

# Remove unpackaged files
rm %buildroot%_infodir/dir

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
%_mandir/man1/m4.*
%_infodir/*.info*
%_datadir/aclocal/m4.m4

%changelog
* Tue Aug 25 2009 Michail Litvak <mci-at-owl.openwall.com> 1.4.13-owl1
- Updated to 1.4.13.
- Removed obsoletes patches.

* Sat Oct 22 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.4-owl1
- Updated to 1.4.4.
- Corrected info files installation.
- Packaged %_datadir/aclocal/m4.m4 from autoconf-2.59 sources.
- Applied ALT's build change to use getopt, error, libintl, and obstack
implementations from glibc rather than build them statically in this package.

* Fri Oct 21 2005 Alexandr D. Kanevskiy <kad-at-owl.openwall.com> 1.4.3-owl1
- Updated to 1.4.3.

* Thu Feb 26 2004 Michail Litvak <mci-at-owl.openwall.com> 1.4-owl17
- Fixed building with new auto* tools.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1.4-owl16
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Tue Feb 06 2001 Michail Litvak <mci-at-owl.openwall.com>
- Fixed format bug in error
- added __attribute__ ((format(...))) for error

* Sat Jan 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
