# $Owl: Owl/packages/readline/readline.spec,v 1.23 2005/11/16 13:31:51 solar Exp $

%define compat_list 3 3.0 4.0 4.1 4.2

Summary: A library for editing typed in command lines.
Name: readline
Version: 4.3
Release: owl1
License: GPL
Group: System Environment/Libraries
Source: ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.gz
Patch0: readline-4.3-up-fixes.diff
Patch1: readline-4.3-alt-owl-nls.diff
Patch2: readline-4.3-alt-warnings.diff
Patch3: readline-4.3-deb-alt-inputrc.diff
Patch4: readline-4.3-deb-delete.diff
Patch5: readline-4.1-rh-man.diff
Patch6: readline-4.3-rh-histexpand-utf8.diff
Patch7: readline-4.3-owl-info.diff
PreReq: /sbin/ldconfig, /sbin/install-info
Provides: %(for n in %compat_list; do echo -n "libhistory.so.$n lib%name.so.$n "; done)
Prefix: %_prefix
BuildRequires: sed, texinfo
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
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{expand:%%define optflags %optflags -Wall}

%build
rm doc/{history,readline,rluserman}.info
%configure
make all shared documentation CFLAGS="%optflags -D_GNU_SOURCE"

%install
rm -rf %buildroot
mkdir -p %buildroot%_libdir

%makeinstall install install-shared

mkdir -p %buildroot%_docdir/examples
install -m 644 examples/* %buildroot%_docdir/examples

chmod 755 %buildroot%_prefix/lib/*.so*

cd %buildroot
ln -sf libreadline.so.%version .%_libdir/libreadline.so
ln -sf libhistory.so.%version .%_libdir/libhistory.so
ln -sf libreadline.so.%version \
	.%_libdir/libreadline.so.`echo %version | sed 's^\..*^^g'`
ln -sf libhistory.so.%version \
	.%_libdir/libhistory.so.`echo %version | sed 's^\..*^^g'`

for n in %name history; do
	t=`objdump -p "%buildroot%_libdir/lib$n.so" | awk '/SONAME/ {print $2}'`
	for v in %compat_list; do
		ln -s "$t" "%buildroot%_libdir/lib$n.so.$v"
	done
done

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_datadir/doc/examples/Inputrc
rm %buildroot%_datadir/doc/examples/Makefile
rm %buildroot%_datadir/doc/examples/Makefile.in
rm %buildroot%_datadir/doc/examples/excallback.c
rm %buildroot%_datadir/doc/examples/fileman.c
rm %buildroot%_datadir/doc/examples/histexamp.c
rm %buildroot%_datadir/doc/examples/manexamp.c
rm %buildroot%_datadir/doc/examples/readlinebuf.h
rm %buildroot%_datadir/doc/examples/rl.c
rm %buildroot%_datadir/doc/examples/rlcat.c
rm %buildroot%_datadir/doc/examples/rlfe.c
rm %buildroot%_datadir/doc/examples/rltest.c
rm %buildroot%_datadir/doc/examples/rlversion.c
rm %buildroot%_infodir/dir

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

# Remove remnants of this packaging error.  The directory contents are
# removed by RPM when package is upgraded, but the directory itself is
# not a part of the old packages and thus would remain.
%triggerpostun devel -- readline-devel < 4.1-owl11
if [ -d /usr/doc/examples ]; then
	rmdir /usr/doc/examples
fi

%files
%defattr(-,root,root)
%doc CHANGELOG CHANGES README
%_mandir/man*/*
%_infodir/*.info*
%_libdir/lib*.so.*

%files devel
%defattr(-,root,root)
%doc examples
%_includedir/readline
%_libdir/lib*.a
%_libdir/lib*.so

%changelog
* Wed Feb 18 2004 Michail Litvak <mci-at-owl.openwall.com> 4.3-owl1
- 4.3
- Added official patches, patches from Alt Linux Team,
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
