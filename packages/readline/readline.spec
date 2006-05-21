# $Owl: Owl/packages/readline/readline.spec,v 1.26 2006/05/21 00:02:51 ldv Exp $

Summary: A library for editing typed in command lines.
Name: readline
Version: 5.1
Release: owl1
License: GPL
Group: System Environment/Libraries
URL: http://www.gnu.org/software/%name/
Source: ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.gz
Patch0: readline-5.1-up-patchlevel.diff
Patch1: readline-5.1-rh-man.diff
Patch2: readline-5.1-alt-owl-shlib.diff
Patch3: readline-5.1-alt-warnings.diff
Patch4: readline-5.1-alt-nls.diff
Patch5: readline-5.1-deb-alt-inputrc.diff
Patch6: readline-5.1-deb-header.diff
Patch7: readline-5.1-rh-wrap.diff
Patch8: readline-5.1-owl-info.diff
PreReq: /sbin/ldconfig, /sbin/install-info
Prefix: %_prefix
BuildRequires: sed >= 4.0.9, texinfo
BuildRoot: /override/%name-%version

%description
The readline library reads a line from the terminal and returns it,
allowing the user to edit the line with standard emacs editing keys.

%package devel
Summary: Files needed to develop programs which use the readline library.
Group: Development/Libraries
Requires: %name = %version-%release
PreReq: /sbin/install-info

%description devel
The readline library reads a line from the terminal and returns it,
allowing the user to edit the line with standard emacs editing keys.

This package contains the files needed to develop programs which use
the readline library to provide an easy to use and more intuitive
command line interface for users.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
find -type f -name '*.orig' -delete -print
bzip2 -9k CHANGES

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags} -Wall -D_GNU_SOURCE}

%build
rm doc/*.info
# Fix temporary file handling
sed -i 's,/tmp/,,g' aclocal.m4
autoconf
%configure
make everything documentation

%install
rm -rf %buildroot

%makeinstall

# Relocate and fix documentation.
%define docdir %_docdir/%name-%version
mkdir -p %buildroot%docdir
cp -a README CHANGES.bz2 USAGE examples \
	%buildroot%docdir/
cp -p config.h posixstat.h xmalloc.h \
	%buildroot%docdir/examples/
sed -i -e 's,\.\./shlib/lib\([^.]\+\)\.so,-l\1,' \
	 -e 's,^\(top_srcdir *=\).*,\1 %_includedir/readline,g;s,^\(LDFLAGS *=\).*,\1,g' \
	 %buildroot%docdir/examples/Makefile
make -C %buildroot%docdir/examples clean

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/ldconfig
/sbin/install-info %_infodir/rluserman.info %_infodir/dir

%post devel
/sbin/install-info %_infodir/history.info %_infodir/dir
/sbin/install-info %_infodir/readline.info %_infodir/dir

%postun -p /sbin/ldconfig

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/rluserman.info \
		%_infodir/dir
fi

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/history.info \
		%_infodir/dir
	/sbin/install-info --delete %_infodir/readline.info \
		%_infodir/dir
fi

# Remove remnants of this packaging error.  The directory contents are
# removed by RPM when package is upgraded, but the directory itself is
# not a part of the old packages and thus would remain.
%triggerpostun devel -- readline-devel < 0:4.1-owl11
if [ -d /usr/doc/examples ]; then
	rmdir /usr/doc/examples
fi

%files
%defattr(-,root,root)
%dir %docdir
%docdir/[A-Z]*
%_infodir/rluserman.info*
%_libdir/lib*.so.*

%files devel
%defattr(-,root,root)
%dir %docdir
%docdir/examples
%_infodir/history.info*
%_infodir/readline.info*
%_mandir/man3/*
%_includedir/readline
%_libdir/lib*.a
%_libdir/lib*.so

%changelog
* Sun May 21 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.1-owl1
- Updated to 5.1 patchlevel 4.
- Dropped compatibility symlinks because new libhistory breaks backwards
binary compatibility.
- Restricted list of global symbols exported by libraries to the list
of symbols mentioned in the public API.
- Relocated development manpages and info documentation to -devel
subpackage.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.3-owl2
- Compressed CHANGES file, dropped CHANGELOG file.
- Corrected info files installation.

* Wed Feb 18 2004 Michail Litvak <mci-at-owl.openwall.com> 4.3-owl1
- 4.3
- Added official patches, patches from ALT Linux Team,
dropped outdated patches.
- Provide symlinks for compatibility with previous versions of readline.

* Sat Jan 17 2004 Solar Designer <solar-at-owl.openwall.com> 4.1-owl11
- Remove /usr/doc/examples with a trigger on package upgrades.

* Thu Jan 15 2004 Michail Litvak <mci-at-owl.openwall.com> 4.1-owl10
- Put examples to right place.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 4.1-owl9
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Dec 08 2000 Michail Litvak <mci-at-owl.openwall.com>
- optflags_lib support.

* Wed Dec 06 2000 Michail Litvak <mci-at-owl.openwall.com>
- hack for compatibility with readline2
- spec file cleanups

* Tue Dec 05 2000 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH
- added Debian patches
