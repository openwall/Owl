# $Id: Owl/packages/readline/readline.spec,v 1.14 2004/01/15 22:45:17 mci Exp $

Summary: A library for editing typed in command lines.
Name: readline
Version: 4.1
Release: owl10
License: GPL
Group: System Environment/Libraries
Source: ftp://ftp.gnu.org/gnu/readline-%version.tar.gz
Patch0: readline-4.1-rh-guard.diff
Patch1: readline-4.1-deb-doc_makefile.diff
Patch2: readline-4.1-deb-inputrc.diff
Patch3: readline-4.1-deb-del_bcksp.diff
Patch4: readline-4.1-deb-char.diff
Patch5: readline-4.1-owl-info.diff
PreReq: /sbin/ldconfig, /sbin/install-info
Provides: libreadline.so.3, libreadline.so.3.0
Prefix: %_prefix
BuildRequires: sed
BuildRoot: /override/%name-%version

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%description
The readline library reads a line from the terminal and returns it,
allowing the user to edit the line with standard emacs editing keys.

%package devel
Summary: Files needed to develop programs which use the readline library.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
The readline library reads a line from the terminal and returns it,
allowing the user to edit the line with standard emacs editing keys.

This package contains the files needed to develop programs which use
the readline library to provide an easy to use and more intuitive
command line interface for users.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
rm doc/{history,readline,rluserman}.info
%configure
make all shared documentation CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_libdir

%makeinstall install install-shared

mkdir -p $RPM_BUILD_ROOT%_docdir/examples
install -m 644 examples/* $RPM_BUILD_ROOT%_docdir/examples

chmod 755 $RPM_BUILD_ROOT%_prefix/lib/*.so*

cd $RPM_BUILD_ROOT
ln -sf libreadline.so.%version .%_libdir/libreadline.so
ln -sf libhistory.so.%version .%_libdir/libhistory.so
ln -sf libreadline.so.%version \
	.%_libdir/libreadline.so.`echo %version | sed 's^\..*^^g'`
ln -sf libhistory.so.%version \
	.%_libdir/libhistory.so.`echo %version | sed 's^\..*^^g'`

# Hack!
ln -s libreadline.so.%version .%_libdir/libreadline.so.3
ln -s libreadline.so.%version .%_libdir/libreadline.so.3.0

%post
/sbin/ldconfig
/sbin/install-info %_infodir/history.info.gz %_infodir/dir
/sbin/install-info %_infodir/readline.info.gz %_infodir/dir

%postun -p /sbin/ldconfig

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/history.info.gz \
		%_infodir/dir
	/sbin/install-info --delete %_infodir/readline.info.gz \
		%_infodir/dir
fi

%files
%defattr(-,root,root)
%_mandir/man*/*
%_infodir/*.info*
%_libdir/lib*.so.*

%files devel
%defattr(-,root,root)
%doc examples/
%_includedir/readline
%_libdir/lib*.a
%_libdir/lib*.so

%changelog
* Thu Jan 15 2004 Michail Litvak <mci@owl.openwall.com> 4.1-owl10
- Put examples to right place.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 4.1-owl9
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Dec 08 2000 Michail Litvak <mci@owl.openwall.com>
- optflags_lib support.

* Wed Dec 06 2000 Michail Litvak <mci@owl.openwall.com>
- hack for compatibility with readline2
- spec file cleanups

* Tue Dec 05 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- added Debian patches
